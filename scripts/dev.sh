#!/bin/bash
set -e

# ====================================================
# Dev Environment Startup Script for Damoov_Driving_Score
# ====================================================

# ---- Configuration ----
FRONTEND_HOST="192.168.10.41"
FRONTEND_PORT=7001
BACKEND_HOST="192.168.10.41"
BACKEND_PORT=6001

# ---- Move to workspace root ----
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

echo "==============================================="
echo "🚀 Starting Damoov Dev Environment"
echo "Frontend: http://$FRONTEND_HOST:$FRONTEND_PORT"
echo "Backend:  http://$BACKEND_HOST:$BACKEND_PORT"
echo "==============================================="

# ---- Stop previous processes ----
echo "🧹 Stopping any existing frontend/backend..."
pkill -f "python3 -m src.flask_server" 2>/dev/null || echo "No backend running"
pkill -f "vite" 2>/dev/null || echo "No frontend running"
sleep 3  # wait for ports to free

# ---- Ensure logs exist and are writable ----
touch frontend.log backend.log
chmod 664 frontend.log backend.log

# ---- Start Backend ----
echo "⚡ Starting Backend (Flask)..."
cd Backend

# Activate existing virtual environment
source venv/bin/activate

# Start backend in detached mode
nohup setsid python3 -m src.flask_server --host "$BACKEND_HOST" --port "$BACKEND_PORT" > ../backend.log 2>&1 &
deactivate
cd ..

# ---- Start Frontend ----
echo "🌐 Starting Frontend (Vite)..."
cd Frontend

# Set backend API URL for frontend
echo "VITE_API_BASE_URL=http://$BACKEND_HOST:$BACKEND_PORT" > .env.local

# Start frontend in detached mode
nohup setsid node node_modules/vite/bin/vite.js --host "$FRONTEND_HOST" --port "$FRONTEND_PORT" > ../frontend.log 2>&1 &
cd ..

echo "✅ Dev servers started successfully!"
echo "-----------------------------------------------"
echo "Frontend: http://$FRONTEND_HOST:$FRONTEND_PORT"
echo "Backend:  http://$BACKEND_HOST:$BACKEND_PORT"
echo "Logs: frontend.log | backend.log"
echo "-----------------------------------------------"
