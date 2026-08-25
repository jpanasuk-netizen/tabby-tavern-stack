---
license: mit
tags:
- exl3
- exllamav3
- tabby
- tabbyapi
- docker
- docker-compose
- sillytavern
- character-card
- open-webui
- openwebui
- ollama
- mcp
- model-context-protocol
- mcpo
- searxng
- llm
- local-llm
- self-hosted
- ai-infrastructure
- rtx-4070
- nvidia
- cuda
- wsl2
- ubuntu
- inference-stack
- multi-service
pipeline_tag: text-generation
library_name: exllama
---

# Tabby Tavern 2.0

**Six-service containerized private AI lab.** This repo is the Tabby product:

| Layer | Software |
| --------------------- | ----------------------------------- |
| High-perf inference | **TabbyAPI** + **EXL3 / ExLlamaV3** |
| Character chat UI | **SillyTavern** (+ shipped **character cards**) |
| General LLM workspace | **Open WebUI** on **:3000** (Ollama **and** TabbyAPI) |
| GGUF backend | **Ollama** (host **:11435**) |
| Private search | **SearXNG** |
| Tooling / MCP | **MCPO** + FastMCP stack server |

This is a **private-lab / portfolio** stack — production-*shaped*, not a multi-tenant SaaS product and not a hosted inference endpoint.

**Taproot is not this repo.** On the same workstation a separate compose project (`taproot`) currently runs llama.cpp + its own Open WebUI on **:3001**. It is linked below so you do not mix brands, ports, or GPU owners. A brief Taproot rebrand of Tabby compose was reverted; Tabby names and ports stay Tabby.

Lab hardware: **LightBringer**, WSL2 Ubuntu, **NVIDIA RTX 4070 12 GB**.

| Surface | URL |
| -------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| **GitHub (source of truth)** | [https://github.com/jpanasuk-netizen/tabby-tavern-stack](https://github.com/jpanasuk-netizen/tabby-tavern-stack) |
| **This HF model card** | [https://huggingface.co/jpanasuk/tabby-tavern-stack](https://huggingface.co/jpanasuk/tabby-tavern-stack) |
| **Lab tour Space** (static) | [https://huggingface.co/spaces/jpanasuk/tabby-tavern-stack](https://huggingface.co/spaces/jpanasuk/tabby-tavern-stack) |
| **Sell sheet Space** | [https://huggingface.co/spaces/jpanasuk/tabby-tavern-sell-sheet](https://huggingface.co/spaces/jpanasuk/tabby-tavern-sell-sheet) |
| **dockroot-mcp** (companion) | [https://huggingface.co/spaces/jpanasuk/dockroot-mcp](https://huggingface.co/spaces/jpanasuk/dockroot-mcp) |
| **Connectivity skill** | [https://huggingface.co/spaces/jpanasuk/local-ai-stack-connectivity](https://huggingface.co/spaces/jpanasuk/local-ai-stack-connectivity) |
| **Telemetry / benchmarks** | [https://github.com/jpanasuk-netizen/local_grid_suite](https://github.com/jpanasuk-netizen/local_grid_suite) |
| **Multi-agent prototype** | [https://github.com/jpanasuk-netizen/multi-agent-dungeon-crawler](https://github.com/jpanasuk-netizen/multi-agent-dungeon-crawler) |
| **Author** | [https://huggingface.co/jpanasuk](https://huggingface.co/jpanasuk) · [@jpanasuk-netizen](https://github.com/jpanasuk-netizen) |

The model card and the lab-tour Space share a slug and **different namespaces**. `/jpanasuk/tabby-tavern-stack` is this card. `/spaces/jpanasuk/tabby-tavern-stack` is the static tour.

> **Weights are not included.** You download EXL3 and/or GGUF models yourself.
> **Secrets are not included.** Copy examples and generate your own keys.
> **Character cards are included.** Import the PNGs under `cards/` into SillyTavern.

---

## Operator snapshot (2026-08-25) — GitHub was stale; this wins

On LightBringer the **Tabby compose is left down** so llama.cpp can own the 4070. That is a VRAM policy, not a rebrand.

| Fact | Detail |
| --- | --- |
| Tabby compose | Restored Tabby names/ports. All Tabby containers **Exited** (~17 h), `restart=no` |
| GPU owner | llama.cpp `qwen38-llama-server` on **:1234** (Taproot project — see below) |
| VRAM | **11450 / 12282 MiB** with llama resident. Xwayland ~3.6 GB when the desktop is up |
| Last call | Do **not** start TabbyAPI / Ollama GPU while llama is on the card. Two heavy engines stall CUDA instead of erroring. Do not kill grok / hermes / llama to “clean tavern.” |
| Operator desk | VS Code (snap + Windows Remote-WSL) drives the machine. VS Code is **not** a Tabby container. |

Full notes: [`DEVLOG.md`](DEVLOG.md) § 2026-08-25.

---

## Same machine, different stack (Taproot)

Linked so you do not absorb it. **Do not** `docker compose up` the qwen/llama service as a Tabby step — recreating it would bounce the live server.

- Compose project **`taproot`** at `~/taproot` (not this tree). Open WebUI **:3001**, `WEBUI_NAME=Taproot`, `OPENAI_API_BASE_URL=http://host.docker.internal:1234/v1`.
- Live engine: container name still **`qwen38-llama-server`** (yaml wants `taproot-qwen`; it was **not** recreated). Image `ghcr.io/ggml-org/llama.cpp:server-cuda`, Qwen3.5-9B UD-Q4_K_XL, `n_ctx` 262144, host **:1234**.
- Tabby’s old shared network was **removed** so the stacks cannot see each other by accident.
- Continue (VS Code) → `http://127.0.0.1:1234/v1`. Grok 1.0.5 at `~/.local/bin/grok`. Hermes v0.20.0 at `~/.hermes/hermes-agent`.
- `~/annie-scratch` is an Annie++ Python class tree. It is **not** this repo and is **not** Taproot.
- No Qwen3.5-9B tok/s is published here (not measured in this tree).

---

## Service ports (Tabby compose defaults)

| Compose service | Container name (default) | Host port | In-container | Role |
| --------------- | ------------------------------ | ------------ | ------------ | ------------------------------- |
| `sillytavern` | `tabby-tavern-sillytavern-1` | **8000** | 8000 | Chat / character frontend |
| `open-webui` | `tabby-tavern-open-webui-1` | **3000** | 8080 | General LLM workspace |
| `tabbyapi` | `tabby-tavern-tabbyapi-1` | **5000** | 5000 | EXL3 high-performance inference |
| `ollama` | `tabby-tavern-ollama-1` | **11435** | 11434 | GGUF model backend (host remap) |
| `searxng` | `tabby-tavern-searxng-1` | **8080** | 8080 | Private metasearch |
| `mcpo` | `tabby-tavern-mcpo-1` | **8001** | 8000 | MCP → OpenAPI proxy |

Ollama is published on **11435** so a host-level `ollama serve` on 11434 does not collide. Open WebUI still reaches it on the compose network at `http://ollama:11434`.

Open WebUI is wired to **both** backends:

```yaml
OLLAMA_BASE_URL=http://ollama:11434
OPENAI_API_BASE_URL=http://tabbyapi:5000/v1
OPENAI_API_KEY=${TABBYAPI_API_KEY}
ENABLE_OPENAI_API=true
ENABLE_RAG_WEB_SEARCH=true
RAG_WEB_SEARCH_ENGINE=searxng
SEARXNG_QUERY_URL=http://searxng:8080/search?q=<query>
```

All Tabby services share the bridge network `ai-network`. That network is **not** shared with Taproot.

---

## System requirements

### Host

* **OS:** Linux native, or Windows **WSL2** with Docker Desktop / Docker Engine
* **GPU:** NVIDIA GPU with recent drivers (lab used RTX 4070)
* **Docker:** Docker Engine + **Compose plugin** (`docker compose version`)
* **NVIDIA Container Toolkit** (required for GPU passthrough into containers)
* **Disk:** room for Docker images **plus** model weights (EXL3 8B class is often tens of GB; GGUF varies by quant)
* **RAM / VRAM:** 8B-class EXL3 fits a 12 GB class card with headroom when KV/cache is tuned; larger models need more VRAM. **One heavy GPU owner at a time** on 12 GB.

### One-time NVIDIA Container Toolkit check

```bash
nvidia-smi

docker run --rm --gpus all nvidia/cuda:12.4.1-base-ubuntu22.04 nvidia-smi
```

If `nvidia-smi` works on the host but fails in Docker, fix the toolkit / Docker daemon GPU runtime **before** bringing the stack up.

### Optional host tools

```bash
pipx install "huggingface_hub[cli]"
# or: python3 -m venv .venv && . .venv/bin/activate && pip install -U "huggingface_hub[cli]"
```

---

## Cold start (stranger path — Tabby compose only)

Prefer cloning **GitHub** for day-to-day work. This HF repo is the public **model card** + sanitized mirror of the same layout.

If llama.cpp already owns the 4070 on this machine, **do not** `docker compose up` TabbyAPI/Ollama until you have freed VRAM. The commands below assume Tabby is allowed to take the GPU.

### 0) Clone

```bash
git clone https://github.com/jpanasuk-netizen/tabby-tavern-stack.git
cd tabby-tavern-stack
```

Alternate (HF **model** mirror — same public layout, may lag GitHub):

```bash
git lfs install   # only if you later pull large assets; weights still not shipped
git clone https://huggingface.co/jpanasuk/tabby-tavern-stack
cd tabby-tavern-stack
```

### 1) Build the TabbyAPI image used by compose

Compose expects this **exact** local tag:

```bash
docker build -f Dockerfile.tabby -t local/tabbyapi:exl3-fixed .
```

`Dockerfile.tabby` is the WSL2-tested image: `ghcr.io/theroyallab/tabbyapi:latest` plus build deps **and** a `libcuda.so` symlink so ExLlamaV3/Triton can link inside WSL2.

### 2A) Download an EXL3 model for TabbyAPI

Weights go under `tabby_models/` (gitignored). Compose mounts:

```text
./tabby_models  →  /app/models   (inside tabbyapi)
```

TabbyAPI `model_name` is a **directory name under that mount**.

```bash
mkdir -p tabby_models

huggingface-cli download turboderp/Llama-3.1-8B-Instruct-exl3 \
  --revision 6.0bpw \
  --local-dir tabby_models/Llama-3.1-8B-Instruct-exl3-6.0bpw

ls -la tabby_models/Llama-3.1-8B-Instruct-exl3-6.0bpw | head
```

**EXL2 will not load.** Current TabbyAPI dropped the ExLlamaV2 backend. Use EXL3 quants only.

### 2B) Configure TabbyAPI (required before first launch)

```bash
cp -n tabby_config/config.example.yml tabby_config/config.yml
```

Generate real keys and paste them in:

```bash
python3 -c "import secrets; print('admin_key:', secrets.token_hex(32)); print('api_key:  ', secrets.token_hex(32))"
```

Set `model_name` to the folder you downloaded. For a 12 GB card the lab uses:

```yaml
model:
  model_dir: models
  model_name: Llama-3.1-8B-Instruct-exl3-6.0bpw
  max_seq_len: 8192
  cache_size: 8192
  cache_8bit: true
```

Compose always mounts:

```text
./tabby_config/config.yml  →  /app/config.yml
```

Put the same `api_key` in:

* `open-webui` `OPENAI_API_KEY`
* `mcpo/config.json` `TABBYAPI_KEY`
* SillyTavern API settings

### 2C) Ollama / GGUF path (secondary backend)

After the stack is up:

```bash
docker exec -it tabby-tavern-ollama-1 ollama pull llama3.1:8b
docker exec -it tabby-tavern-ollama-1 ollama list
docker exec -it tabby-tavern-ollama-1 ollama run llama3.1:8b "Say hello in one sentence."
```

You can run **TabbyAPI (EXL3)** and **Ollama (GGUF)** together; on a 12 GB card load one heavy model at a time unless you know your headroom. Lab measurement: ~8 GB VRAM for Llama-3.1-8B EXL3 6.0bpw + 8-bit cache, ~4 GB left for a small GGUF. **Do not** add llama.cpp as a third GPU tenant.

### 3) Frontend / search secrets (placeholders only)

**SillyTavern** (`sillytavern_config/config.yaml`):

* Default listen port **8000**
* `browserLaunch.enabled: false` (no browser inside Docker)
* `basicAuthMode: true` — ST refuses to start on `0.0.0.0` without auth
* Replace:

```yaml
basicAuthUser:
  username: "YOUR_ST_USERNAME_HERE"
  password: "YOUR_ST_PASSWORD_HERE"
```

**SearXNG** (`searxng_config/settings.yml`):

```yaml
use_default_settings: true
server:
  secret_key: "YOUR_SEARXNG_SECRET_KEY_HERE"
  image_proxy: true
search:
  formats:
    - html
    - json
```

JSON format is required for MCPO `searxng_search` and Open WebUI RAG.

### 4) Character cards (SillyTavern)

This release ships Tavern **character cards** under `cards/`:

| File | What it is |
| --------------------------------------------- | -------------------------------- |
| `cards/default_Seraphina.png` | SillyTavern PNG character card (embedded spec) |
| `cards/Seraphina/*.png` | Expression sprites used by the card |
| `cards/README.md` | Import notes |

**Use the cards:**

1. Start SillyTavern → http://localhost:8000
2. Characters → Import → pick `cards/default_Seraphina.png`
3. Copy `cards/Seraphina/` into SillyTavern's character expressions folder if the importer does not pull sprites automatically (`sillytavern_data/default-user/characters/Seraphina/`)

Do not commit chats, `secrets.json`, or live API keys from a running data directory.

### 5) Launch

```bash
docker compose up -d
docker compose ps
```

Or:

```bash
chmod +x start-stack.sh load-model.sh
./start-stack.sh
```

`start-stack.sh` only orchestrates **this** compose file. It is not a Taproot / llama.cpp launcher.

### 6) Health checks (every service)

```bash
docker compose ps
docker compose logs --tail=80 tabbyapi
docker compose logs --tail=40 ollama
docker compose logs --tail=40 sillytavern
docker compose logs --tail=40 open-webui
docker compose logs --tail=40 searxng
docker compose logs --tail=40 mcpo

curl -sS -o /dev/null -w "sillytavern  %{http_code}\n" http://127.0.0.1:8000/ || true
curl -sS -o /dev/null -w "open-webui   %{http_code}\n" http://127.0.0.1:3000/ || true
curl -sS -o /dev/null -w "tabbyapi     %{http_code}\n" http://127.0.0.1:5000/ || true
curl -sS -o /dev/null -w "ollama       %{http_code}\n" http://127.0.0.1:11435/ || true
curl -sS -o /dev/null -w "searxng      %{http_code}\n" http://127.0.0.1:8080/ || true
curl -sS -o /dev/null -w "mcpo         %{http_code}\n" http://127.0.0.1:8001/docs || true

docker exec -it tabby-tavern-tabbyapi-1 nvidia-smi || true
```

Browser targets (Tabby):

* SillyTavern → http://localhost:8000
* Open WebUI → http://localhost:3000
* TabbyAPI → http://localhost:5000
* Ollama (host) → http://localhost:11435
* SearXNG → http://localhost:8080
* MCPO Swagger → http://localhost:8001/docs

### 7) Point SillyTavern at TabbyAPI

In SillyTavern API settings:

* API type: **OpenAI-compatible** / TabbyAPI
* Endpoint: `http://tabbyapi:5000/v1` from another container, or `http://127.0.0.1:5000/v1` from the host
* API key: the `api_key` in `tabby_config/config.yml`

If ST cannot reach TabbyAPI, check:

1. Both containers on `ai-network`
2. Keys match
3. TabbyAPI finished loading the EXL3 model (`docker compose logs -f tabbyapi`)

### 8) Switch / reload TabbyAPI model

```bash
# Edit model_name in tabby_config/config.yml to another folder under tabby_models/
docker compose restart tabbyapi
docker compose logs -f tabbyapi
```

---

## Why the YAML actually works (lab pitfalls)

These are the real keys from the **example** files. Never commit live secrets.

| Pitfall | What this tree ships |
| --- | --- |
| EXL2 dropped upstream | EXL3 only: `model_name: Llama-3.1-8B-Instruct-exl3-6.0bpw`, `model_dir: models` |
| 12 GB KV blow-up | `max_seq_len: 8192`, `cache_size: 8192`, `cache_8bit: true` |
| TabbyAPI ignoring host YAML | Compose mounts `./tabby_config/config.yml` → `/app/config.yml` |
| WSL2 `-lcuda` | `Dockerfile.tabby` symlinks `cuda-12.8/compat/libcuda.so`; `shm_size: 16g`; CUDA device order; flash-attn / KV flags |
| Open WebUI only saw Ollama | `OPENAI_API_BASE_URL=http://tabbyapi:5000/v1` **and** `OLLAMA_BASE_URL=http://ollama:11434` |
| Host Ollama on 11434 | Publish `11435:11434` |
| SillyTavern in Docker | `browserLaunch.enabled: false`; `basicAuthMode: true` (ST refuses `0.0.0.0` without auth) |
| MCPO / RAG search empty | SearXNG `search.formats`: **html and json** |
| MCPO crash on boot | FastMCP `mcp-servers/server.py`, seven tools under `/host-master/`, python `/app/.venv/bin/python3`; empty `mcpServers` crashes MCPO |
| NVIDIA toolkit apt | `deb …/noble main` is malformed; flat `amd64 /` repo line works |
| Character chat as an afterthought | PNG cards in `cards/` are first-class |

Connection rule (companion Space, not duplicated here): path is always `/v1`; inside Docker the host is the **service name**, not `localhost`. See [local-ai-stack-connectivity](https://huggingface.co/spaces/jpanasuk/local-ai-stack-connectivity).

---

## MCPO (MCP → OpenAPI)

MCPO (`ghcr.io/open-webui/mcpo:main`) launches MCP servers as subprocesses and exposes their tools as OpenAPI HTTP endpoints.

`mcp-servers/server.py` is a **FastMCP** server (not raw JSON-RPC) with 7 tools:

| Tool | Description |
| ------------------- | ----------------------------------- |
| `list_tabbyapi_models` | List loaded EXL3 models in TabbyAPI |
| `tabbyapi_chat` | Chat with the TabbyAPI EXL3 model |
| `list_ollama_models` | List GGUF models in Ollama |
| `ollama_pull_model` | Pull a model into Ollama |
| `ollama_chat` | Chat with an Ollama model |
| `get_stack_status` | Health check all services |
| `searxng_search` | Web search via SearXNG (JSON) |

Config notes:

* `mcpo/config.json` must call `/app/.venv/bin/python3` (MCPO image venv has `mcp`)
* Env: `TABBYAPI_URL`, `OLLAMA_URL`, `TABBYAPI_KEY` (placeholder in public tree)
* Tools are served under `/host-master/` (server name in config)
* Empty `"mcpServers": {}` **crashes** MCPO — keep at least one entry
* Set `--api-key` in compose (public tree uses `REPLACE_WITH_YOUR_MCPO_API_KEY`)

A second server, `mcp-servers/tavern_mcp.py`, is the lab connectivity toolkit (`status`, `self_check`, `wire`, `models`, `chat`). Wire it only if you also ship `discover.py` next to it.

**dockroot-mcp** is a companion (read-only docker vision), not a core Tabby service. On the live box it is a local helper under `~/dockroot`, not a running container. Space: [jpanasuk/dockroot-mcp](https://huggingface.co/spaces/jpanasuk/dockroot-mcp).

---

## GPU / compose tuning (what the lab actually ships)

| Setting | Value | Why |
| --------------------------------------- | ----------------------- | ---------------------------------------- |
| `deploy.resources.reservations.devices` | NVIDIA GPU `count: all` | Passthrough |
| `shm_size` | **16g** | Avoid shared-memory OOM during load/attn |
| `CUDA_VISIBLE_DEVICES` | `0` | Pin first GPU |
| `CUDA_DEVICE_ORDER` | `PCI_BUS_ID` | Stable device ordering |
| `PYTORCH_CUDA_ALLOC_CONF` | `max_split_size_mb:128` | Allocator fragmentation control |
| `EXLLAMA_GPU_LAYERS` | `999` | Prefer full GPU offload |
| `EXLLAMA_KV_CACHE` | `q8_0` | KV cache quant tradeoff |
| `EXLLAMA_FLASH_ATTENTION` | `1` | Flash-attn path when available |
| `OLLAMA_FLASH_ATTENTION` | `1` | Ollama flash-attn |
| `OLLAMA_KV_CACHE_TYPE` | `q8_0` | Ollama KV quant |
| TabbyAPI `cache_8bit` | `true` | Halves KV VRAM on 12 GB cards |

If you OOM: lower `max_seq_len` / `cache_size`, use a smaller bpw EXL3, or stop Ollama models while TabbyAPI holds a large model. If llama.cpp is already resident, **leave Tabby GPU services down**.

---

## Repository structure

```text
tabby-tavern-stack/
├── docker-compose.yml              # Tabby orchestration (6 services)
├── docker-compose.starter.yml      # optional coding-tools overlay
├── Dockerfile / Dockerfile.tabby   # TabbyAPI image (WSL2 libcuda fix)
├── start-stack.sh
├── load-model.sh
├── cards/                          # SillyTavern character cards (PNG)
├── mcpo/config.json                # MCPO server map (placeholders)
├── mcp-servers/server.py           # FastMCP stack tools
├── tabby_config/config.example.yml
├── sillytavern_config/config.yaml
├── searxng_config/settings.yml
├── tabby_models/                   # EXL3 weights (gitignored contents)
├── SECURITY.md
├── DEVLOG.md
├── LICENSE
└── docs/spaces/                    # sell sheet + Space HTML (shared CSS)
```

Compose service names (authoritative):

`tabbyapi` · `sillytavern` · `ollama` · `open-webui` · `searxng` · `mcpo`

---

## Environment & secrets guidance

| Secret / file | Where | Rule |
| -------------------------------- | ---------------------------- | ------------------------------------------- |
| TabbyAPI `admin_key` / `api_key` | `tabby_config/config.yml` | Generate yourself; never commit live values |
| Open WebUI `OPENAI_API_KEY` | compose env | Same value as TabbyAPI `api_key` |
| MCPO `--api-key` / `TABBYAPI_KEY` | compose + `mcpo/config.json` | Placeholders in public tree |
| SillyTavern basic auth | `sillytavern_config/config.yaml` | Replace `YOUR_ST_*` placeholders |
| SearXNG `secret_key` | `searxng_config/settings.yml` | Replace placeholder |
| Open WebUI DB | `openwebui_data/` | gitignored |
| Ollama keys/models | host `~/.ollama` or `ollama_data/` | gitignored |

**Private-lab defaults are intentional.** This is not hardened multi-tenant hosting.

Before any LAN/WAN exposure:

1. Replace every placeholder credential
2. Prefer binding host ports to `127.0.0.1`
3. Put a reverse proxy + TLS in front if you leave the machine
4. Read [`SECURITY.md`](SECURITY.md)

Older public revisions of this mirror contained lab convenience keys (including a TabbyAPI key in `mcpo/config.json`). **Treat any key you ever saw in a public file as burned** and rotate it.

---

## Common failure modes

| Symptom | Likely cause | Fix |
| --------------------------------------------- | ------------------------------------------ | ----------------------------------------------------------------- |
| `local/tabbyapi:exl3-fixed` start fails | Image never built | `docker build -f Dockerfile.tabby -t local/tabbyapi:exl3-fixed .` |
| TabbyAPI: `exl2` backend no longer supported | Pointed at an EXL2 directory | Download an EXL3 revision instead |
| `/usr/bin/ld: cannot find -lcuda` | WSL2 CUDA libs not on linker path | Use the patched `Dockerfile.tabby` in this repo |
| TabbyAPI cannot find model | `model_name` ≠ folder under `tabby_models/` | Align names; confirm mount |
| CUDA / GPU errors in container | Toolkit missing | Fix NVIDIA Container Toolkit first |
| CUDA “stalls forever” bringing Tabby up | llama.cpp already on the 4070 | Leave Tabby GPU down; do not bounce llama to free tavern |
| OOM during load | Model + KV + dual backends too large | Smaller quant; `cache_8bit`; unload Ollama |
| ST cannot talk to TabbyAPI | Auth/network mismatch | Same network; matching API key; wait for load |
| Open WebUI shows no models | Ollama empty or URL wrong | `ollama pull`; confirm `OLLAMA_BASE_URL` |
| Host port 11434 in use | Host Ollama already running | Keep compose map `11435:11434` |
| SearXNG 500s / no JSON | Placeholder secret or HTML-only formats | Set secret; add `json` to `search.formats` |
| MCPO crash: no mcpServers | Empty config | Keep at least one server entry |
| SillyTavern refuses to start | Listen 0.0.0.0 with no auth | Keep `basicAuthMode: true` |
| NVIDIA apt `Malformed entry` | Wrong toolkit repo line | See WSL2 notes below |

---

## Measured lab results (defensible only)

Numbers from checked-in sample telemetry in [`local_grid_suite`](https://github.com/jpanasuk-netizen/local_grid_suite) (`benchmarks/sample_hardware_runs.json`) plus the Tabby 24/24 compose pass. **Single-box lab runs — not a product SLA.**

| Stage | Model | Decode tok/s |
| ---------- | ----------------- | --------------- |
| Baseline | `qwen3:8b` | **1.39** |
| GPU-routed | `qwen-gpu:latest` | **29.7 – 39.3** |
| Stabilized | `qwen-gpu:latest` | **37.47** |

→ **~27× decode uplift** on that run series after GPU routing / tuning.

Warm stream suite on `qwen3:8b`: **~76 tok/s** (400-token runs).

WSL2 EXL3 chat (Llama-3.1-8B-Instruct 6.0bpw, RTX 4070): **~53 tok/s** processing in the verified 24/24 check pass.

Qwen3.5-9B llama.cpp tok/s is **not** published (not measured here). Re-measure on your hardware. Do not advertise these as guaranteed throughput.

---

## Engineering notes

See [`DEVLOG.md`](DEVLOG.md) for the build log:

* Compose consolidation (TabbyAPI + ST + Open WebUI + Ollama + SearXNG + MCPO)
* EXL3 adoption; EXL2 dropped upstream
* GPU env tuning (`shm_size`, flash-attn / KV cache, `cache_8bit`)
* Container-to-TabbyAPI auth / whitelist fixes
* WSL2 NVIDIA toolkit + `libcuda.so` linker fix
* MCPO FastMCP server (7 tools verified)
* Character cards shipped in `cards/`
* 2026-08-25 operator path: Tabby left down; Taproot llama.cpp neighbor; VS Code as the desk

---

## Optional coding starter overlay

`docker-compose.starter.yml` is an **optional** overlay (browser IDE, vector DBs, n8n, extra chat UIs). It is **not** required for the core six-service lab. It expects the core stack network `ai-network` to already exist. Change every placeholder password before `up`.

```bash
docker compose up -d
docker compose -f docker-compose.starter.yml up -d
```

The overlay is not the live operator desk. VS Code on LightBringer is the host snap / Remote-WSL install, not `starter-code-server`.

---

## WSL2 field notes — fresh-install lessons (Aug 2026)

A from-scratch rebuild on a clean WSL2 Ubuntu environment (same RTX 4070). Additive to the cold-start guide.

### EXL2 vs EXL3 — TabbyAPI dropped EXL2 support

```
ValueError: Models quantized with 'exl2' require the exllamav2 backend, which is no longer supported. Please use an exl3 or unquantized model.
```

Use EXL3 quants only (`turboderp/Llama-3.1-8B-Instruct-exl3` branches 2.0–8.0 bpw).

### NVIDIA Container Toolkit repo URL

The `deb .../noble main` line is **wrong** for this repo (apt: `Malformed entry (Component)`). NVIDIA uses a flat structure:

```bash
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey \
  | sudo gpg --dearmor --yes -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg

echo 'deb [arch=amd64 signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://nvidia.github.io/libnvidia-container/stable/deb/amd64 /' \
  | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```

### libcuda.so not found inside TabbyAPI on WSL2

Even with `torch.cuda.is_available() == True`, model load can fail with `cannot find -lcuda`. The patched Dockerfile in this repo creates:

```dockerfile
RUN ln -sf /usr/local/cuda-12.8/compat/libcuda.so /usr/lib/x86_64-linux-gnu/libcuda.so && ldconfig
```

Triton “not supported, roll back to CPU” warnings are **cosmetic** — exllamav3 uses its own CUDA kernels.

### Port conflict when host Ollama is already running

Compose maps `11435:11434`. Open WebUI still uses `http://ollama:11434` internally.

### Verified working state (compose path)

After the v2.0.0 tree: 24/24 checks passing on the lab box — six containers, EXL3 chat, Ollama `llama3.1:8b`, Open WebUI dual backend, SillyTavern with cards, SearXNG JSON, MCPO 7 tools, ~8 GB / 12 GB VRAM **when Tabby owns the GPU**.

---

## Related spine

| Project | Link |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| Stack (this card) | https://huggingface.co/jpanasuk/tabby-tavern-stack |
| Lab tour Space | https://huggingface.co/spaces/jpanasuk/tabby-tavern-stack |
| Stack (GitHub) | https://github.com/jpanasuk-netizen/tabby-tavern-stack |
| Sell sheet Space | https://huggingface.co/spaces/jpanasuk/tabby-tavern-sell-sheet |
| dockroot-mcp | https://huggingface.co/spaces/jpanasuk/dockroot-mcp |
| Connectivity skill | https://huggingface.co/spaces/jpanasuk/local-ai-stack-connectivity |
| Local Grid Suite | https://github.com/jpanasuk-netizen/local_grid_suite |
| Multi-agent prototype | https://github.com/jpanasuk-netizen/multi-agent-dungeon-crawler |
| Collection | https://huggingface.co/collections/jpanasuk/independent-ai-lab-spine-6a727803ed9c6d16164f5130 |

---

## Author

**Jeremy Panasuk** — enterprise data / platform background; **Aug 2024–present** independent local-AI systems year (private Docker LLM lab, decode telemetry, multi-agent prototypes).

* GitHub: [@jpanasuk-netizen](https://github.com/jpanasuk-netizen)
* Hugging Face: [jpanasuk](https://huggingface.co/jpanasuk)
* LinkedIn: [jeremy-p-34203322](https://www.linkedin.com/in/jeremy-p-34203322)

## License

MIT
