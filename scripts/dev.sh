#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Stop any previously running servers
pkill -f "python3 -m src.flask_server" 2>/dev/null || echo "No backend running"
pkill -f "vite" 2>/dev/null || echo "No frontend running"
sleep 2

# -------------------------------
# Frontend: install, build, and start
# -------------------------------
(
  cd "$SCRIPT_DIR/../Frontend"

  echo "📦 Installing frontend dependencies..."
  npm install

  echo "🏗️ Building frontend..."
  npm run build

  echo "🚀 Serving frontend..."
  # Option 1: Serve production build using Vite preview
  npx vite preview --port 7001
) &

# -------------------------------
# Backend: activate venv and run
# -------------------------------
(
  cd "$SCRIPT_DIR/../Backend"

  # Activate venv
  if [ -f "venv/bin/activate" ]; then
      echo "⚡ Activating virtual environment..."
      source venv/bin/activate
  else
      echo "❌ Virtual environment not found. Creating one..."
      python3 -m venv venv
      source venv/bin/activate
      pip install -r requirements.txt
  fi

  echo "🏃 Starting Flask backend..."
  nohup python3 -m src.flask_server --host 192.168.10.41 --port 6001 > ../backend.log 2>&1 &

  deactivate
) &

# Wait for both processes
wait

echo "✅ Frontend (port 7001) and Backend (port 6001) are running!"
