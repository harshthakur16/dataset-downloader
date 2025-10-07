#!/usr/bin/env bash
set -euo pipefail

# Create venv if missing
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi

# Activate venv
# shellcheck disable=SC1091
source .venv/bin/activate

# Install deps
python -m pip install --upgrade pip
pip install -r requirements.txt

# Ensure .env exists or prompt for key
if [ ! -f ".env" ]; then
  if [ -f ".env.example" ]; then
    cp .env.example .env
  else
    touch .env
  fi
  read -rp "Enter your SEEKHO API key: " SEEKHO_API_KEY
  # Replace or add the line
  if grep -q '^SEEKHO_API_KEY=' .env; then
    sed -i.bak "s/^SEEKHO_API_KEY=.*/SEEKHO_API_KEY=${SEEKHO_API_KEY}/" .env
  else
    printf "\nSEEKHO_API_KEY=%s\n" "$SEEKHO_API_KEY" >> .env
  fi
fi

# Run the tool
python -m seekho_downloader --out dataset.csv

echo
echo "Done. You can find dataset.csv in this folder."
