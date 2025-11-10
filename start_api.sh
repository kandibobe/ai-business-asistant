#!/bin/bash

# AI Business Assistant - API Startup Script

echo "🚀 Starting AI Business Assistant API..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "Please create .env file with required variables:"
    echo "  - DATABASE_URL"
    echo "  - JWT_SECRET"
    echo "  - GEMINI_API_KEY"
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed!"
    exit 1
fi

# Check if required packages are installed
echo "📦 Checking dependencies..."
python3 -c "import fastapi" 2>/dev/null || {
    echo "❌ FastAPI not installed. Installing..."
    pip install fastapi uvicorn python-jose passlib bcrypt python-multipart google-generativeai
}

# Set environment
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Start API server
echo "✅ Starting API server on http://0.0.0.0:8000"
echo "📚 API Documentation: http://localhost:8000/api/docs"
echo ""

uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
