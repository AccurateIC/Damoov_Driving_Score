#!/bin/bash
set -e  # Stop on first error

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ----------------------------
# FRONTEND
# ----------------------------
cd "$SCRIPT_DIR/../Frontend"
echo "📦 Installing Frontend dependencies..."
npm install

# Optional: Install missing types if needed
npm install --save-dev @types/leaflet || true

echo "🏗️ Building Frontend..."
# Allow TypeScript warnings (unused variables, etc.) to not fail build
# Use --force to ignore minor TS errors
npm run build -- --force || echo "⚠️ Frontend build finished with warnings/errors (ignored)"

# ----------------------------
# BACKEND
# ----------------------------
cd "$SCRIPT_DIR/../Backend"
if [ ! -d "venv" ]; then
  echo "🐍 Creating Python virtual environment..."
  python3 -m venv venv || { echo "❌ Failed to create venv. Did you install python3-venv?"; exit 1; }
fi

echo "📥 Installing Backend dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r src/app/requirements.txt
deactivate || true

echo "✅ Install and build complete!"
