#!/usr/bin/env python3
"""
Tabby Tavern MCP Server — exposes stack management tools via Model Context Protocol.
Run inside the MCPO container (has mcp library in /app/.venv).
"""
import subprocess
import json
import httpx
import os
import socket
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("tabby-tavern")

# Service endpoints (use Docker network names when inside compose)
TABBYAPI_URL = os.environ.get("TABBYAPI_URL", "http://tabbyapi:5000")
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://ollama:11434")
TABBYAPI_KEY = os.environ.get("TABBYAPI_KEY", "")


@mcp.tool()
def list_tabbyapi_models() -> str:
    """List all available models in TabbyAPI (EXL3 inference engine)."""
    try:
        headers = {}
        if TABBYAPI_KEY:
            headers["Authorization"] = f"Bearer {TABBYAPI_KEY}"
        r = httpx.get(f"{TABBYAPI_URL}/v1/models", headers=headers, timeout=10)
        data = r.json()
        models = [m["id"] for m in data.get("data", [])]
        return json.dumps({"models": models, "count": len(models)}, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def tabbyapi_chat(message: str, max_tokens: int = 256) -> str:
    """Send a chat message to the TabbyAPI EXL3 model and get a response.
    
    Args:
        message: The user message to send to the model
        max_tokens: Maximum tokens to generate (default 256)
    """
    try:
        headers = {"Content-Type": "application/json"}
        if TABBYAPI_KEY:
            headers["Authorization"] = f"Bearer {TABBYAPI_KEY}"
        
        # First get the available model
        r = httpx.get(f"{TABBYAPI_URL}/v1/models", headers=headers, timeout=10)
        models = r.json().get("data", [])
        if not models:
            return json.dumps({"error": "No models loaded in TabbyAPI"})
        
        model_name = models[0]["id"]
        
        r = httpx.post(
            f"{TABBYAPI_URL}/v1/chat/completions",
            headers=headers,
            json={
                "model": model_name,
                "messages": [{"role": "user", "content": message}],
                "max_tokens": max_tokens,
            },
            timeout=60,
        )
        data = r.json()
        content = data["choices"][0]["message"]["content"]
        return json.dumps({
            "model": model_name,
            "response": content,
            "finish_reason": data["choices"][0].get("finish_reason", "stop"),
        }, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def list_ollama_models() -> str:
    """List all models available in the Ollama (GGUF) backend."""
    try:
        r = httpx.get(f"{OLLAMA_URL}/api/tags", timeout=10)
        data = r.json()
        models = [{"name": m["name"], "size_mb": m["size"] // 1024 // 1024} for m in data.get("models", [])]
        return json.dumps({"models": models, "count": len(models)}, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def ollama_pull_model(model_name: str) -> str:
    """Pull a model into the Ollama backend (e.g., 'llama3.1:8b', 'qwen2.5:7b').
    
    Args:
        model_name: The Ollama model tag to pull (e.g., 'llama3.1:8b')
    """
    try:
        r = httpx.post(f"{OLLAMA_URL}/api/pull", json={"name": model_name}, timeout=300)
        return json.dumps({"status": "success", "model": model_name, "response": r.text[:500]})
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def ollama_chat(message: str, model: str = "llama3.1:8b") -> str:
    """Send a chat message to an Ollama model and get a response.
    
    Args:
        message: The user message to send
        model: The Ollama model to use (default: llama3.1:8b)
    """
    try:
        r = httpx.post(
            f"{OLLAMA_URL}/api/chat",
            json={
                "model": model,
                "messages": [{"role": "user", "content": message}],
                "stream": False,
            },
            timeout=120,
        )
        data = r.json()
        return json.dumps({
            "model": model,
            "response": data.get("message", {}).get("content", ""),
            "eval_count": data.get("eval_count", 0),
            "eval_duration_s": data.get("eval_duration", 0) / 1e9,
        }, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def get_stack_status() -> str:
    """Check the health of all Tabby Tavern services and return a status report."""
    services = {
        "tabbyapi": f"{TABBYAPI_URL}/v1/models",
        "ollama": f"{OLLAMA_URL}/api/tags",
        "open-webui": "http://open-webui:8080/",
        "sillytavern": "http://sillytavern:8000/",
        "searxng": "http://searxng:8080/",
    }
    results = {}
    for name, url in services.items():
        try:
            r = httpx.get(url, timeout=5)
            results[name] = {"status": "online", "http_code": r.status_code}
        except Exception as e:
            results[name] = {"status": "offline", "error": str(e)}
    
    return json.dumps(results, indent=2)


@mcp.tool()
def searxng_search(query: str, num_results: int = 5) -> str:
    """Search the web using the SearXNG private metasearch engine.
    
    Args:
        query: The search query
        num_results: Maximum number of results to return (default 5)
    """
    try:
        r = httpx.get(
            "http://searxng:8080/search",
            params={"q": query, "format": "json"},
            timeout=15,
        )
        data = r.json()
        results = []
        for item in data.get("results", [])[:num_results]:
            results.append({
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "content": item.get("content", "")[:200],
                "engine": item.get("engine", ""),
            })
        return json.dumps({"query": query, "results": results, "count": len(results)}, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


if __name__ == "__main__":
    mcp.run()