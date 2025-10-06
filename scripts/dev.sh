#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Define fixed ports
FRONTEND_PORT=7001
BACKEND_PORT=6001

echo "🧹 Cleaning up old processes using ports $FRONTEND_PORT and $BACKEND_PORT..."

# Kill any old processes running on those ports
lsof -ti:$FRONTEND_PORT | xargs -r kill -9
lsof -ti:$BACKEND_PORT | xargs -r kill -9

# Start Frontend with Vite
(
  cd "$SCRIPT_DIR/../Frontend"
  echo "🚀 Starting Frontend on port $FRONTEND_PORT..."
  nohup node node_modules/vite/bin/vite.js --port $FRONTEND_PORT > "$SCRIPT_DIR/frontend.log" 2>&1 &
)

# Start Backend inside venv
(
  cd "$SCRIPT_DIR/../Backend"
  echo "⚡ Starting Backend on port $BACKEND_PORT..."
  source venv/bin/activate
  nohup python3 -m src.flask_server --port $BACKEND_PORT > "$SCRIPT_DIR/backend.log" 2>&1 &
  deactivate
)

echo "✅ Both servers started successfully!"
echo "Frontend ➜ http://localhost:$FRONTEND_PORT"
echo "Backend  ➜ http://localhost:$BACKEND_PORT"
