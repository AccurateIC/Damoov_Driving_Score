#!/bin/bash
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$SCRIPT_DIR/../Backend"

echo "🐍 Setting up backend virtual environment..."
cd "$BACKEND_DIR"

if [ ! -d "venv" ]; then
  python3 -m venv venv
fi

echo "📥 Installing backend dependencies as Jenkins user..."
sudo -u jenkins bash -c "cd '$BACKEND_DIR' && ./venv/bin/pip install --upgrade pip"
sudo -u jenkins bash -c "cd '$BACKEND_DIR' && ./venv/bin/pip install -r src/app/requirements.txt"
sudo -u jenkins bash -c "cd '$BACKEND_DIR' && ./venv/bin/pip install requests"
