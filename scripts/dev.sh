#!/bin/bash

# Exit on error
set -e

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Default ports (or take from arguments)
FRONTEND_PORT=${1:-7001}
BACKEND_PORT=${2:-6001}

# Log files
FRONTEND_LOG="$SCRIPT_DIR/../Frontend/vite.log"
BACKEND_LOG="$SCRIPT_DIR/../Backend/flask.log"

# Kill existing processes
fuser -k ${FRONTEND_PORT}/tcp || true
fuser -k ${BACKEND_PORT}/tcp || true

echo "🚀 Starting Frontend on port ${FRONTEND_PORT}..."
(
  cd "$SCRIPT_DIR/../Frontend"
  nohup node node_modules/vite/bin/vite.js --port ${FRONTEND_PORT} > "$FRONTEND_LOG" 2>&1 &
)

echo "⚡ Starting Backend on port ${BACKEND_PORT}..."
(
  cd "$SCRIPT_DIR/../Backend"
  source venv/bin/activate
  nohup python3 -m src.flask_server --port ${BACKEND_PORT} > "$BACKEND_LOG" 2>&1 &
  deactivate
)

sleep 5
echo "✅ Frontend (port ${FRONTEND_PORT}) and Backend (port ${BACKEND_PORT}) are up and running!"
