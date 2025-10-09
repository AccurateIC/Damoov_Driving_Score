#!/bin/bash

# ================================
# Dev Server Startup Script
# ================================

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

# Explicit frontend/backend host & ports
FRONTEND_HOST="192.168.10.41"
FRONTEND_PORT=7001

BACKEND_HOST="192.168.10.41"
BACKEND_PORT=6001

# Logs directory
LOG_DIR="$PWD/logs"
mkdir -p "$LOG_DIR"
chmod -R 775 "$LOG_DIR"
chown -R $(whoami):$(whoami) "$LOG_DIR"

# ----------------------------
# Stop previous processes
# ----------------------------
echo "Stopping any previously running frontend/backend..."
pkill -f "python3 -m src.flask_server" 2>/dev/null || echo "No backend running"
pkill -f "vite" 2>/dev/null || echo "No frontend running"
sleep 2

# ----------------------------
# Start Frontend
# ----------------------------
cd Frontend
echo "🚀 Starting Frontend with Vite..."
nohup node node_modules/vite/bin/vite.js --host $FRONTEND_HOST --port $FRONTEND_PORT > "../logs/frontend.log" 2>&1 &
cd ..

# ----------------------------
# Start Backend
# ----------------------------
cd Backend
echo "⚡ Starting Backend (Flask Server)..."
source venv/bin/activate
nohup python3 -m src.flask_server --host $BACKEND_HOST --port $BACKEND_PORT > "../logs/backend.log" 2>&1 &
deactivate
cd ..

# ----------------------------
# Summary
# ----------------------------
echo "✅ Dev servers started!"
echo "Frontend: http://$FRONTEND_HOST:$FRONTEND_PORT"
echo "Backend: http://$BACKEND_HOST:$BACKEND_PORT"

# ----------------------------
# Health check (optional)
# ----------------------------
echo "Checking backend health..."
sleep 5
if curl -s "$BACKEND_HOST:$BACKEND_PORT/api/health" | grep -q "OK"; then
    echo "✅ Backend health OK"
else
    echo "⚠️ Backend health check failed. Check logs: $LOG_DIR/backend.log"
fi
