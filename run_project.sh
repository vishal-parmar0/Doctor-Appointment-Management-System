#!/bin/bash

echo "🚀 Starting MediBook Full-Stack Project..."

# 1. Kill any existing servers to prevent "Address already in use" errors
echo "🧹 Cleaning up old processes..."
fuser -k 5000/tcp 2>/dev/null
fuser -k 5500/tcp 2>/dev/null

# 2. Start Backend
echo "⚙️ Starting Python Backend on Port 5000..."
export PYTHONPATH=$(pwd)/backend
python3 backend/app.py &

# 3. Start Frontend
echo "🌐 Starting UI on Port 5500..."
cd frontend
python3 -m http.server 5500 &

echo "✅ Project is beautifully running!"
echo "👉 Click here to view it natively: http://localhost:5500/index.html"
echo "Press Ctrl+C to stop servers when you are done."

# Wait indefinitely so the user can see logs and stop with Ctrl+C
wait
