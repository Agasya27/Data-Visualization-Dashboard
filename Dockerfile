# Multi-stage build not necessary; simple Python runtime
FROM python:3.11-slim

# Ensure system deps for pandas/openpyxl if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Leverage root requirements that delegates to backend/requirements.txt
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY . .

# Environment defaults
ENV PORT=8000 \
    PYTHONUNBUFFERED=1

# Expose for documentation (Railway passes $PORT)
EXPOSE 8000

# Run FastAPI via Uvicorn; honor $PORT from platform
CMD ["sh", "-c", "uvicorn backend.app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
