#!/bin/bash
set -e

# ------------------------------
# Dev Environment Startup Script
# ------------------------------

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

# Hosts and ports
FRONTEND_HOST="0.0.0.0"
FRONTEND_PORT=7001
BACKEND_HOST="0.0.0.0"
BACKEND_PORT=6001

echo "🧹 Stopping any existing frontend/backend..."
pkill -f "python3 -m src.flask_server" || true
pkill -f "vite" || true
sleep 2

echo "🔧 Ensuring logs exist and are writable..."
touch frontend.log backend.log
chmod 664 frontend.log backend.log

# ------------------------------
# Backend Start
# ------------------------------
cd Backend
source venv/bin/activate
nohup python3 -m src.flask_server --host $BACKEND_HOST --port $BACKEND_PORT > ../backend.log 2>&1 &
deactivate
cd ..

# ------------------------------
# Frontend Start
# ------------------------------
cd Frontend
echo "VITE_API_BASE_URL=http://$BACKEND_HOST:$BACKEND_PORT" > .env.local
nohup node node_modules/vite/bin/vite.js --host $FRONTEND_HOST --port $FRONTEND_PORT > ../frontend.log 2>&1 &
cd ..

echo "✅ Dev servers started!"
echo "Frontend: http://$FRONTEND_HOST:$FRONTEND_PORT"
echo "Backend:  http://$BACKEND_HOST:$BACKEND_PORT"
echo "Logs: frontend.log | backend.log"
