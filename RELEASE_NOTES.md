# Tabby Tavern stack v2.0.0

First tagged release of the **Tabby compose recipe**. Hugging Face model card, GitHub, and this tag document that recipe.

**Live vs shipped:** Taproot is up (`qwen38-llama-server` `:1234`, `taproot-webui` `:3001`). Tabby’s six containers are **stopped**. Two compose files, not one running stack. See README / DEVLOG.

## What's in the Tabby recipe (shipped, currently stopped)

- TabbyAPI EXL3 (ExLlamaV3) on `local/tabbyapi:exl3-fixed`
- SillyTavern with **character cards** shipped under `cards/`
- Open WebUI dual backend (Ollama GGUF **and** TabbyAPI OpenAI-compatible)
- Ollama on host port **11435** (avoids colliding with host `ollama serve`)
- SearXNG with JSON search (MCPO + RAG)
- **MCPO** FastMCP server — 7 stack tools at http://localhost:8001/docs

## Docs

- Hugging Face **model card** is `README.md` (YAML frontmatter)
- `DEVLOG.md` covers WSL2 EXL2→EXL3, NVIDIA toolkit repo line, `libcuda.so` symlink, 12 GB `cache_8bit` tuning, and live vs shipped topology
- `SECURITY.md` — rotate any key that ever appeared in an older public revision

## Not included

Model weights, live API keys, chat logs, Open WebUI DBs.

## Import cards

SillyTavern → Characters → Import → `cards/default_Seraphina.png`
