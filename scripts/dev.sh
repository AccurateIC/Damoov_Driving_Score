#!/bin/bash

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

# Frontend/backend host & ports
FRONTEND_HOST="192.168.10.41"
FRONTEND_PORT=7001
BACKEND_HOST="0.0.0.0"
BACKEND_PORT=6001

echo "Stopping any previously running frontend/backend..."
pkill -f "python3 -m src.flask_server" 2>/dev/null || echo "No backend running"
pkill -f "vite" 2>/dev/null || echo "No frontend running"
sleep 2

# Ensure logs exist
sudo touch frontend.log backend.log
sudo chmod 664 frontend.log backend.log

# -------------------------------
# Start Backend
# -------------------------------
cd Backend
echo "⚡ Starting Backend (Flask Server)..."
source venv/bin/activate

nohup python3 -m src.flask_server > ../backend.log 2>&1 &

# Create temporary route-listing script
cat << 'EOF' > list_routes.py
from src.flask_server import app
print("\n=== BACKEND ROUTES ===")
for rule in app.url_map.iter_rules():
    print(f"{rule} -> {', '.join(rule.methods)}")
EOF

python3 list_routes.py

deactivate
cd ..

# -------------------------------
# Update Frontend .env
# -------------------------------
cd Frontend
echo "🌐 Updating frontend .env with backend URL..."
ENV_FILE=".env.local"

# If file exists, overwrite or create
echo "VITE_API_BASE_URL=http://192.168.10.41:6001" > $ENV_FILE
echo "✅ .env.local updated: VITE_API_BASE_URL=http://192.168.10.41:6001"
cd ..

# -------------------------------
# Start Frontend
# -------------------------------
cd Frontend
echo "🚀 Starting Frontend with Vite..."
nohup node node_modules/vite/bin/vite.js --host $FRONTEND_HOST --port $FRONTEND_PORT > ../frontend.log 2>&1 &
cd ..

echo "✅ Dev servers started!"
echo "Frontend: http://$FRONTEND_HOST:$FRONTEND_PORT"
echo "Backend: http://$BACKEND_HOST:$BACKEND_PORT"
echo "Logs: frontend.log | backend.log"
