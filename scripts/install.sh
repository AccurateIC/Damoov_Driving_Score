#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Install Frontend dependencies
cd "$SCRIPT_DIR/../Frontend"
echo "📦 Installing Frontend dependencies..."
npm install

# Setup Backend venv + install requirements
cd "$SCRIPT_DIR/../Backend"
if [ ! -d "venv" ]; then
  echo "🐍 Creating Python virtual environment..."
  python3 -m venv venv || { echo "❌ Failed to create venv. Did you install python3-venv?"; exit 1; }
fi

echo "📥 Installing Backend dependencies..."
source venv/bin/activate
pip install -r src/app/requirements.txt
deactivate || true
