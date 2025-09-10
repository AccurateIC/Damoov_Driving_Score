#!/bin/bash
set -e

# Go to repo root
cd /home/ai_server/Desktop/Damoov_python_backend/repo

# Activate venv (adjust if yours is different)
source env/bin/activate

# Start Poller pipeline
python3 -u pipelines/poller/pipeline_poller.py >> pipelines/logs/poller.log 2>&1 &

export PYTHONPATH=/home/ai_server/Desktop/Damoov_python_backend/repo/pipelines:$PYTHONPATH

# Start Webapp (Flask backend)
python3 -u pipelines/webapp/flask_server.py >> pipelines/logs/webapp.log 2>&1 &

# Start Frontend
cd pipelines/webapp/Frontend

# Install dependencies if node_modules is missing
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install
fi

# Start in dev mode
npm run dev > ../../logs/frontend.log 2>&1 &

wait
