---
title: Tabby Tavern + Taproot — Independent AI Lab
emoji: 🏠
colorFrom: blue
colorTo: indigo
sdk: static
pinned: true
license: mit
short_description: Live Taproot on :3001/:1234; Tabby compose is stopped
tags:
  - portfolio
  - local-ai
  - docker
  - private-ai
  - mcp
  - sillytavern
  - taproot
  - llama-cpp
---

# Tabby Tavern + Taproot — Independent AI Lab

> **Basically, you can learn AI Infrastructure in 21 days too!**

One RTX 4070. **Two compose files. Not one live stack.**

- **Live:** Taproot — llama.cpp Qwen3.5-9B on :1234 (`n_ctx` 262144), Open WebUI on :3001 via `host.docker.internal:1234/v1`.
- **Shipped, currently stopped:** Tabby Tavern — SillyTavern, EXL3 / TabbyAPI :5000, Open WebUI :3000, Ollama :11435, SearXNG :8080, MCPO :8001.
- **Not running:** coding starter pack (yaml only; `anythingllm` collides with :3001).
- **Not a container:** dockroot is MCP/diagnostics source, not a deployed service.

Open the **App** tab.

- Model card: https://huggingface.co/jpanasuk/tabby-tavern-stack
- GitHub: https://github.com/jpanasuk-netizen/tabby-tavern-stack
- Companions: [dockroot-mcp](https://huggingface.co/spaces/jpanasuk/dockroot-mcp) · [connectivity](https://huggingface.co/spaces/jpanasuk/local-ai-stack-connectivity)
