# Character cards

SillyTavern **character cards** shipped with Tabby Tavern v2.0.0.

These are PNG cards (embedded character spec) plus expression sprites. They are **not** model weights and **not** credentials.

## Contents

| Path | Use |
| ---- | --- |
| `default_Seraphina.png` | Import this in SillyTavern → Characters → Import |
| `Seraphina/*.png` | Expression sprites (admiration, joy, anger, …) |

## Import

1. Bring the core stack up (`docker compose up -d`) and open http://localhost:8000
2. Log in with the SillyTavern basic-auth values you set in `sillytavern_config/config.yaml`
3. **Characters → Import** → choose `cards/default_Seraphina.png`
4. If expressions do not appear, copy `cards/Seraphina/` to:

```text
sillytavern_data/default-user/characters/Seraphina/
```

Compose also bind-mounts this folder read-only at `/opt/cards` inside the SillyTavern container.

## What is not shipped

Chat logs, `secrets.json`, user settings, and API keys stay in the live lab data dir and are gitignored.
