#!/bin/bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

echo "=== Spinning down old Docker stack ==="
docker compose down || true

echo "=== Spinning up full Docker AI stack ==="
docker compose up -d

echo ""
echo "=================================================="
echo " Services initializing from: $ROOT"
echo " Open WebUI:   http://localhost:3000"
echo " SillyTavern:  http://localhost:8000"
echo " SearXNG:      http://localhost:8080"
echo " Ollama:       http://localhost:11434"
echo " TabbyAPI:     http://localhost:5000"
echo "=================================================="
