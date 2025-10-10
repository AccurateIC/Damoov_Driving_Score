#!/bin/bash
set -e

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

# Explicit frontend/backend host & ports
FRONTEND_HOST="192.168.10.41"
FRONTEND_PORT=7001

BACKEND_HOST="192.168.10.41"
BACKEND_PORT=6001

echo "🛑 Stopping any previously running frontend/backend..."

# Kill any leftover Flask or Vite processes cleanly
pids=$(pgrep -f "python3 -m src.flask_server" || true)
if [ -n "$pids" ]; then
  echo "Killing old backend (Flask) processes: $pids"
  kill -9 $pids
fi

vite_pids=$(pgrep -f "vite" || true)
if [ -n "$vite_pids" ]; then
  echo "Killing old frontend (Vite) processes: $vite_pids"
  kill -9 $vite_pids
fi

# Give OS time to free ports
sleep 3

# Ensure logs exist and are writable
touch frontend.log backend.log
chmod 664 frontend.log backend.log

echo "🚀 Starting Frontend with Vite..."
cd Frontend
nohup node node_modules/vite/bin/vite.js --host "$FRONTEND_HOST" --port "$FRONTEND_PORT" > ../frontend.log 2>&1 &
cd ..

echo "⚡ Starting Backend (Flask Server)..."
cd Backend
source venv/bin/activate
nohup python3 -m src.flask_server --host "$BACKEND_HOST" --port "$BACKEND_PORT" > ../backend.log 2>&1 &
deactivate
cd ..

echo "✅ Dev servers started!"
echo "Frontend: http://$FRONTEND_HOST:$FRONTEND_PORT"
echo "Backend: http://$BACKEND_HOST:$BACKEND_PORT"
echo "📜 Logs: tail -f frontend.log or backend.log (avoid using too many tail -f simultaneously)"
