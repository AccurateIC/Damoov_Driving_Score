#!/bin/bash
set -e

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOST_IP="192.168.10.41"
FRONTEND_DIR="$SCRIPT_DIR/../Frontend"
BACKEND_DIR="$SCRIPT_DIR/../Backend"

# -----------------------------
# Install & Build Frontend
# -----------------------------
cd "$FRONTEND_DIR"
echo "📦 Installing frontend dependencies..."
npm install

echo "🏗️ Building frontend for production..."
npm run build

# Update .env to backend LAN IP
sed -i "s#VITE_BASE_URL=.*#VITE_BASE_URL=http://$HOST_IP:6001#" .env

# -----------------------------
# Setup Backend
# -----------------------------
cd "$BACKEND_DIR"
if [ ! -d "venv" ]; then
    echo "🐍 Creating Python virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -r src/app/requirements.txt
deactivate

# -----------------------------
# Stop previous servers
# -----------------------------
pkill -f "python3 -m src.flask_server" || echo "No backend running"
echo "🛑 Previous backend stopped."

# -----------------------------
# Start backend (Flask) serving frontend
# -----------------------------
echo "⚡ Starting backend on $HOST_IP:6001..."
source venv/bin/activate
nohup python3 -m src.flask_server > "$SCRIPT_DIR/backend.log" 2>&1 &
deactivate

echo "✅ Backend started. Logs: $SCRIPT_DIR/backend.log"
echo "🌐 Access frontend via: http://$HOST_IP:7001 (if dev) or served by backend at http://$HOST_IP:6001"
