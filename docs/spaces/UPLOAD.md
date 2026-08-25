# Hugging Face Space uploads

Static family for Jeremy Panasuk (`jpanasuk`). Shared CSS: `docs/spaces/tavern.css`.

**Do not confuse** the model card with the new Space:

| Surface | URL |
| --- | --- |
| Model card (already exists) | https://huggingface.co/jpanasuk/tabby-tavern-stack |
| **New Space** (static SDK) | https://huggingface.co/spaces/jpanasuk/tabby-tavern-stack |
| Sell sheet Space (update) | https://huggingface.co/spaces/jpanasuk/tabby-tavern-sell-sheet |
| Connectivity companion (fill App) | https://huggingface.co/spaces/jpanasuk/local-ai-stack-connectivity |
| dockroot companion (restyle) | https://huggingface.co/spaces/jpanasuk/dockroot-mcp |

This cloud environment had **no** `HF_TOKEN` / `huggingface_hub` login. Nothing was published from the agent. Run the commands below on a machine that is logged in as `jpanasuk`.

```bash
# one-time
pipx install "huggingface_hub[cli]"
hf auth login   # or: export HF_TOKEN=hf_...

ROOT="$(cd "$(dirname "$0")" && pwd)"   # docs/spaces
cp "$ROOT/tavern.css" "$ROOT/tabby-tavern-stack/tavern.css"
cp "$ROOT/tavern.css" "$ROOT/tabby-tavern-sell-sheet/tavern.css"
cp "$ROOT/tavern.css" "$ROOT/local-ai-stack-connectivity/tavern.css"
cp "$ROOT/tavern.css" "$ROOT/dockroot-mcp/tavern.css"

# 1) CREATE the stack Space (does not exist yet; model repo is a different namespace)
hf repo create jpanasuk/tabby-tavern-stack --type space --space-sdk static --exist-ok
hf upload jpanasuk/tabby-tavern-stack "$ROOT/tabby-tavern-stack" . --repo-type space

# 2) UPDATE sell sheet (replace App + README only)
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

Optional: mirror `README.md` from GitHub to the **model card** (not the Space):

```bash
hf upload jpanasuk/tabby-tavern-stack README.md README.md --repo-type model
```

`short_description` on the new Space is ≤60 characters: Independent AI lab — EXL3 compose + llama.cpp 262k desk. The Space is **not** live until these commands succeed. This environment has no HF token.
