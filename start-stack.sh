#!/bin/bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

if [ ! -f tabby_config/config.yml ]; then
  echo "Copying tabby_config/config.example.yml → tabby_config/config.yml"
  cp tabby_config/config.example.yml tabby_config/config.yml
  echo "Edit tabby_config/config.yml and set YOUR OWN keys + model_name before first use."
fi

echo "=== Spinning down old Docker stack ==="
docker compose down || true

echo "=== Spinning up full Docker AI stack ==="
docker compose up -d

echo ""
echo "=================================================="
echo " Services initializing from: $ROOT"
echo " Open WebUI:    http://localhost:3000"
echo " SillyTavern:   http://localhost:8000"
echo " SearXNG:       http://localhost:8080"
echo " Ollama (host): http://localhost:11435"
echo " TabbyAPI:      http://localhost:5000"
echo " MCPO docs:     http://localhost:8001/docs"
echo " Character cards: $ROOT/cards/"
echo "=================================================="
