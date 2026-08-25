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
- llama-cpp
- vscode
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

**Basically, you can learn AI Infrastructure in 21 days too.**

**Tabby** is local AI you can actually use. **Taproot** is the next step: a local coding desk, no internet required — llama.cpp 262k, VS Code/Continue, Grok, Hermes.

One repo story: `tabby-tavern-stack`. One Space family. Both layers, one lab. Private IaaS on a workstation you own — production-*shaped*, not SaaS. The page teaches by showing the live stack. Proof is [`DEVLOG.md`](DEVLOG.md) **Week 4** (clean WSL2 rebuild on the same 4070) plus **v2.0 packaging** (2026-08-25). Hardware: **LightBringer**, WSL2 Ubuntu, **NVIDIA RTX 4070 12 GB**.

| Layer | What runs |
| --- | --- |
| **Tabby** — local AI you can use | **TabbyAPI** `:5000` EXL3 + **SillyTavern** `:8000` + shipped **character cards** + **Open WebUI** `:3000` (Ollama **and** TabbyAPI `/v1`) + **Ollama** `:11435` + **SearXNG** `:8080` + **MCPO** `:8001` |
| **Taproot** — local coding desk | **llama.cpp** `:1234` Qwen 9B `n_ctx` 262144 + Open WebUI `:3001` (`WEBUI_NAME=Taproot`) + Windows VS Code 1.134.0 + Remote-WSL + **Continue 2.0** → `:1234/v1` + **Grok** 1.0.5 + **Hermes** v0.20.0 |
| Docker vision | `~/dockroot` helper + [dockroot-mcp](https://huggingface.co/spaces/jpanasuk/dockroot-mcp) Space |

This GitHub tree ships the Tabby EXL3 compose (six services, YAML, cards, MCPO) and the lab card for the whole box. Taproot’s llama.cpp / Open WebUI `:3001` compose lives on the machine at `~/taproot` — same lab, same docs, not a second repo. Tabby compose **service names and ports stay Tabby** (`8000` / `3000` / `5000` / `11435` / `8080` / `8001`). Class work in `~/annie-scratch` stays out of this tree.

| Surface | URL |
| -------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| **GitHub (source of truth)** | [https://github.com/jpanasuk-netizen/tabby-tavern-stack](https://github.com/jpanasuk-netizen/tabby-tavern-stack) |
| **This HF model card** | [https://huggingface.co/jpanasuk/tabby-tavern-stack](https://huggingface.co/jpanasuk/tabby-tavern-stack) |
| **Lab tour Space** (static) | [https://huggingface.co/spaces/jpanasuk/tabby-tavern-stack](https://huggingface.co/spaces/jpanasuk/tabby-tavern-stack) |
| **Sell sheet Space** | [https://huggingface.co/spaces/jpanasuk/tabby-tavern-sell-sheet](https://huggingface.co/spaces/jpanasuk/tabby-tavern-sell-sheet) |
| **dockroot-mcp** | [https://huggingface.co/spaces/jpanasuk/dockroot-mcp](https://huggingface.co/spaces/jpanasuk/dockroot-mcp) |
| **Connectivity skill** (44 recipes) | [https://huggingface.co/spaces/jpanasuk/local-ai-stack-connectivity](https://huggingface.co/spaces/jpanasuk/local-ai-stack-connectivity) |
| **Telemetry / benchmarks** | [https://github.com/jpanasuk-netizen/local_grid_suite](https://github.com/jpanasuk-netizen/local_grid_suite) |
| **Multi-agent prototype** | [https://github.com/jpanasuk-netizen/multi-agent-dungeon-crawler](https://github.com/jpanasuk-netizen/multi-agent-dungeon-crawler) |
| **Author** | [https://huggingface.co/jpanasuk](https://huggingface.co/jpanasuk) · [@jpanasuk-netizen](https://github.com/jpanasuk-netizen) |

The model card and the lab-tour Space share a slug in **different namespaces**. `/jpanasuk/tabby-tavern-stack` is this card. `/spaces/jpanasuk/tabby-tavern-stack` is the static tour.

> **Weights are not included.** You download EXL3, GGUF, and GGUF-UD packs yourself.
> **Secrets are not included.** Copy examples and generate your own keys.
> **Character cards are included.** Import the PNGs under `cards/` into SillyTavern.
> **Class work is not included.** `~/annie-scratch` is an Annie++ Python class tree. Mentioned only so it is not confused with the lab.

---

## Live lab (2026-08-25) — this snapshot wins

One GPU. Two heavy engines will **stall CUDA** instead of erroring. Today llama.cpp owns the card; the Tabby GPU path is parked.

| Fact | Detail |
| --- | --- |
| GPU owner | llama.cpp container **`qwen38-llama-server`** on **:1234** — healthy; **do not bounce / recreate it** |
| VRAM | **11450 / 12282 MiB** with llama resident. Xwayland ~3.6 GB when the desktop is up |
| Tabby compose | Names/ports restored. All Tabby GPU containers **Exited** (~17 h), `restart=no` |
| Last call | Do **not** start TabbyAPI / Ollama while llama is on the 4070. Do not kill grok / hermes / llama to “clean tavern” |
| Desk | Continue 2.0 → `http://127.0.0.1:1234/v1`. Grok 1.0.5. Hermes v0.20.0 |

Full notes: [`DEVLOG.md`](DEVLOG.md) § 2026-08-25.

---

## Layer A — Tabby: local AI you can actually use

Six services on bridge `ai-network`. **Do not rename these ports or service names.**

| Compose service | Container name (default) | Host port | In-container | Role |
| --------------- | ------------------------------ | ------------ | ------------ | ------------------------------- |
| `sillytavern` | `tabby-tavern-sillytavern-1` | **8000** | 8000 | Character frontend |
| `open-webui` | `tabby-tavern-open-webui-1` | **3000** | 8080 | EXL3 + GGUF workspace |
| `tabbyapi` | `tabby-tavern-tabbyapi-1` | **5000** | 5000 | EXL3 / ExLlamaV3 |
| `ollama` | `tabby-tavern-ollama-1` | **11435** | 11434 | GGUF (host remap) |
| `searxng` | `tabby-tavern-searxng-1` | **8080** | 8080 | Private metasearch |
| `mcpo` | `tabby-tavern-mcpo-1` | **8001** | 8000 | MCP → OpenAPI |

Ollama is published on **11435** so a host-level `ollama serve` on 11434 does not collide. Open WebUI still reaches it at `http://ollama:11434` on `ai-network`.

```yaml
OLLAMA_BASE_URL=http://ollama:11434
OPENAI_API_BASE_URL=http://tabbyapi:5000/v1
OPENAI_API_KEY=${TABBYAPI_API_KEY}
ENABLE_OPENAI_API=true
ENABLE_RAG_WEB_SEARCH=true
RAG_WEB_SEARCH_ENGINE=searxng
SEARXNG_QUERY_URL=http://searxng:8080/search?q=<query>
```

`tabby-tavern_ai-network` was **removed** from the llama.cpp side so Tabby and Taproot cannot both grab the 4070. Same lab; they do not share a Docker network.

---

## Layer B — Taproot: local coding desk, no internet (`~/taproot`)

The next step after Tabby. Compose project name **`taproot`**, file `/home/jpanasuk/taproot/docker-compose.yml`. Not copied into this git tree; do not paste it over `docker-compose.yml` here.

| Piece | Live fact | Why that YAML exists |
| --- | --- | --- |
| llama.cpp server | Host **`0.0.0.0:1234→8080`**, image `ghcr.io/ggml-org/llama.cpp:server-cuda`, Qwen3.5-9B **UD-Q4_K_XL**, `n_ctx` **262144** | 262k context on a 12 GB card needs the llama.cpp server path, not TabbyAPI EXL3 8k |
| Container name | Still **`qwen38-llama-server`**. YAML wants `taproot-qwen`. **Not recreated.** | Recreating would bounce the live server. Leave it. |
| Open WebUI | **`taproot-webui` :3001**, `WEBUI_NAME=Taproot`, data `/home/jpanasuk/taproot/open-webui-data` | Separate from Tabby Open WebUI **:3000** so the two UIs do not share a DB |
| Engine URL | `OPENAI_API_BASE_URL=http://host.docker.internal:1234/v1` | WebUI is in Docker; llama is published on the host. `localhost` inside the container is the wrong box. Path is `/v1`, not `/v1/chat/completions` |
| Lineage | `/home/jpanasuk/qwen38-agent/docker-compose.yml` (27B then 9B 262k) | Live llama started from this lineage before the taproot project name |

**Do not** `docker compose up` that llama service from this Tabby repo. It is already up.

No Qwen3.5-9B tok/s is published (not measured in this tree).

---

## Layer C — the Taproot desk (VS Code, Continue, Grok, Hermes)

| Tool | Where | Why |
| --- | --- | --- |
| Windows VS Code **1.134.0** + Remote-WSL **0.104.3** | `/home/jpanasuk/taproot` | Local coding desk for the 262k engine |
| Continue **2.0** | `~/.continue/config.yaml` → `http://127.0.0.1:1234/v1` Qwen3.5-9B | Continue runs on the host, so the host loopback port, not `host.docker.internal` |
| Grok Build **1.0.5** | `~/.local/bin/grok` | Host CLI for the lab |
| Hermes **v0.20.0** | `~/.hermes/hermes-agent` | Agent runtime; loads the connectivity skill |
| Linux snap VS Code **1.134.0** | `~/annie-scratch` | **Annie++ Python class only.** Not the lab. Not this repo. Do not copy class files here. |

VS Code is the Taproot desk, not a Tabby container. `docker-compose.starter.yml`’s browser IDE is an optional overlay, not how LightBringer is driven.

---

## Layer D — MCP and connectivity

- **MCPO** in Tabby compose: FastMCP `mcp-servers/server.py`, seven tools under `/host-master/`, python `/app/.venv/bin/python3`. Empty `mcpServers` crashes MCPO.
- **Dockroot** on the box: `~/dockroot` (`tavern.sh`, `tavern_mcp.py`, `discover.py`, `recipes.py`) — local recipe helper, **not** running as a container right now. Space: [dockroot-mcp](https://huggingface.co/spaces/jpanasuk/dockroot-mcp) (read-only docker vision).
- **Connection rule** + 44 recipes: [local-ai-stack-connectivity](https://huggingface.co/spaces/jpanasuk/local-ai-stack-connectivity). Path is always `/v1`. Inside Docker, host is the **service name**, not `localhost`. Continue on the host uses `127.0.0.1:1234/v1`. Taproot WebUI uses `host.docker.internal:1234/v1`.

---

## Custom YAML — why each change exists

Public example keys only. Never commit live secrets.

### TabbyAPI (`tabby_config/config.example.yml`)

```yaml
model:
  model_dir: models
  model_name: Llama-3.1-8B-Instruct-exl3-6.0bpw
  max_seq_len: 8192
  cache_size: 8192
  cache_8bit: true
```

| Change | Why |
| --- | --- |
| EXL3 directory name, not EXL2 | Current TabbyAPI dropped ExLlamaV2. EXL2 crashes on load. |
| `model_dir: models` + compose mount `./tabby_models → /app/models` | `model_name` is a folder under that mount |
| Compose `./tabby_config/config.yml → /app/config.yml` | Otherwise TabbyAPI never sees the host YAML |
| `cache_8bit` + 8192 seq/cache | 12 GB card: ~8 GB for 6.0bpw EXL3, ~4 GB left |
| Generated `api_key` / `admin_key` | Same key in Open WebUI, MCPO, SillyTavern |

`Dockerfile.tabby` also `ln -sf /usr/local/cuda-12.8/compat/libcuda.so` so Triton/exllamav3 can `-lcuda` on WSL2. `shm_size: 16g`, CUDA device order, flash-attn / KV flags.

### Open WebUI `:3000` (Tabby compose)

Dual backend so the UI can use EXL3 **and** GGUF. `OLLAMA_BASE_URL=http://ollama:11434` **and** `OPENAI_API_BASE_URL=http://tabbyapi:5000/v1`.

### Ollama

Host map `11435:11434` because host `ollama serve` already owns 11434. In-network name stays `ollama:11434`.

### SillyTavern (`sillytavern_config/config.yaml`)

`browserLaunch.enabled: false` (no browser inside Docker). `basicAuthMode: true` — ST **refuses** `0.0.0.0` without auth. Cards under `cards/` are first-class.

### SearXNG (`searxng_config/settings.yml`)

`search.formats`: **html and json**. JSON is required for MCPO `searxng_search` and Open WebUI RAG. HTML-only was the default and starved both.

### MCPO (`mcpo/config.json`)

`command: /app/.venv/bin/python3` (that venv has `mcp`). Tools under `/host-master/`. Empty `mcpServers: {}` crashes the proxy.

### NVIDIA Container Toolkit

`deb …/noble main` is a **malformed** apt line. Flat `amd64 /` repo line works.

### Taproot compose + Continue

| Change | Why |
| --- | --- |
| `OPENAI_API_BASE_URL=http://host.docker.internal:1234/v1` | WebUI container → host-published llama |
| Continue `http://127.0.0.1:1234/v1` | Continue is a host process |
| Separate `:3001` + `WEBUI_NAME=Taproot` + own data dir | Do not smash Tabby Open WebUI `:3000` chats |
| Networks not shared | Two GPU engines on one 4070 must not discover each other and both allocate |

---

## System requirements

### Host

* **OS:** Linux native, or Windows **WSL2** with Docker Desktop / Docker Engine
* **GPU:** NVIDIA GPU with recent drivers (lab used RTX 4070)
* **Docker:** Docker Engine + **Compose plugin** (`docker compose version`)
* **NVIDIA Container Toolkit** (required for GPU passthrough into containers)
* **Disk:** room for Docker images **plus** model weights (EXL3 8B class is often tens of GB; GGUF / UD-Q4_K_XL varies)
* **RAM / VRAM:** **one heavy GPU owner at a time** on 12 GB

### One-time NVIDIA Container Toolkit check

```bash
nvidia-smi

docker run --rm --gpus all nvidia/cuda:12.4.1-base-ubuntu22.04 nvidia-smi
```

If `nvidia-smi` works on the host but fails in Docker, fix the toolkit / Docker daemon GPU runtime **before** bringing GPU containers up.

### Optional host tools

```bash
pipx install "huggingface_hub[cli]"
# or: python3 -m venv .venv && . .venv/bin/activate && pip install -U "huggingface_hub[cli]"
```

---

## Cold start (Tabby compose in this repo)

Prefer cloning **GitHub**. This HF repo is the public **model card** + sanitized mirror.

If llama.cpp already owns the 4070, **do not** `docker compose up` TabbyAPI/Ollama until you have freed VRAM. Do not recreate `qwen38-llama-server` to “make room.”

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

Weights go under `tabby_models/` (gitignored). Compose mounts `./tabby_models → /app/models`. `model_name` is a **directory name under that mount**.

```bash
mkdir -p tabby_models

huggingface-cli download turboderp/Llama-3.1-8B-Instruct-exl3 \
  --revision 6.0bpw \
  --local-dir tabby_models/Llama-3.1-8B-Instruct-exl3-6.0bpw

ls -la tabby_models/Llama-3.1-8B-Instruct-exl3-6.0bpw | head
```

**EXL2 will not load.** Use EXL3 quants only.

### 2B) Configure TabbyAPI (required before first launch)

```bash
cp -n tabby_config/config.example.yml tabby_config/config.yml
python3 -c "import secrets; print('admin_key:', secrets.token_hex(32)); print('api_key:  ', secrets.token_hex(32))"
```

Paste keys; set `model_name` to the folder you downloaded. Put the same `api_key` in Open WebUI `OPENAI_API_KEY`, `mcpo/config.json` `TABBYAPI_KEY`, and SillyTavern.

### 2C) Ollama / GGUF path (secondary backend)

After the Tabby stack is up **and allowed to own the GPU**:

```bash
docker exec -it tabby-tavern-ollama-1 ollama pull llama3.1:8b
docker exec -it tabby-tavern-ollama-1 ollama list
docker exec -it tabby-tavern-ollama-1 ollama run llama3.1:8b "Say hello in one sentence."
```

Lab measurement: ~8 GB VRAM for Llama-3.1-8B EXL3 6.0bpw + 8-bit cache, ~4 GB left for a small GGUF. Do not add llama.cpp as a third GPU tenant.

### 3) Frontend / search secrets (placeholders only)

**SillyTavern** (`sillytavern_config/config.yaml`):

* Default listen port **8000**
* `browserLaunch.enabled: false`
* `basicAuthMode: true` — ST refuses `0.0.0.0` without auth
* Replace `YOUR_ST_USERNAME_HERE` / `YOUR_ST_PASSWORD_HERE`

**SearXNG** (`searxng_config/settings.yml`): `secret_key` placeholder + `search.formats: [html, json]`.

### 4) Character cards (SillyTavern)

| File | What it is |
| --------------------------------------------- | -------------------------------- |
| `cards/default_Seraphina.png` | SillyTavern PNG character card |
| `cards/Seraphina/*.png` | Expression sprites |
| `cards/README.md` | Import notes |

1. Start SillyTavern → http://localhost:8000
2. Characters → Import → `cards/default_Seraphina.png`
3. Copy `cards/Seraphina/` into `sillytavern_data/default-user/characters/Seraphina/` if sprites do not import

Do not commit chats, `secrets.json`, or live API keys.

### 5) Launch Tabby compose

```bash
docker compose up -d
docker compose ps
```

Or `./start-stack.sh`. That script only orchestrates **this** compose file. It does not start llama.cpp.

### 6) Health checks (Tabby services)

```bash
docker compose ps
curl -sS -o /dev/null -w "sillytavern  %{http_code}\n" http://127.0.0.1:8000/ || true
curl -sS -o /dev/null -w "open-webui   %{http_code}\n" http://127.0.0.1:3000/ || true
curl -sS -o /dev/null -w "tabbyapi     %{http_code}\n" http://127.0.0.1:5000/ || true
curl -sS -o /dev/null -w "ollama       %{http_code}\n" http://127.0.0.1:11435/ || true
curl -sS -o /dev/null -w "searxng      %{http_code}\n" http://127.0.0.1:8080/ || true
curl -sS -o /dev/null -w "mcpo         %{http_code}\n" http://127.0.0.1:8001/docs || true
```

Browser (Tabby layer): SillyTavern `:8000` · Open WebUI `:3000` · TabbyAPI `:5000` · Ollama `:11435` · SearXNG `:8080` · MCPO `:8001/docs`

Taproot (already live on LightBringer): llama.cpp `:1234` · Taproot Open WebUI `:3001`

### 7) Point SillyTavern at TabbyAPI

* API type: OpenAI-compatible / TabbyAPI
* Endpoint: `http://tabbyapi:5000/v1` from another container, or `http://127.0.0.1:5000/v1` from the host
* API key: `api_key` in `tabby_config/config.yml`

### 8) Switch / reload TabbyAPI model

```bash
# Edit model_name in tabby_config/config.yml to another folder under tabby_models/
docker compose restart tabbyapi
docker compose logs -f tabbyapi
```

---

## MCPO (MCP → OpenAPI)

`mcp-servers/server.py` is a **FastMCP** server (not raw JSON-RPC) with 7 tools:

| Tool | Description |
| ------------------- | ----------------------------------- |
| `list_tabbyapi_models` | List loaded EXL3 models in TabbyAPI |
| `tabbyapi_chat` | Chat with the TabbyAPI EXL3 model |
| `list_ollama_models` | List GGUF models in Ollama |
| `ollama_pull_model` | Pull a model into Ollama |
| `ollama_chat` | Chat with an Ollama model |
| `get_stack_status` | Health check Tabby services |
| `searxng_search` | Web search via SearXNG (JSON) |

`mcp-servers/tavern_mcp.py` is the connectivity toolkit (`status`, `self_check`, `wire`, `models`, `chat`). Wire it only if you also ship `discover.py` next to it.

---

## GPU / compose tuning (Tabby layer)

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

If llama.cpp is already resident, **leave Tabby GPU services down**.

---

## Repository structure

```text
tabby-tavern-stack/
├── docker-compose.yml              # Tabby layer (6 services) — names/ports stay Tabby
├── docker-compose.starter.yml      # optional overlay (not the live VS Code desk)
├── Dockerfile / Dockerfile.tabby   # TabbyAPI image (WSL2 libcuda fix)
├── start-stack.sh                  # Tabby compose only
├── cards/                          # SillyTavern character cards (PNG)
├── mcpo/config.json
├── mcp-servers/server.py
├── tabby_config/config.example.yml
├── sillytavern_config/config.yaml
├── searxng_config/settings.yml
├── SECURITY.md
├── DEVLOG.md
├── LICENSE
└── docs/spaces/                    # sell sheet + Space HTML (whole-lab story)
```

On the live machine (not in this tree): `~/taproot/docker-compose.yml`, `~/qwen38-agent/`, `~/dockroot/`, `~/.continue/config.yaml`, `~/.local/bin/grok`, `~/.hermes/hermes-agent`. `~/annie-scratch` is class-only.

---

## Environment & secrets guidance

| Secret / file | Where | Rule |
| -------------------------------- | ---------------------------- | ------------------------------------------- |
| TabbyAPI `admin_key` / `api_key` | `tabby_config/config.yml` | Generate yourself; never commit live values |
| Open WebUI `OPENAI_API_KEY` | Tabby compose env | Same value as TabbyAPI `api_key` |
| MCPO `--api-key` / `TABBYAPI_KEY` | compose + `mcpo/config.json` | Placeholders in public tree |
| SillyTavern basic auth | `sillytavern_config/config.yaml` | Replace `YOUR_ST_*` placeholders |
| SearXNG `secret_key` | `searxng_config/settings.yml` | Replace placeholder |
| Open WebUI DBs | `openwebui_data/` and `~/taproot/open-webui-data` | gitignored / off this tree |
| Continue | `~/.continue/config.yaml` | Host file; no live keys in this repo |

**Private-lab defaults are intentional.** Read [`SECURITY.md`](SECURITY.md). Treat any key that ever appeared in an older public revision as burned.

---

## Common failure modes

| Symptom | Likely cause | Fix |
| --------------------------------------------- | ------------------------------------------ | ----------------------------------------------------------------- |
| `local/tabbyapi:exl3-fixed` start fails | Image never built | `docker build -f Dockerfile.tabby -t local/tabbyapi:exl3-fixed .` |
| TabbyAPI: `exl2` backend no longer supported | Pointed at an EXL2 directory | Download an EXL3 revision instead |
| `/usr/bin/ld: cannot find -lcuda` | WSL2 CUDA libs not on linker path | Use the patched `Dockerfile.tabby` in this repo |
| TabbyAPI cannot find model | `model_name` ≠ folder under `tabby_models/` | Align names; confirm mount |
| CUDA “stalls forever” bringing Tabby up | llama.cpp already on the 4070 | Leave Tabby GPU down; do not bounce llama |
| Continue cannot reach the model | Wrong host/path | Host Continue → `http://127.0.0.1:1234/v1` |
| Taproot WebUI cannot reach llama | Used `localhost` inside the container | `http://host.docker.internal:1234/v1` |
| Recreated llama container | `docker compose up` on taproot yaml | Do not; live name is `qwen38-llama-server` |
| Host port 11434 in use | Host Ollama already running | Keep Tabby map `11435:11434` |
| SearXNG 500s / no JSON | Placeholder secret or HTML-only formats | Set secret; add `json` |
| MCPO crash: no mcpServers | Empty config | Keep at least one server entry |
| SillyTavern refuses to start | Listen 0.0.0.0 with no auth | Keep `basicAuthMode: true` |
| NVIDIA apt `Malformed entry` | Wrong toolkit repo line | See WSL2 notes below |

---

## Measured lab results (defensible only)

Numbers from [`local_grid_suite`](https://github.com/jpanasuk-netizen/local_grid_suite) plus the Tabby 24/24 compose pass. **Single-box lab runs — not a product SLA.**

| Stage | Model | Decode tok/s |
| ---------- | ----------------- | --------------- |
| Baseline | `qwen3:8b` | **1.39** |
| GPU-routed | `qwen-gpu:latest` | **29.7 – 39.3** |
| Stabilized | `qwen-gpu:latest` | **37.47** |

Warm stream suite on `qwen3:8b`: **~76 tok/s**. WSL2 EXL3 chat (Llama-3.1-8B-Instruct 6.0bpw): **~53 tok/s** in the 24/24 check pass.

Qwen3.5-9B llama.cpp tok/s is **not** published. Re-measure on your hardware.

---

## Engineering notes

See [`DEVLOG.md`](DEVLOG.md):

* Tabby compose consolidation + EXL3 + WSL2 `libcuda` + MCPO + cards
* Taproot local coding desk (qwen38-agent lineage → taproot project: llama.cpp 262k, VS Code / Continue / Grok / Hermes)
* VRAM last-call: one heavy engine on the 4070

---

## Optional coding starter overlay

`docker-compose.starter.yml` is **optional** (browser IDE, vector DBs, n8n). Not required. Not Taproot. Expects `ai-network` to exist. Change every placeholder password before `up`.

---

## WSL2 field notes — fresh-install lessons (Aug 2026)

A from-scratch rebuild on clean WSL2 (same RTX 4070). Additive to the cold-start guide.

### EXL2 vs EXL3 — TabbyAPI dropped EXL2 support

```
ValueError: Models quantized with 'exl2' require the exllamav2 backend, which is no longer supported. Please use an exl3 or unquantized model.
```

Use EXL3 quants only (`turboderp/Llama-3.1-8B-Instruct-exl3` branches 2.0–8.0 bpw).

### NVIDIA Container Toolkit repo URL

The `deb .../noble main` line is **wrong** (apt: `Malformed entry (Component)`). Flat structure:

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

Even with `torch.cuda.is_available() == True`, model load can fail with `cannot find -lcuda`:

```dockerfile
RUN ln -sf /usr/local/cuda-12.8/compat/libcuda.so /usr/lib/x86_64-linux-gnu/libcuda.so && ldconfig
```

Triton “not supported, roll back to CPU” warnings are **cosmetic** — exllamav3 uses its own CUDA kernels.

### Port conflict when host Ollama is already running

Tabby compose maps `11435:11434`. Open WebUI still uses `http://ollama:11434` internally.

### Verified working state (Tabby compose path)

24/24 checks when Tabby owns the GPU: six containers, EXL3 chat, Ollama `llama3.1:8b`, Open WebUI dual backend, SillyTavern with cards, SearXNG JSON, MCPO 7 tools, ~8 GB / 12 GB VRAM.

### Verified working state (Taproot path, 2026-08-25)

llama.cpp `qwen38-llama-server` Up on `:1234`; Taproot WebUI Up on `:3001`; Continue on host `:1234/v1`; Tabby GPU path Exited; VRAM 11450 / 12282 MiB.

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
