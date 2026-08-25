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

echo "=== Spinning up UNIFIED Docker AI stack ==="
docker compose up -d

echo ""
echo "=================================================="
echo " Services initializing from: $ROOT"
echo " Open WebUI:      http://localhost:3000"
echo " Qwen llama.cpp:  http://localhost:1234"
echo " SillyTavern:     http://localhost:8000"
echo " MCPO docs:       http://localhost:8001/docs"
echo " SearXNG:         http://localhost:8080"
echo " code-server:     http://localhost:8443"
echo " LibreChat:       http://localhost:3080"
echo " AnythingLLM:     http://localhost:3002"
echo " Lobe:            http://localhost:3210"
echo " n8n:             http://localhost:5678"
echo " Qdrant:          http://localhost:6333"
echo " Chroma:          http://localhost:8005"
echo " Meilisearch:     http://localhost:7700"
echo " Firefox:         http://localhost:3010"
echo " Bookmarks HTML:  $ROOT/browser/bookmarks.html"
echo " Alternate inference (not default): TabbyAPI :5000 · Ollama :11435"
echo " Character cards: $ROOT/cards/"
echo "=================================================="
