# Tabby-Tavern Development Log

Engineering history for the Independent AI Lab on LightBringer. Public tree is sanitized — no live keys, no weights, no chat logs.

**Tabby Tavern 2.0 is the whole lab:** EXL3 Tabby compose (this repo) + llama.cpp 262k operator desk (`~/taproot`) + VS Code / Continue / Grok / Hermes + MCP. Tabby **service names and ports stay Tabby**. Class files in `~/annie-scratch` stay out of this repo.

## Hardware baseline

- Host: LightBringer — WSL2 Ubuntu
- GPU: NVIDIA GeForce RTX 4070 (12 GB) — **one heavy engine at a time**
- Character / EXL3 layer: TabbyAPI + SillyTavern + Open WebUI :3000 + Ollama :11435 + SearXNG + MCPO
- Long-context layer: llama.cpp Qwen3.5-9B `n_ctx` 262144 on :1234 + Open WebUI :3001
- Desk: Windows VS Code + Remote-WSL + Continue 2.0; Grok 1.0.5; Hermes v0.20.0
- Docker vision: `~/dockroot` helper + dockroot-mcp Space

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

## 2026-08-25 — full lab: EXL3 compose + llama.cpp 262k desk

GitHub README was stale vs the live box (it still read as if Tabby owned the GPU). **This snapshot wins.** Tabby compose was **not** rewritten and was **not** renamed to Taproot. `~/annie-scratch` class files stay out of this repo.

Tabby Tavern 2.0 **is** the whole LightBringer lab. The llama.cpp / Continue / Grok / Hermes path is first-class, not a footnote.

### What is actually running (LightBringer)

- **Operator layer** — `/home/jpanasuk/taproot/docker-compose.yml`, project name `taproot`:
  - `qwen38-llama-server` **Up**, `0.0.0.0:1234->8080`, image `ghcr.io/ggml-org/llama.cpp:server-cuda`, model Qwen3.5-9B UD-Q4_K_XL, `n_ctx` 262144. Container name is still `qwen38-llama-server` (yaml wants `taproot-qwen`; **not recreated** — do not bounce it).
  - `taproot-webui` **Up** on **:3001**, `WEBUI_NAME=Taproot`, `OPENAI_API_BASE_URL=http://host.docker.internal:1234/v1`, data `/home/jpanasuk/taproot/open-webui-data`. Separate from Tabby Open WebUI **:3000** so the UIs do not share a database.
- `/home/jpanasuk/qwen38-agent/docker-compose.yml` still exists (27B then 9B 262k). Live llama started from this lineage.
- `tabby-tavern_ai-network` was **removed** so the two GPU stacks do not collide (two heavy engines on 12 GB stall CUDA instead of erroring).
- `/home/jpanasuk/tabby-tavern/docker-compose.yml` **restored** from `.bak-tabby` (Tabby names/ports). All Tabby containers **Exited** ~17 h, `restart=no`.
- Grok 1.0.5 at `/home/jpanasuk/.local/bin/grok`. Hermes v0.20.0 at `~/.hermes/hermes-agent`.
- Windows VS Code **1.134.0** + Remote-WSL **0.104.3** + Continue **2.0** on `/home/jpanasuk/taproot`. Continue → `http://127.0.0.1:1234/v1` Qwen3.5-9B (`~/.continue/config.yaml`).
- Linux snap VS Code **1.134.0** on `~/annie-scratch` is **Annie++ Python class only** — not the lab desk.
- Dockroot `~/dockroot` is a local recipe/MCP helper (`tavern.sh`, `tavern_mcp.py`, `discover.py`, `recipes.py`), **not** running as a container right now.

### VRAM last call

RTX 4070: **11450 / 12282 MiB** with llama resident. Tabby GPU (Ollama / TabbyAPI) **stays down** while llama is on the 4070. Xwayland ~3.6 GB when the desktop is up. Do not kill grok / hermes / llama to clean tavern.

No Qwen3.5-9B llama.cpp tok/s is recorded here.

### Public 2.0 packaging (same calendar day)

- README retitled **Tabby Tavern 2.0** as the Independent AI Lab: EXL3 character path **and** llama.cpp 262k operator path **and** VS Code/Continue/Grok/Hermes **and** MCP. Compose architecture in this repo unchanged (Tabby names/ports).
- Static HTML family under `docs/spaces/` (shared `tavern.css`): sell sheet, lab-tour Space, connectivity companion, dockroot companion — one product story.
- Intended new Hugging Face **Space** `jpanasuk/tabby-tavern-stack` (static SDK) is distinct from the existing **model card** at `huggingface.co/jpanasuk/tabby-tavern-stack`. Upload commands: `docs/spaces/UPLOAD.md`. This environment has no HF token; the Space is not live until those commands run.

## Open follow-ups

- One-command bootstrap that builds the TabbyAPI image + prints next model download
- Healthcheck targets in compose
- Optional Traefik/Caddy reverse-proxy profile for LAN HTTPS
- Keep Redis as an optional compose profile if SearXNG cache becomes a bottleneck
