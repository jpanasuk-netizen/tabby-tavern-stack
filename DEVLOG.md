# Tabby-Tavern Development Log

Engineering history for the containerized local AI lab. Public tree is sanitized — no live keys, no weights, no chat logs.

> **Basically, you can learn AI Infrastructure in 21 days too!**

Same GitHub repo, one README, one DEVLOG. Live Hugging Face surfaces: model card [`jpanasuk/tabby-tavern-stack`](https://huggingface.co/jpanasuk/tabby-tavern-stack) and sell-sheet Space [`jpanasuk/tabby-tavern-sell-sheet`](https://huggingface.co/spaces/jpanasuk/tabby-tavern-sell-sheet). Do not create `spaces/jpanasuk/tabby-tavern-stack`. Class files in `~/annie-scratch` stay out of this repo.

## Live vs shipped (same RTX 4070, not one running stack)

The services were **not fully merged**. Two compose projects, one GPU. Only Taproot is up.

**Live now (verified on LightBringer):**

- `qwen38-llama-server` — llama.cpp CUDA, Qwen3.5-9B UD-Q4_K_XL, host **:1234**, `n_ctx` 262144. **HOLD this container.** Do not `compose up` Taproot's qwen service to rename it.
- `taproot-webui` — Open WebUI, host **:3001**, `OPENAI_API_BASE_URL=http://host.docker.internal:1234/v1`

They sit on different Docker networks. The WebUI reaches llama through the host gateway, not a shared service name.

**Shipped, currently stopped:** Tabby Tavern six containers — SillyTavern `:8000`, Open WebUI `:3000`, TabbyAPI `:5000`, Ollama `:11435`, SearXNG `:8080`, MCPO `:8001`. Compose still exists. Ports **unchanged**. One 4070 cannot run Tabby GPU services and llama.cpp at the same time.

**Not running:** `docker-compose.starter.yml` is yaml only. It wants `taproot_ai-network` but still names `ollama` / `tabbyapi`. `anythingllm` would collide with Taproot host `:3001`.

**Not a container:** dockroot is source under the lab (`discover.py`, `tavern_mcp.py`), not a deployed container. Companions: [dockroot-mcp](https://huggingface.co/spaces/jpanasuk/dockroot-mcp) · [local-ai-stack-connectivity](https://huggingface.co/spaces/jpanasuk/local-ai-stack-connectivity).

**Tabby** = local AI you can actually use (chat stack, currently stopped).
**Taproot** = coding at home, live path `:3001` → `host.docker.internal:1234/v1` → `qwen38-llama-server`.

No Qwen3.5-9B llama.cpp tok/s is recorded here.

## Hardware baseline

- Host: LightBringer — WSL2 Ubuntu
- GPU: NVIDIA GeForce RTX 4070 (12 GB) — **one heavy engine at a time**
- Tabby recipe (compose exists, containers stopped): TabbyAPI + EXL3 / ExLlamaV3, SillyTavern, Open WebUI `:3000`, Ollama, SearXNG, MCPO
- Live path: llama.cpp on `:1234` + Taproot Open WebUI `:3001`

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

This week verified the **Tabby compose recipe** while Tabby owned the GPU. That is **not** the current live process list (Taproot owns the 4070 now).

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
- Optional `docker-compose.starter.yml` overlay for extra coding tools (not required, not running)

### Final verified state (24/24 checks) — Tabby recipe, when Tabby owned the GPU

- Six containers running, no restart loops
- TabbyAPI: EXL3 model loaded, chat ~53 tok/s processing
- Ollama: `llama3.1:8b` pulled
- Open WebUI: healthy, connected to TabbyAPI and Ollama
- SillyTavern: running with basic auth; cards importable
- SearXNG: serving with JSON format
- MCPO: 7 tool endpoints live
- GPU: 8 GB / 12 GB VRAM on RTX 4070

## v2.0.0 public release (2026-08-25)

- Hugging Face **model card** (this README YAML) documents the Tabby compose recipe (MCPO, dual backends, SillyTavern cards, WSL2 EXL3 notes)
- GitHub first tagged release (`v2.0.0`)
- Public `mcpo/config.json` no longer contains a live TabbyAPI key (placeholder only)
- That recipe is **not** the live process list. Live is Taproot WebUI `:3001` into llama.cpp `:1234`.

## Open follow-ups

- One-command bootstrap that builds the TabbyAPI image + prints next model download
- Healthcheck targets in compose
- Optional Traefik/Caddy reverse-proxy profile for LAN HTTPS
- Keep Redis as an optional compose profile if SearXNG cache becomes a bottleneck
