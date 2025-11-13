#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FRONTEND_DIR="$SCRIPT_DIR/../Frontend"
BACKEND_DIR="$SCRIPT_DIR/../Backend"

# --- Frontend ---
(
  cd "$FRONTEND_DIR"
  echo "🚀 Starting Frontend with Vite..."
  sudo -u jenkins npm run dev
) &

# --- Backend ---
(
  cd "$BACKEND_DIR"
  echo "⚡ Starting Backend (Flask Server)..."
  sudo -u jenkins bash -c "source venv/bin/activate && python3 -m src.flask_server"
) &

wait
