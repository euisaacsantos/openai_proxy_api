# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY api ./api

# Expose port (Fly.io will set the PORT env var)
EXPOSE 8080

# Run uvicorn server
CMD uvicorn api.index:app --host 0.0.0.0 --port ${PORT:-8080}
