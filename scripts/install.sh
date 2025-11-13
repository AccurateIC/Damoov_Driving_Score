#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# --- Frontend ---
cd "$SCRIPT_DIR/../Frontend"
echo "📦 Installing Frontend dependencies..."
npm install

# --- Backend ---
cd "$SCRIPT_DIR/../Backend"
if [ ! -d "venv" ]; then
  echo "🐍 Creating Python virtual environment..."
  python3 -m venv venv
fi

echo "📥 Installing Backend dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r src/app/requirements.txt
pip install requests
deactivate

echo "✅ Installation completed successfully."
