#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FRONTEND_PORT=7001
BACKEND_PORT=6001

echo "🚀 Starting Frontend..."
cd "$SCRIPT_DIR/../Frontend"
nohup node node_modules/vite/bin/vite.js --port $FRONTEND_PORT --host 0.0.0.0 > "$SCRIPT_DIR/frontend.log" 2>&1 &
sleep 5

echo "⚡ Starting Backend..."
cd "$SCRIPT_DIR/../Backend"
"$SCRIPT_DIR/../Backend/venv/bin/python3" -m src.flask_server --port $BACKEND_PORT > "$SCRIPT_DIR/backend.log" 2>&1 &

echo "✅ Servers started. Check logs:"
echo "   Frontend → $SCRIPT_DIR/frontend.log"
echo "   Backend  → $SCRIPT_DIR/backend.log"
