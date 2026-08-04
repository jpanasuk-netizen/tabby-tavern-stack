# Tabby Tavern Stack

**Containerized private AI lab:** TabbyAPI (EXL3 / ExLlamaV3) + SillyTavern + Open WebUI + Ollama + SearXNG.

This is the application-layer companion to [`local_grid_suite`](https://github.com/jpanasuk-netizen/local_grid_suite) (telemetry/benchmarking). Together they document a full independent year of local AI systems work on an NVIDIA RTX 4070 box.

Also published on Hugging Face: [jpanasuk/tabby-tavern-stack](https://huggingface.co/jpanasuk/tabby-tavern-stack)

[![Stack](https://img.shields.io/badge/Stack-Docker%20Compose-blue)]()
[![GPU](https://img.shields.io/badge/GPU-NVIDIA%20EXL3-success)]()
[![License](https://img.shields.io/badge/License-MIT-green)]()

---

## What you get

| Service | Default URL | Role |
|---------|-------------|------|
| SillyTavern | http://localhost:8000 | Chat / character frontend |
| Open WebUI | http://localhost:3000 | General LLM workspace |
| TabbyAPI | http://localhost:5000 | EXL3 high-performance inference |
| Ollama | http://localhost:11434 | GGUF model backend |
| SearXNG | http://localhost:8080 | Private metasearch |

Optional Redis supports SearXNG caching in the compose file.

---

## Requirements

- Linux or Windows **WSL2**
- NVIDIA GPU + [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)
- Docker + Docker Compose plugin
- Disk space for EXL3/GGUF weights (not included)

---

## Quick start

```bash
git clone https://github.com/jpanasuk-netizen/tabby-tavern-stack.git
cd tabby-tavern-stack

# 1) Build the TabbyAPI image used by compose
docker build -f Dockerfile.tabby -t local/tabbyapi:exl3-fixed .

# 2) Download an EXL3 model into tabby_models/
mkdir -p tabby_models
# example:
# huggingface-cli download turboderp/Llama-3.1-8B-Instruct-exl3 \
#   --revision 6.0bpw --local-dir tabby_models/Llama-3.1-8B-Instruct-6.0bpw-exl3

# 3) Configure TabbyAPI (start from example)
cp tabby_config/config.example.yml tabby_config/config.yml
# edit model name / network / credentials

# 4) Launch
docker compose up -d
docker compose ps
docker compose logs -f tabbyapi
```

Helper script (adjust paths inside if needed):

```bash
chmod +x start-stack.sh load-model.sh
./start-stack.sh
```

---

## Repository layout

```text
tabby-tavern-stack/
├── docker-compose.yml      # full lab orchestration
├── Dockerfile / Dockerfile.tabby
├── start-stack.sh
├── tabby_config/           # TabbyAPI templates
├── sillytavern_config/
├── searxng_config/
├── tabby_models/           # gitignored weights (placeholder only)
├── SECURITY.md
├── DEVLOG.md               # engineering history
└── docs/                   # sell sheet / extras
```

---

## Engineering notes

See [`DEVLOG.md`](DEVLOG.md) for the real build log: EXL3 adoption, compose consolidation, GPU env tuning (`shm_size`, flash-attn / KV cache flags), and the container-to-TabbyAPI auth/whitelist fix.

**Security posture:** this is a **private lab stack**. Read [`SECURITY.md`](SECURITY.md) before exposing ports. Do not reuse lab convenience credentials on a shared network.

---

## Related work

| Project | Link |
|---------|------|
| Local Grid Suite (benchmarks/telemetry) | https://github.com/jpanasuk-netizen/local_grid_suite |
| Multi-agent dungeon prototype | https://github.com/jpanasuk-netizen/multi-agent-dungeon-crawler |
| HF model card / stack mirror | https://huggingface.co/jpanasuk/tabby-tavern-stack |

---

## Author

**Jeremy Panasuk** · [@jpanasuk-netizen](https://github.com/jpanasuk-netizen) · [huggingface.co/jpanasuk](https://huggingface.co/jpanasuk)

Independent engineer — enterprise data platforms background; 2024–present local AI infrastructure.

## License

MIT
