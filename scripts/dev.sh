#!/bin/bash
set -e  # Stop on any error

# Absolute script path
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# LAN IP and ports
HOST_IP="192.168.10.41"
FRONTEND_PORT=7001
BACKEND_PORT=6001

# -----------------------------
# Start Frontend (Vite)
# -----------------------------
echo "🚀 Starting Frontend on $HOST_IP:$FRONTEND_PORT..."

cd "$SCRIPT_DIR/../Frontend"

# Update .env to point frontend to backend LAN IP
if [ -f ".env" ]; then
    sed -i "s#VITE_BASE_URL=.*#VITE_BASE_URL=http://$HOST_IP:$BACKEND_PORT#" .env
else
    echo "VITE_BASE_URL=http://$HOST_IP:$BACKEND_PORT" > .env
fi

# Run frontend
nohup npx vite --port $FRONTEND_PORT --host $HOST_IP > "$SCRIPT_DIR/frontend.log" 2>&1 &

# Wait a few seconds for frontend to initialize
sleep 5

# -----------------------------
# Start Backend (Flask)
# -----------------------------
echo "⚡ Starting Backend on $HOST_IP:$BACKEND_PORT..."

cd "$SCRIPT_DIR/../Backend"

# Ensure virtual environment exists
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Activate venv safely
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
fi

# Install requirements if missing
pip install --upgrade pip
pip install -r requirements.txt

# Run backend
nohup python3 -m src.flask_server --host $HOST_IP --port $BACKEND_PORT > "$SCRIPT_DIR/backend.log" 2>&1 &

# Deactivate venv
deactivate || true

# -----------------------------
# Summary
# -----------------------------
echo "✅ Servers started successfully!"
echo "   Frontend → http://$HOST_IP:$FRONTEND_PORT (logs: $SCRIPT_DIR/frontend.log)"
echo "   Backend  → http://$HOST_IP:$BACKEND_PORT (logs: $SCRIPT_DIR/backend.log)"
