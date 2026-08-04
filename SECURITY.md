# Security notes

This stack is designed for a **private local lab** (single trusted machine / LAN), not a public multi-tenant deployment.

## Defaults to change before any network exposure
- Replace any default admin credentials immediately
- Do not publish `api_tokens.yml`, cookie secrets, or SSH keys
- Bind ports to localhost if you do not need LAN access
- Keep model directories and user chat data out of git (see `.gitignore`)

## What is intentionally not in this repo
- Model weights
- Live user databases / chat logs
- Real API tokens

If you found a secret in an older revision, rotate it and open an issue.
