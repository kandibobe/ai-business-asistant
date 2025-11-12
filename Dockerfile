# ==============================================================================
# Multi-Stage Dockerfile for AI Business Intelligence Agent
# ==============================================================================
# Supports: Telegram Bot, FastAPI REST API
# Build targets: base, bot, api
# ==============================================================================

# --- Stage 1: Base Image with Dependencies ---
FROM python:3.11-slim as base

# Metadata
LABEL maintainer="AI Business Assistant Team"
LABEL description="AI-powered business document analysis platform"
LABEL version="1.0.0"

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libpq-dev \
    ffmpeg \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Set working directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p downloads logs backups

# Create non-root user for security
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# --- Stage 2: Telegram Bot ---
FROM base as bot

# Metadata
LABEL service="telegram-bot"

# Expose port for health checks (optional)
EXPOSE 8080

# Health check script
HEALTHCHECK --interval=60s --timeout=10s --retries=3 --start-period=30s \
    CMD python -c "import sys; sys.exit(0)"

# Start Telegram bot
CMD ["python", "main.py"]

# --- Stage 3: FastAPI REST API ---
FROM base as api

# Metadata
LABEL service="rest-api"

# Install additional dependencies for API
RUN pip install --no-cache-dir uvicorn[standard]

# Expose API port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 --start-period=40s \
    CMD curl -f http://localhost:8000/api/health || exit 1

# Start FastAPI server
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
