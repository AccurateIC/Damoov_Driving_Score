#!/bin/bash
set -e  # Stop on error

# Absolute script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# LAN IP of your server
HOST_IP="192.168.10.41"

# Ports
FRONTEND_PORT=7001
BACKEND_PORT=6001

# Frontend
echo "🚀 Starting Frontend on $HOST_IP:$FRONTEND_PORT..."
cd "$SCRIPT_DIR/../Frontend"

# Make sure VITE_BASE_URL points to backend LAN IP
sed -i "s#VITE_BASE_URL=.*#VITE_BASE_URL=http://$HOST_IP:$BACKEND_PORT#" .env

nohup node node_modules/vite/bin/vite.js --port $FRONTEND_PORT --host $HOST_IP > "$SCRIPT_DIR/frontend.log" 2>&1 &

# Backend
echo "⚡ Starting Backend on $HOST_IP:$BACKEND_PORT..."
cd "$SCRIPT_DIR/../Backend"
source venv/bin/activate
nohup python3 -m src.flask_server --host $HOST_IP --port $BACKEND_PORT > "$SCRIPT_DIR/backend.log" 2>&1 &
deactivate

echo "✅ Servers started successfully!"
echo "   Frontend → http://$HOST_IP:$FRONTEND_PORT (logs: $SCRIPT_DIR/frontend.log)"
echo "   Backend  → http://$HOST_IP:$BACKEND_PORT (logs: $SCRIPT_DIR/backend.log)"
