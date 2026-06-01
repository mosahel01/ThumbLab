#!/usr/bin/env bash
set -e

ROOT="$(cd "$(dirname "$0")" && pwd)"

echo "=== Starting ThumbLab ==="

# Activate venv and start backend
echo "[backend] Starting API server on :8000..."
source "$ROOT/.venv/bin/activate"
cd "$ROOT/backend"
python3 -m uvicorn main:app --port 8000 --reload &
BACKEND_PID=$!

# Start frontend dev server
echo "[frontend] Starting dev server on :5173..."
cd "$ROOT/frontend"
npm run dev &
FRONTEND_PID=$!

echo ""
echo "  Backend  → http://localhost:8000"
echo "  Frontend → http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop both."

trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit 0" INT TERM
wait
