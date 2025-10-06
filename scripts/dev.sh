#!/bin/bash
cd "$(dirname "$0")/.."

FRONTEND_DIR="./Frontend"
BACKEND_DIR="./Backend"

FRONTEND_PORT=7001
BACKEND_PORT=6001
FRONTEND_HOST="192.168.10.41"
BACKEND_HOST="192.168.10.41"

echo "🚀 Starting Backend..."
(cd "$BACKEND_DIR" && nohup python3 -m src.flask_server > backend.log 2>&1 &)

echo "⚡ Starting Frontend..."
(cd "$FRONTEND_DIR" && nohup npm run dev -- --host $FRONTEND_HOST --port $FRONTEND_PORT > frontend.log 2>&1 &)

echo "✅ Servers started successfully!"
echo "Frontend → http://$FRONTEND_HOST:$FRONTEND_PORT"
echo "Backend  → http://$BACKEND_HOST:$BACKEND_PORT"
