#!/bin/bash
set -e  # stop if error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

FRONTEND_PORT=7001
BACKEND_PORT=6001

echo "🚀 Starting Frontend on $FRONTEND_PORT..."
cd "$SCRIPT_DIR/../Frontend"
nohup node node_modules/vite/bin/vite.js --port $FRONTEND_PORT > "$SCRIPT_DIR/frontend.log" 2>&1 &

echo "⚡ Starting Backend on $BACKEND_PORT..."
cd "$SCRIPT_DIR/../Backend"
source venv/bin/activate
nohup python3 -m src.flask_server --port $BACKEND_PORT > "$SCRIPT_DIR/backend.log" 2>&1 &
deactivate

echo "✅ Servers started. Check logs:"
echo "   Frontend → $SCRIPT_DIR/frontend.log"
echo "   Backend  → $SCRIPT_DIR/backend.log"
