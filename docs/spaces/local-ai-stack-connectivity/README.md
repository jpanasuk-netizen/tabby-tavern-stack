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

Part of **Tabby Tavern 2.0** — not a live service.

The connection rule: path is always `/v1`; inside Docker the host is the **service name**, not `localhost`. On the host, Continue uses `http://127.0.0.1:1234/v1`. Taproot WebUI uses `http://host.docker.internal:1234/v1`.

Open the **App** tab. `SKILL.md` and `references/wiring-recipes.md` (if present) are the Hermes deep reference (44 recipes) and are not duplicated on the page.

- Lab tour: https://huggingface.co/spaces/jpanasuk/tabby-tavern-stack
- GitHub: https://github.com/jpanasuk-netizen/tabby-tavern-stack
- dockroot-mcp: https://huggingface.co/spaces/jpanasuk/dockroot-mcp
