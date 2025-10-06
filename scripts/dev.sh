#!/bin/bash

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ------------------ Frontend ------------------
(
  cd "$SCRIPT_DIR/../Frontend" || exit
  echo "🚀 Installing frontend dependencies..."
  npm install
  echo "🚀 Starting frontend with Vite..."
  node node_modules/vite/bin/vite.js --host 0.0.0.0 --port 7001
) &

# ------------------ Backend ------------------
(
  cd "$SCRIPT_DIR/../Backend" || exit
  echo "⚡ Setting up backend virtualenv..."
  if [ ! -d "venv" ]; then
      python3 -m venv venv
  fi

  if [ -f "requirements.txt" ]; then
      . venv/bin/activate
      echo "⚡ Installing backend dependencies..."
      pip install -r requirements.txt
      echo "⚡ Starting Flask server..."
      python3 -m src.flask_server --host 0.0.0.0 --port 6001
      deactivate
  else
      echo "⚠️ requirements.txt not found in Backend!"
  fi
) &

wait
