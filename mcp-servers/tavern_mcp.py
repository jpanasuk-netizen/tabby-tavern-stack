#!/usr/bin/env python3
"""Tavern MCP server — exposes the basecamp connectivity toolkit as
first-class Hermes tools (mcp_tavern_status, mcp_tavern_self_check,
mcp_tavern_wire, mcp_tavern_rediscover, mcp_tavern_models,
mcp_tavern_chat).

Protocol: proper MCP stdio server. Waits for the client's initialize
request, responds with server capabilities, then serves tools/list and
tools/call. Pure stdlib — no external deps.

FIXED 2026-08-10: the old stub sent unsolicited initialize/initialized
messages on startup (client->server messages) — the client saw garbage
and closed the connection ("Connection failed: Connection closed").
"""
import json
import os
import subprocess
import sys

DISCOVER = "/opt/basecamp/discover.py"
TAVERN = "/usr/local/bin/tavern"
# Fallbacks for running outside basecamp (e.g. in MCPO's container): use
# the discover.py that sits next to this file if /opt/basecamp isn't there.
if not os.path.exists(DISCOVER):
    _here = os.path.dirname(os.path.abspath(__file__))
    for cand in (os.path.join(_here, "discover.py"),
                 os.path.join(_here, "..", "discover.py")):
        if os.path.exists(cand):
            DISCOVER = os.path.abspath(cand)
            break

# ── stdio helpers ──


def _send(msg):
    sys.stdout.write(json.dumps(msg) + "\n")
    sys.stdout.flush()


def _read():
    """Yield parsed JSON-RPC messages from stdin (notifications + requests)."""
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            yield json.loads(line)
        except json.JSONDecodeError:
            continue


def _run(cmd, timeout=120):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return {"exit": r.returncode, "stdout": r.stdout[-4000:], "stderr": r.stderr[-2000:]}
    except subprocess.TimeoutExpired:
        return {"exit": -1, "stdout": "", "stderr": f"timed out after {timeout}s"}
    except Exception as e:
        return {"exit": -2, "stdout": "", "stderr": str(e)}


def _tool_result(text):
    return {"content": [{"type": "text", "text": text}]}


def _call_tool(name, args):
    # tavern CLI may not exist in every container (MCPO's image has none) —
    # fall back to discover.py actions when the CLI is missing.
    def tavern_or_discover(tavern_cmd, discover_action):
        if os.path.exists(TAVERN):
            return _run(tavern_cmd)
        return _run(["python3", DISCOVER, discover_action])

    if name == "status":
        r = tavern_or_discover([TAVERN, "status"], "scan")
    elif name == "self_check":
        r = _run(["python3", DISCOVER, "self-check"])
    elif name == "wire":
        r = _run(["python3", DISCOVER, "wire"])
    elif name == "rediscover":
        r = _run(["python3", DISCOVER, "scan"])
    elif name == "models":
        r = tavern_or_discover([TAVERN, "models"], "models")
    elif name == "chat":
        prompt = args.get("prompt", "hi")
        r = tavern_or_discover([TAVERN, "chat", prompt], "chat")
    # ── Virtual docker root: read-only power over the box's own
    # containers (the docker socket must be mounted into the container —
    # see basecamp.sh BASECAMP_DOCKER=1). Scoped to the discovered
    # network; never touches host root. ──
    elif name == "docker_ps":
        net = args.get("network", "")
        cmd = ["docker", "ps", "-a", "--format",
               "{{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}"]
        if net:
            cmd += ["--filter", f"network={net}"]
        r = _run(cmd)
    elif name == "docker_logs":
        container = args.get("container", "")
        tail = str(args.get("tail", 50))
        if not container:
            return _tool_result("error: 'container' argument is required")
        r = _run(["docker", "logs", "--tail", tail, container])
    elif name == "docker_inspect":
        container = args.get("container", "")
        if not container:
            return _tool_result("error: 'container' argument is required")
        r = _run(["docker", "inspect", container])
    elif name == "docker_stats":
        r = _run(["docker", "stats", "--no-stream",
                  "--format", "{{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"])
    elif name == "docker_networks":
        r = _run(["docker", "network", "ls", "--format", "{{.Name}}\t{{.Driver}}"])
    else:
        return _tool_result(f"unknown tool: {name}")
    out = r["stdout"] or r["stderr"] or f"(exit {r['exit']})"
    return _tool_result(out)


TOOLS = [
    {
        "name": "status",
        "description": "List every discovered service with its link:port "
                       "(e.g. http://starter-code-server:8080). Use for "
                       "'what's connected', 'show my services', 'ports'.",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "self_check",
        "description": "Verify every service's health (HTTP + TCP sweep of "
                       "all known containers). Use for 'verify my "
                       "connections', 'is everything working', 'test my "
                       "stack'. Reports healthy/failing counts.",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "wire",
        "description": "Audit what should talk to what, with exact fixes. "
                       "Use for 'why doesn't X work', 'connect X to Y', "
                       "'fix my wiring'.",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "rediscover",
        "description": "Re-scan the network for new or changed services.",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "models",
        "description": "List available models on the discovered inference "
                       "engines.",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "chat",
        "description": "Chat with the primary inference engine (one-shot).",
        "inputSchema": {
            "type": "object",
            "properties": {"prompt": {"type": "string"}},
            "required": ["prompt"],
        },
    },
    # ── Virtual docker root (read-only, scoped to the box's network) ──
    {
        "name": "docker_ps",
        "description": "List containers on the box's Docker network "
                       "(virtual docker root — read-only). Optional "
                       "'network' filter. Use for 'what containers are "
                       "running', 'is X up'.",
        "inputSchema": {
            "type": "object",
            "properties": {"network": {"type": "string"}},
        },
    },
    {
        "name": "docker_logs",
        "description": "Tail logs of a container (read-only). Use for "
                       "'why is X failing', 'show me X's logs'.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "container": {"type": "string"},
                "tail": {"type": "integer"},
            },
            "required": ["container"],
        },
    },
    {
        "name": "docker_inspect",
        "description": "Inspect a container's full config (env, mounts, "
                       "network, health). Use for 'what env does X have', "
                       "'is X wired to Y'.",
        "inputSchema": {
            "type": "object",
            "properties": {"container": {"type": "string"}},
            "required": ["container"],
        },
    },
    {
        "name": "docker_stats",
        "description": "Live CPU/memory usage of running containers "
                       "(read-only).",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "docker_networks",
        "description": "List Docker networks (read-only). Use for "
                       "'what networks exist'.",
        "inputSchema": {"type": "object", "properties": {}},
    },
]

SERVER_INFO = {"name": "tavern", "version": "1.0.6"}


def main():
    initialized = False
    for msg in _read():
        method = msg.get("method", "")
        mid = msg.get("id")
        is_notification = mid is None

        if method == "initialize":
            # Respond with server capabilities (the handshake).
            _send({"jsonrpc": "2.0", "id": mid, "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": SERVER_INFO,
            }})
            initialized = True
        elif method == "notifications/initialized":
            continue  # client says it's ready — nothing to do
        elif method == "ping":
            if not is_notification:
                _send({"jsonrpc": "2.0", "id": mid, "result": {}})
        elif method == "tools/list":
            if not is_notification:
                _send({"jsonrpc": "2.0", "id": mid, "result": {"tools": TOOLS}})
        elif method == "tools/call":
            if not is_notification:
                params = msg.get("params", {})
                name = params.get("name", "")
                args = params.get("arguments", {})
                _send({"jsonrpc": "2.0", "id": mid, "result": _call_tool(name, args)})
        elif method == "shutdown":
            if not is_notification:
                _send({"jsonrpc": "2.0", "id": mid, "result": None})
            break
        elif method == "exit":
            break
        # Unknown methods: respond with -32601 if it's a request.
        elif not is_notification:
            _send({"jsonrpc": "2.0", "id": mid,
                   "error": {"code": -32601, "message": f"method not found: {method}"}})


if __name__ == "__main__":
    main()
