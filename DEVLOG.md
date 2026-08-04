# Tabby-Tavern Development Log

Engineering history for the containerized local AI lab.

## Hardware baseline
- GPU: NVIDIA GeForce RTX 4070
- Environment: Linux + Docker Compose with NVIDIA GPU passthrough
- Primary inference path: TabbyAPI + EXL3 / ExLlamaV3
- Secondary path: Ollama (GGUF)

## Week 1 — Core integration
- Consolidated TabbyAPI, SillyTavern, Open WebUI, Ollama, SearXNG (+ Redis) into one compose file
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

## Open follow-ups
- One-command bootstrap that builds the TabbyAPI image + prints next model download
- Healthcheck targets in compose
- Optional Traefik/Caddy reverse-proxy profile for LAN HTTPS
