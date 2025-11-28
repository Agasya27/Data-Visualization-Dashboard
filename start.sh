#!/usr/bin/env bash
set -euo pipefail

echo "[start.sh] Python version: $(python --version 2>&1)"

if [ -f "requirements.txt" ]; then
  echo "[start.sh] Installing dependencies from requirements.txt"
  pip install --no-cache-dir -r requirements.txt
elif [ -f "backend/requirements.txt" ]; then
  echo "[start.sh] Installing dependencies from backend/requirements.txt"
  pip install --no-cache-dir -r backend/requirements.txt
else
  echo "[start.sh] No requirements.txt found; continuing"
fi

export PORT="${PORT:-8000}"
echo "[start.sh] Starting Uvicorn on port ${PORT}"
exec uvicorn backend.app.main:app --host 0.0.0.0 --port "${PORT}"
