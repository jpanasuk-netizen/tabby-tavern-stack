# Security notes

This stack is designed for a **private local lab** (single trusted machine / LAN), not a public multi-tenant deployment.

## Defaults to change before any network exposure

- Replace every `REPLACE_WITH_*` / `YOUR_*_HERE` placeholder immediately
- Generate TabbyAPI `admin_key` and `api_key` with `python3 -c "import secrets; print(secrets.token_hex(32))"`
- Use the **same** TabbyAPI `api_key` in Open WebUI `OPENAI_API_KEY`, MCPO `TABBYAPI_KEY`, and SillyTavern
- Do not publish `api_tokens.yml`, cookie secrets, chat logs, or SSH keys
- Bind ports to localhost (`127.0.0.1`) if you do not need LAN access
- Keep model directories and user chat data out of git (see `.gitignore`)
- Prefer `disable_auth: false` and long random keys in TabbyAPI config
- SillyTavern on `0.0.0.0` needs `basicAuthMode: true` (or user accounts) or it will refuse to start

## Incident note (public mirror hygiene)

Earlier public revisions of this Hugging Face / GitHub tree included lab convenience keys:

- TabbyAPI keys in `tabby_config/config.yml`
- A live `TABBYAPI_KEY` in `mcpo/config.json` (`a4333bfb7630a44bec1f23175f27e1ee` and later lab values)

Those keys must be treated as **compromised for any shared or networked use**. Rotate them everywhere they might have been reused. The public tree now ships **placeholders and examples only**.

## What is intentionally not in this repo

- Model weights
- Live user databases / chat logs
- Real API tokens

SillyTavern **character cards** (PNG) under `cards/` are included on purpose. They are not credentials.

If you found a secret in an older revision, rotate it and open an issue on the GitHub companion: https://github.com/jpanasuk-netizen/tabby-tavern-stack
