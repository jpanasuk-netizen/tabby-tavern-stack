# Hugging Face uploads — existing surfaces only

Source of truth in this repo for the **two live Hugging Face surfaces**:

| Live surface | In-repo file | Hugging Face |
| --- | --- | --- |
| **Model card** | repo-root `README.md` | https://huggingface.co/jpanasuk/tabby-tavern-stack (`--repo-type model`) |
| **Sell sheet Space** | `docs/spaces/tabby-tavern-sell-sheet/` | https://huggingface.co/spaces/jpanasuk/tabby-tavern-sell-sheet |

Companions (also existing):

| Space | In-repo folder |
| --- | --- |
| https://huggingface.co/spaces/jpanasuk/dockroot-mcp | `docs/spaces/dockroot-mcp/` |
| https://huggingface.co/spaces/jpanasuk/local-ai-stack-connectivity | `docs/spaces/local-ai-stack-connectivity/` |

**Do not create** `spaces/jpanasuk/tabby-tavern-stack`. That Space is unpublished and is **not** part of this lab. The model card slug and the sell-sheet Space are the public HTML/markdown.

This cloud environment had **no** `HF_TOKEN`. Nothing was published from the agent until those commands run as `jpanasuk`.

```bash
# one-time
pipx install "huggingface_hub[cli]"
hf auth login   # or: export HF_TOKEN=hf_...  (write token for jpanasuk)

ROOT="$(cd "$(dirname "$0")" && pwd)"   # docs/spaces
REPO="$(cd "$ROOT/../.." && pwd)"       # git root
cp "$ROOT/tavern.css" "$ROOT/tabby-tavern-sell-sheet/tavern.css"
cp "$ROOT/tavern.css" "$ROOT/local-ai-stack-connectivity/tavern.css"
cp "$ROOT/tavern.css" "$ROOT/dockroot-mcp/tavern.css"

# 1) REQUIRED — live model card (this is why HF still shows Tabby-only until you run it)
hf upload jpanasuk/tabby-tavern-stack "$REPO/README.md" README.md --repo-type model
hf upload jpanasuk/tabby-tavern-stack "$REPO/DEVLOG.md" DEVLOG.md --repo-type model

# 2) REQUIRED — live sell-sheet Space (App + Space README + CSS)
hf upload jpanasuk/tabby-tavern-sell-sheet "$ROOT/tabby-tavern-sell-sheet/index.html" index.html --repo-type space
hf upload jpanasuk/tabby-tavern-sell-sheet "$ROOT/tabby-tavern-sell-sheet/README.md" README.md --repo-type space
hf upload jpanasuk/tabby-tavern-sell-sheet "$ROOT/tabby-tavern-sell-sheet/tavern.css" tavern.css --repo-type space

# 3) FILL connectivity App without deleting SKILL.md / recipes
hf upload jpanasuk/local-ai-stack-connectivity "$ROOT/local-ai-stack-connectivity/index.html" index.html --repo-type space
hf upload jpanasuk/local-ai-stack-connectivity "$ROOT/local-ai-stack-connectivity/README.md" README.md --repo-type space
hf upload jpanasuk/local-ai-stack-connectivity "$ROOT/local-ai-stack-connectivity/tavern.css" tavern.css --repo-type space

# 4) Restyle dockroot App (keep existing Python/Dockerfile siblings)
hf upload jpanasuk/dockroot-mcp "$ROOT/dockroot-mcp/index.html" index.html --repo-type space
hf upload jpanasuk/dockroot-mcp "$ROOT/dockroot-mcp/README.md" README.md --repo-type space
hf upload jpanasuk/dockroot-mcp "$ROOT/dockroot-mcp/tavern.css" tavern.css --repo-type space
```

Do **not** run `hf repo create … --type space` for `jpanasuk/tabby-tavern-stack`.
