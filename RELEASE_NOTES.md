# Tabby Tavern stack v2.0.0

First tagged release of the live lab tree. Hugging Face model card, GitHub, and this tag are aligned.

Tabby Tavern 2.0 is the **Independent AI Lab** on LightBringer: six-service EXL3 compose in this repo **and** the llama.cpp 262k operator desk (`~/taproot`, WebUI :3001, Continue, Grok, Hermes). Tabby service names/ports stay Tabby. See README / DEVLOG (2026-08-25).

## What's in the stack now

- TabbyAPI EXL3 (ExLlamaV3) on `local/tabbyapi:exl3-fixed`
- SillyTavern with **character cards** shipped under `cards/`
- Open WebUI dual backend (Ollama GGUF **and** TabbyAPI OpenAI-compatible)
- Ollama on host port **11435** (avoids colliding with host `ollama serve`)
- SearXNG with JSON search (MCPO + RAG)
- **MCPO** FastMCP server — 7 stack tools at http://localhost:8001/docs

## Docs

- Hugging Face **model card** is `README.md` (YAML frontmatter)
- `DEVLOG.md` covers WSL2 EXL2→EXL3, NVIDIA toolkit repo line, `libcuda.so` symlink, 12 GB `cache_8bit` tuning
- `SECURITY.md` — rotate any key that ever appeared in an older public revision

## Not included

Model weights, live API keys, chat logs, Open WebUI DBs.

## Import cards

SillyTavern → Characters → Import → `cards/default_Seraphina.png`
