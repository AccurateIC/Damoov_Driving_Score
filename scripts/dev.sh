#!/bin/bash

# ====================================================
# Damoov Dev Environment Startup Script
# ====================================================

# Get script directory and move to workspace root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

# -------------------- Configuration --------------------
FRONTEND_HOST="192.168.10.41"
FRONTEND_PORT=7001

BACKEND_HOST="192.168.10.41"
BACKEND_PORT=6001

# -------------------- Stop previous servers --------------------
echo "🧹 Stopping any existing frontend/backend..."
pkill -f "python3 -m src.flask_server" 2>/dev/null || echo "No backend running"
pkill -f "vite" 2>/dev/null || echo "No frontend running"
sleep 2

# -------------------- Ensure logs exist --------------------
echo "🔧 Ensuring logs exist and are writable..."
touch frontend.log backend.log
chmod 664 frontend.log backend.log

# -------------------- Start Backend --------------------
echo "⚡ Starting Backend (Flask Server)..."
cd Backend
source venv/bin/activate
nohup python3 -m src.flask_server --host "$BACKEND_HOST" --port "$BACKEND_PORT" > ../backend.log 2>&1 &
deactivate
cd ..

# -------------------- Update Frontend .env --------------------
echo "🌐 Updating Frontend .env..."
cd Frontend
cat > .env <<EOL
VITE_API_BASE_URL=http://$BACKEND_HOST:$BACKEND_PORT
EOL

# -------------------- Start Frontend --------------------
echo "🚀 Starting Frontend (Vite)..."
nohup node node_modules/vite/bin/vite.js --host "$FRONTEND_HOST" --port "$FRONTEND_PORT" > ../frontend.log 2>&1 &
cd ..

# -------------------- Summary --------------------
echo "✅ Dev servers started successfully!"
echo "Frontend: http://$FRONTEND_HOST:$FRONTEND_PORT"
echo "Backend:  http://$BACKEND_HOST:$BACKEND_PORT"
echo "Logs: frontend.log | backend.log"
