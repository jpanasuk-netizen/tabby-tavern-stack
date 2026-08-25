# Tabby-Tavern Development Log

Engineering history for the containerized local AI lab. Public tree is sanitized — no live keys, no weights, no chat logs.

## Hardware baseline

- GPU: NVIDIA GeForce RTX 4070 (12 GB)
- Environment: WSL2 Ubuntu + Docker Compose with NVIDIA GPU passthrough
- Primary inference path (v3 UNIFIED): Qwen3.5-9B GGUF on llama.cpp CUDA (`qwen` service)
- Alternate inference (profile): TabbyAPI EXL3 + Ollama GGUF
- Character frontend: SillyTavern (PNG character cards)
- Tooling: MCPO + FastMCP; optional dockroot diagnostics
- Coding pack: former Basecamp volumes on the same network

## v3.0.0 UNIFIED — Taproot + Basecamp folded in (2026-08-25)

Hermes session `20260825_002829` merged the running Taproot Qwen stack and Basecamp coding pack into `/home/jpanasuk/tabby-tavern/docker-compose.yml`.

- Compose project: `tabby-tavern`
- Network: `tabby-tavern_ai-network`
- Default: 15 services. Qwen and Postgres healthy. SearXNG / MCPO / code-server / Qdrant / Meilisearch HTTP 200.
- Primary endpoint: `http://qwen:8080/v1` in-network, `http://localhost:1234/v1` on the host. Model alias `Qwen3.5-9B`.
- TabbyAPI + Ollama: `--profile alternate-inference` (VRAM contention).
- dockroot: `--profile diagnostics`, socket read-only, no host port.
- Basecamp named volumes preserved (`basecamp_*`).
- Public tree sanitizes host model paths to `./models/...` and drops `external: true` so a stranger can `up` without those volume names pre-created.
- Sell sheet rewritten from this live graph — not the old 6-service pitch and not the fake 21-service pitch.

## Week 1 — Core integration

- Consolidated TabbyAPI, SillyTavern, Open WebUI, Ollama, SearXNG into one compose file
- Adopted EXL3 weights for faster VRAM load vs earlier experiments
- Fixed cross-container TabbyAPI auth/whitelist failures that blocked peer services
- Added persistent volume mounts for configs and data directories

## Week 2 — Model bring-up & GPU tuning

- Loaded Llama-3.1-8B-Instruct EXL3 (6.0 bpw class) into `tabby_models/`
- Tuned container env: flash attention / KV cache flags, `shm_size: 16g`, CUDA device ordering
- Documented start/stop operational loop (`docker compose down && up -d`)

## Week 3 — Public packaging

- Created sanitized publish tree (no weights, no user DBs, no tokens)
- Added SECURITY.md and example TabbyAPI config
- Mirrored narrative to GitHub portfolio rebuild (Aug 2026)
- Early public revisions accidentally included lab convenience keys — treat those as burned (see SECURITY.md)

## Week 4 — WSL2 fresh install + MCPO (Aug 2026)

Full from-scratch rebuild on clean WSL2 (same RTX 4070). Every fix is in the README WSL2 field notes.

### Issues hit and resolved

- **EXL2 dropped from TabbyAPI.** `ghcr.io/theroyallab/tabbyapi:latest` no longer loads EXL2. Switched to `turboderp/Llama-3.1-8B-Instruct-exl3` 6.0bpw.
- **NVIDIA Container Toolkit repo URL.** `deb ... noble main` → apt `Malformed entry (Component)`. Flat repo line with `amd64 /` works.
- **libcuda.so missing in container.** Triton/exllamav3 link step needs `-lcuda`. Dockerfile now symlinks `/usr/local/cuda-12.8/compat/libcuda.so`.
- **Port conflict with host Ollama.** Docker Ollama remapped to host **11435**.
- **Open WebUI only wired to Ollama.** Added `OPENAI_API_BASE_URL=http://tabbyapi:5000/v1` so the UI can use EXL3 and GGUF.
- **SillyTavern browser launch in Docker.** `browserLaunch.enabled: false`. Keep `basicAuthMode: true` or ST will refuse to start on 0.0.0.0.
- **SearXNG JSON format.** Default was HTML-only; added `json` for MCPO + Open WebUI RAG.
- **12 GB VRAM tuning.** `cache_8bit: true`, `max_seq_len: 8192`, `cache_size: 8192`. ~8 GB used by 6.0bpw EXL3, ~4 GB left for a small GGUF.

### MCPO MCP server — built and integrated

- FastMCP server at `mcp-servers/server.py` (not raw JSON-RPC)
- Seven tools via MCPO OpenAPI at `/host-master/`:
  - `list_tabbyapi_models`
  - `tabbyapi_chat`
  - `list_ollama_models`
  - `ollama_pull_model`
  - `ollama_chat`
  - `get_stack_status`
  - `searxng_search`
- MCPO config uses `/app/.venv/bin/python3` because that venv has `mcp`
- Empty `mcpServers` crashes MCPO — always ship at least one entry
- Companion `tavern_mcp.py` is the connectivity toolkit (status / self-check / wire)

### Character cards

- SillyTavern PNG character cards are first-class in this tree (`cards/`)
- Default Seraphina card + expression sprites copied from the lab ST data dir (no chats, no secrets)
- README documents import into a fresh SillyTavern

### Compose shape vs earlier public tree

- **In:** `mcpo` service (port 8001), Open WebUI dual-backend env, Ollama host 11435, character cards
- **Out of core compose:** SearXNG Redis (SearXNG runs fine without it; JSON search still works)
- Optional `docker-compose.starter.yml` overlay for extra coding tools (not required)

### Final verified state (24/24 checks)

- Six containers running, no restart loops
- TabbyAPI: EXL3 model loaded, chat ~53 tok/s processing
- Ollama: `llama3.1:8b` pulled
- Open WebUI: healthy, connected to TabbyAPI and Ollama
- SillyTavern: running with basic auth; cards importable
- SearXNG: serving with JSON format
- MCPO: 7 tool endpoints live
- GPU: 8 GB / 12 GB VRAM on RTX 4070

## v2.0.0 public release (2026-08-25)

- Hugging Face **model card** (this README YAML) brought in sync with the live lab
- GitHub first tagged release (`v2.0.0`)
- Public `mcpo/config.json` no longer contains a live TabbyAPI key (placeholder only)
- Cards, MCPO, WSL2 Dockerfile fix, and dual-backend Open WebUI are in the published compose

## Open follow-ups

- One-command bootstrap that builds the TabbyAPI image + prints next model download
- Healthcheck targets in compose
- Optional Traefik/Caddy reverse-proxy profile for LAN HTTPS
- Keep Redis as an optional compose profile if SearXNG cache becomes a bottleneck
