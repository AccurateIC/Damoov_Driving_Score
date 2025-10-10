#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

FRONTEND_HOST="0.0.0.0"
FRONTEND_PORT=7001
BACKEND_HOST="0.0.0.0"
BACKEND_PORT=6001

# Stop old processes
pkill -f "python3 -m src.flask_server" || true
pkill -f "vite" || true
sleep 2

# Ensure logs exist
touch frontend.log backend.log
chmod 664 frontend.log backend.log

# Start backend
cd Backend
source venv/bin/activate
nohup python3 -m src.flask_server --host $BACKEND_HOST --port $BACKEND_PORT > ../backend.log 2>&1 &
deactivate
cd ..

# Start frontend
cd Frontend
echo "VITE_API_BASE_URL=http://$BACKEND_HOST:$BACKEND_PORT" > .env
nohup node node_modules/vite/bin/vite.js --host $FRONTEND_HOST --port $FRONTEND_PORT > ../frontend.log 2>&1 &
cd ..

echo "✅ Servers started!"
echo "Frontend: http://$FRONTEND_HOST:$FRONTEND_PORT"
echo "Backend: http://$BACKEND_HOST:$BACKEND_PORT"
