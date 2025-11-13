#!/bin/bash
set -e

# === Common Paths ===
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FRONTEND_DIR="$SCRIPT_DIR/../Frontend"
BACKEND_DIR="$SCRIPT_DIR/../Backend"

echo "🚀 Starting Damoov Dev Environment..."

# === Frontend ===
echo "📦 Installing Frontend dependencies..."
cd "$FRONTEND_DIR"
npm install

# === Backend ===
echo "🐍 Setting up Backend..."
cd "$BACKEND_DIR"

if [ ! -d "venv" ]; then
  echo "🧱 Creating Python virtual environment..."
  python3 -m venv venv
fi

echo "📥 Installing Python dependencies..."
sudo -u jenkins bash -c "cd '$BACKEND_DIR' && ./venv/bin/pip install --upgrade pip"
sudo -u jenkins bash -c "cd '$BACKEND_DIR' && ./venv/bin/pip install -r src/app/requirements.txt"

# === Run Frontend ===
(
  cd "$FRONTEND_DIR"
  echo "⚡ Starting Frontend (Vite)..."
  npm run dev
) &

# === Run Backend ===
(
  cd "$BACKEND_DIR"
  echo "🔥 Starting Backend (Flask)..."
  source venv/bin/activate
  python3 -m src.flask_server
  deactivate
) &

wait
