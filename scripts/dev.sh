 #!/bin/bash

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

FRONTEND_HOST="192.168.10.41"
FRONTEND_PORT=7001
BACKEND_HOST="192.168.10.41"
BACKEND_PORT=6001

echo "🧹 Stopping previous servers..."
pkill -f "python3 -m src.flask_server" 2>/dev/null || echo "No backend running"
pkill -f "vite" 2>/dev/null || echo "No frontend running"
sleep 2

echo "🔧 Ensuring logs exist and writable..."
touch frontend.log backend.log
chmod 664 frontend.log backend.log

# Start Backend
echo "⚡ Starting Backend..."
cd Backend
source venv/bin/activate
nohup python3 -m src.flask_server --host "$BACKEND_HOST" --port "$BACKEND_PORT" > ../backend.log 2>&1 &
deactivate
cd ..

# Start Frontend
echo "🚀 Starting Frontend..."
cd Frontend
echo "VITE_API_BASE_URL=http://$BACKEND_HOST:$BACKEND_PORT" > .env.local
nohup node node_modules/vite/bin/vite.js --host "$FRONTEND_HOST" --port "$FRONTEND_PORT" > ../frontend.log 2>&1 &
cd ..

echo "✅ Servers started!"
echo "Frontend: http://$FRONTEND_HOST:$FRONTEND_PORT"
echo "Backend: http://$BACKEND_HOST:$BACKEND_PORT"
