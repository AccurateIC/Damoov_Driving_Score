#!/bin/bash
set -e

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# === Frontend install ===
cd "$SCRIPT_DIR/../Frontend"
echo "📦 Installing Frontend dependencies..."
npm install --force

# === Backend install ===
cd "$SCRIPT_DIR/../Backend"
echo "🐍 Setting up backend virtual environment..."

if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

echo "📥 Installing backend dependencies..."
./venv/bin/pip install --upgrade pip
./venv/bin/pip install -r src/app/requirements
./venv/bin/pip install requests

echo "✅ Backend installation completed"
