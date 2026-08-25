---
title: Local AI Stack Connectivity
emoji: 🔌
colorFrom: indigo
colorTo: purple
sdk: static
pinned: false
license: apache-2.0
short_description: The /v1 rule for the Independent AI Lab (44 recipes)
---

# Local AI Stack Connectivity

Part of the lab — not a live gateway. Two compose files, not one running stack.

The connection rule: path is always `/v1`. Live Taproot WebUI uses `http://host.docker.internal:1234/v1`. Continue on the host uses `http://127.0.0.1:1234/v1`. Inside Tabby compose (currently stopped), the host is the **service name**, not `localhost`.

Open the **App** tab. `SKILL.md` and `references/wiring-recipes.md` (if present) are the Hermes deep reference (44 recipes) and are not duplicated on the page.

- Sell sheet: https://huggingface.co/spaces/jpanasuk/tabby-tavern-sell-sheet
- GitHub: https://github.com/jpanasuk-netizen/tabby-tavern-stack
- dockroot-mcp: https://huggingface.co/spaces/jpanasuk/dockroot-mcp
