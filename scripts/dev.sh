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

# ---- Move to script root directory ----
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "==============================================="
echo "🚀 Starting Damoov Dev Environment"
echo "Frontend: http://$FRONTEND_HOST:$FRONTEND_PORT"
echo "Backend:  http://$BACKEND_HOST:$BACKEND_PORT"
echo "==============================================="

# ---- Stop previous processes ----
echo "🧹 Stopping any existing frontend/backend..."
pkill -f "python3 -m src.flask_server" 2>/dev/null || true
pkill -f "vite" 2>/dev/null || true
sleep 2

# ---- Fix Permissions ----
echo "🔧 Fixing workspace permissions..."
sudo chown -R jenkins:jenkins "$SCRIPT_DIR"
sudo chmod -R 775 "$SCRIPT_DIR"

# ====================================================
# BACKEND START
# ====================================================
echo "⚡ Starting Backend (Flask)..."
cd Backend

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
fi

# Start backend in background
nohup python3 -m src.flask_server --host "$BACKEND_HOST" --port "$BACKEND_PORT" > ../backend.log 2>&1 &
deactivate
cd ..

# ====================================================
# FRONTEND START
# ====================================================
echo "🌐 Starting Frontend (Vite)..."
cd Frontend

# Update environment to point to backend API
echo "VITE_API_BASE_URL=http://$BACKEND_HOST:$BACKEND_PORT" > .env.local

nohup node node_modules/vite/bin/vite.js --host "$FRONTEND_HOST" --port "$FRONTEND_PORT" > ../frontend.log 2>&1 &
cd ..

echo "✅ Servers started successfully!"
echo "-----------------------------------------------"
echo "Frontend: http://$FRONTEND_HOST:$FRONTEND_PORT"
echo "Backend:  http://$BACKEND_HOST:$BACKEND_PORT"
echo "Logs: frontend.log | backend.log"
echo "-----------------------------------------------"
