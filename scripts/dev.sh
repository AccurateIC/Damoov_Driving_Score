#!/bin/bash

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Default ports if not provided
FRONTEND_PORT=${FRONTEND_PORT:-7001}
BACKEND_PORT=${BACKEND_PORT:-6001}

# Start Frontend (Vite) in background
(
  cd "$SCRIPT_DIR/../Frontend"
  echo "🚀 Starting Frontend on port $FRONTEND_PORT..."
  nohup node node_modules/vite/bin/vite.js --port $FRONTEND_PORT > vite.log 2>&1 &
)

# Start Backend (Flask) in background
(
  cd "$SCRIPT_DIR/../Backend"
  echo "⚡ Starting Backend on port $BACKEND_PORT..."
  source venv/bin/activate
  nohup python3 -m src.flask_server --port $BACKEND_PORT > flask.log 2>&1 &
  deactivate
)

echo "✅ Both servers started. Frontend: $FRONTEND_PORT, Backend: $BACKEND_PORT"
