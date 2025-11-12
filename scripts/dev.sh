
#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Start Frontend with Vite
(
  cd "$SCRIPT_DIR/../Frontend"
  echo "🚀 Starting Frontend with Vite..."
  node node_modules/vite/bin/vite.js
) &

# Start Backend inside venv
(
  cd "$SCRIPT_DIR/../Backend"
  echo "⚡ Starting Backend (Flask Server)..."
  source venv/bin/activate
  python3 -m src.flask_server
  deactivate
) &

# Wait for both processes
wait
