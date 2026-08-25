# Hugging Face uploads — existing surfaces only

Live Hugging Face is the source of truth:

| Live surface | Commit (verified) | In-repo file |
| --- | --- | --- |
| https://huggingface.co/jpanasuk/tabby-tavern-stack | `b50983f` | repo-root `README.md` |
| https://huggingface.co/spaces/jpanasuk/tabby-tavern-sell-sheet | `de826bb` | `docs/spaces/tabby-tavern-sell-sheet/` |

**Do not create** `spaces/jpanasuk/tabby-tavern-stack`.

The sell-sheet Space App is a **self-contained** `index.html` (inline CSS). Do not replace it with a merged-stack tavern.css family page.

Companions (existing): dockroot-mcp · local-ai-stack-connectivity.

If you need to re-sync **from this repo back to HF** (only when GitHub matches the live topology: Taproot up, Tabby stopped):

```bash
pipx install "huggingface_hub[cli]"
hf auth login   # as jpanasuk

ROOT="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$ROOT/../.." && pwd)"

hf upload jpanasuk/tabby-tavern-stack "$REPO/README.md" README.md --repo-type model
hf upload jpanasuk/tabby-tavern-stack "$REPO/DEVLOG.md" DEVLOG.md --repo-type model

hf upload jpanasuk/tabby-tavern-sell-sheet "$ROOT/tabby-tavern-sell-sheet/index.html" index.html --repo-type space
hf upload jpanasuk/tabby-tavern-sell-sheet "$ROOT/tabby-tavern-sell-sheet/README.md" README.md --repo-type space
```

Do **not** `hf repo create … --type space` for `jpanasuk/tabby-tavern-stack`.
