#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🧹 Stopping any previously running frontend/backend..."
pkill -f "python3 -m src.flask_server" 2>/dev/null || echo "No backend running"
pkill -f "vite" 2>/dev/null || echo "No frontend running"

(
  cd "$SCRIPT_DIR/../Frontend"
  echo "🚀 Starting Frontend with Vite..."
  nohup node node_modules/vite/bin/vite.js --port 7001 --host 192.168.10.41 > "$SCRIPT_DIR/frontend.log" 2>&1 &
)

(
  cd "$SCRIPT_DIR/../Backend"
  echo "⚡ Starting Backend (Flask Server)..."
  source venv/bin/activate
  nohup python3 -m src.flask_server > "$SCRIPT_DIR/backend.log" 2>&1 &
  deactivate
)

echo "✅ Both servers started successfully!"
echo "🌐 Frontend → http://192.168.10.41:7001"
echo "🖥️ Backend  → http://192.168.10.41:6001"

wait
