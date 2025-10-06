#!/bin/bash
set -e  # Stop on any error

# Absolute path of the script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# -------------------------------
# Frontend: Install dependencies
# -------------------------------
cd "$SCRIPT_DIR/../Frontend"
echo "📦 Installing Frontend dependencies..."
# Ensure Jenkins user can write to node_modules
mkdir -p node_modules
chmod -R 755 node_modules
npm install
# Optional: build for production if serving via Flask
npm run build

# -------------------------------
# Backend: Setup virtual environment
# -------------------------------
cd "$SCRIPT_DIR/../Backend"
if [ ! -d "venv" ]; then
  echo "🐍 Creating Python virtual environment..."
  python3 -m venv venv || { echo "❌ Failed to create venv. Install python3-venv?"; exit 1; }
fi

# Make sure venv and site-packages are writable
chmod -R 755 venv

echo "📥 Installing Backend dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r src/app/requirements.txt
deactivate

echo "✅ Dependencies installed successfully!"
