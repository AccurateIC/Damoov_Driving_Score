#!/bin/bash
set -e  # Stop if any command fails

# Get absolute script path
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Define ports
FRONTEND_PORT=7001
BACKEND_PORT=6001
HOST_IP="0.0.0.0"

echo "🚀 Starting Frontend on $FRONTEND_PORT..."
cd "$SCRIPT_DIR/../Frontend"
nohup node node_modules/vite/bin/vite.js --port $FRONTEND_PORT --host $HOST_IP > "$SCRIPT_DIR/frontend.log" 2>&1 &
sleep 5

echo "⚡ Starting Backend on $BACKEND_PORT..."
cd "$SCRIPT_DIR/../Backend"

# Activate virtual environment and run backend
source venv/bin/activate
nohup python3 -m src.flask_server --host $HOST_IP --port $BACKEND_PORT > "$SCRIPT_DIR/backend.log" 2>&1 &
deactivate

echo "✅ Servers started successfully!"
echo "   Frontend → http://$HOST_IP:$FRONTEND_PORT (logs: $SCRIPT_DIR/frontend.log)"
echo "   Backend  → http://$HOST_IP:$BACKEND_PORT (logs: $SCRIPT_DIR/backend.log)"
