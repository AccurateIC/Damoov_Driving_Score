#!/bin/bash
set -e  # Stop if any command fails

# Absolute path of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# LAN IP of the server
HOST_IP="192.168.10.41"

# Ports
FRONTEND_PORT=7001
BACKEND_PORT=6001

# -------------------------------
# Start Frontend
# -------------------------------
echo "🚀 Starting Frontend on $HOST_IP:$FRONTEND_PORT..."
cd "$SCRIPT_DIR/../Frontend"

# Update VITE_BASE_URL dynamically to point to backend LAN IP
if [ -f .env ]; then
    sed -i "s#VITE_BASE_URL=.*#VITE_BASE_URL=http://$HOST_IP:$BACKEND_PORT#" .env
else
    echo "VITE_BASE_URL=http://$HOST_IP:$BACKEND_PORT" > .env
fi

# Ensure node_modules exist
if [ ! -d node_modules ]; then
    echo "Installing frontend dependencies..."
    npm install
fi

# Start Vite frontend
nohup npx vite --port $FRONTEND_PORT --host $HOST_IP > "$SCRIPT_DIR/frontend.log" 2>&1 &

# Wait a few seconds to let frontend start
sleep 5

# -------------------------------
# Start Backend
# -------------------------------
echo "⚡ Starting Backend on $HOST_IP:$BACKEND_PORT..."
cd "$SCRIPT_DIR/../Backend"

# Ensure virtual environment exists
if [ ! -d venv ]; then
    echo "Creating virtual environment and installing backend dependencies..."
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Run Flask backend
nohup python3 -m src.flask_server --host $HOST_IP --port $BACKEND_PORT > "$SCRIPT_DIR/backend.log" 2>&1 &

# Deactivate virtual environment
deactivate

# -------------------------------
# Finished
# -------------------------------
echo "✅ Servers started successfully!"
echo "   Frontend → http://$HOST_IP:$FRONTEND_PORT (logs: $SCRIPT_DIR/frontend.log)"
echo "   Backend  → http://$HOST_IP:$BACKEND_PORT (logs: $SCRIPT_DIR/backend.log)"
