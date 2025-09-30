#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

FRONTEND_PORT=7001
BACKEND_PORT=6001

# Start frontend (detached)
(
  cd "$SCRIPT_DIR/../Frontend"
  echo "🚀 Starting Frontend on port $FRONTEND_PORT..."
  nohup node node_modules/vite/bin/vite.js --port $FRONTEND_PORT > vite.log 2>&1 &
)

# Start backend (detached)
(
  cd "$SCRIPT_DIR/../Backend"
  echo "⚡ Starting Backend on port $BACKEND_PORT..."
  source venv/bin/activate
  nohup python3 -m src.flask_server --port $BACKEND_PORT > flask.log 2>&1 &
  deactivate
)

echo "✅ New servers started!"
echo "   Frontend → http://localhost:$FRONTEND_PORT"
echo "   Backend  → http://localhost:$BACKEND_PORT"
