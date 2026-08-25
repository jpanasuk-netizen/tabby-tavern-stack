# MCP servers

Mounted read-only into the `mcpo` container at `/opt/mcp-servers`.

| File | Role |
| ---- | ---- |
| `server.py` | FastMCP stack tools (`host-master`) — list/chat TabbyAPI + Ollama, stack health, SearXNG |
| `tavern_mcp.py` | Optional connectivity toolkit (status / self-check / wire). Needs `discover.py` beside it if you use those tools. |

`mcpo/config.json` in the public tree only registers `host-master`. Add `tavern` there only if you also provide its companion scripts.

Do not put live API keys in these files — they read `TABBYAPI_KEY` from the MCPO config `env` block.
