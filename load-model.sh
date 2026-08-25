#!/bin/bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
CONFIG="$ROOT/tabby_config/config.yml"
MODEL="${1:-Llama-3.1-8B-Instruct-exl3-6.0bpw}"

if [ ! -f "$CONFIG" ]; then
  echo "Config not found at $CONFIG"
  echo "Copy tabby_config/config.example.yml to tabby_config/config.yml first."
  exit 1
fi

if [ ! -d "$ROOT/tabby_models/$MODEL" ]; then
  echo "Model directory not found: $ROOT/tabby_models/$MODEL"
  echo "Download an EXL3 pack into tabby_models/<folder>/ first. EXL2 will not load."
  exit 1
fi

if grep -q "model_name:" "$CONFIG"; then
  sed -i "s|model_name:.*|model_name: $MODEL|" "$CONFIG"
else
  sed -i "/^model:/a\\  model_name: $MODEL" "$CONFIG"
fi

echo "Updated config with model: $MODEL"
echo "Restarting TabbyAPI..."
cd "$ROOT"
docker compose restart tabbyapi
echo "Waiting for model to load..."
sleep 5
docker compose logs tabbyapi --tail 30
