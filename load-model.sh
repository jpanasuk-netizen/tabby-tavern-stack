#!/bin/bash
set -e

CONFIG=~/tabby-tavern/tabby_config/config.yml
MODEL="Meta-Llama-3.1-8B-Instruct-abliterated-exl2-6.5bpw"

# Make sure config exists
if [ ! -f "$CONFIG" ]; then
  echo "Config not found at $CONFIG"
  exit 1
fi

# Set or update model_name
if grep -q "model_name:" "$CONFIG"; then
  sed -i "s|model_name:.*|model_name: $MODEL|" "$CONFIG"
else
  # Add it under the model section if missing
  sed -i "/^model:/a\  model_name: $MODEL" "$CONFIG"
fi

echo "Updated config with model: $MODEL"
echo "Restarting TabbyAPI..."
cd ~/tabby-tavern
docker compose restart tabbyapi

echo "Waiting for model to load..."
sleep 5
docker compose logs tabbyapi --tail 20
