#!/bin/bash

echo "================================"
echo "AI Business Assistant - Launcher"
echo "================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo -e "${RED}[ERROR]${NC} Python not found! Please install Python 3.9+"
    exit 1
fi

PYTHON_CMD=$(command -v python3 || command -v python)

# Check Node.js
if ! command -v node &> /dev/null; then
    echo -e "${RED}[ERROR]${NC} Node.js not found! Please install Node.js 18+"
    exit 1
fi

# Check Docker
if ! command -v docker &> /dev/null; then
    echo -e "${YELLOW}[WARNING]${NC} Docker not found! Make sure PostgreSQL and Redis are running."
    echo ""
else
    echo -e "${GREEN}[1/5]${NC} Starting Docker services..."
    docker-compose up -d
    echo "Done!"
    echo ""
fi

# Check .env file
if [ ! -f .env ]; then
    echo -e "${RED}[ERROR]${NC} .env file not found!"
    echo "Please create .env file:"
    echo "  1. cp .env.example .env"
    echo "  2. Fill in your API keys"
    exit 1
fi

# Activate virtual environment if exists
echo -e "${GREEN}[2/5]${NC} Activating Python virtual environment..."
if [ -f venv/bin/activate ]; then
    source venv/bin/activate
elif [ -f .venv/bin/activate ]; then
    source .venv/bin/activate
else
    echo -e "${YELLOW}[WARNING]${NC} Virtual environment not found"
fi
echo "Done!"
echo ""

# Apply database migrations
echo -e "${GREEN}[3/5]${NC} Applying database migrations..."
$PYTHON_CMD upgrade_db.py 2>/dev/null || echo "Migration skipped"
echo "Done!"
echo ""

# Start Backend API in background
echo -e "${GREEN}[4/5]${NC} Starting Backend API..."
cd api
$PYTHON_CMD main.py > ../backend.log 2>&1 &
BACKEND_PID=$!
cd ..
sleep 2
echo "Done! (PID: $BACKEND_PID)"
echo ""

# Start Web App in background
echo -e "${GREEN}[5/5]${NC} Starting Web Application..."
cd web-app
npm run dev > ../web.log 2>&1 &
WEB_PID=$!
cd ..
sleep 2
echo "Done! (PID: $WEB_PID)"
echo ""

echo "================================"
echo "All services started!"
echo "================================"
echo ""
echo -e "Web App:    ${GREEN}http://localhost:3000${NC}"
echo -e "Backend:    ${GREEN}http://localhost:8000${NC}"
echo -e "API Docs:   ${GREEN}http://localhost:8000/docs${NC}"
echo ""
echo -e "Backend PID: ${YELLOW}$BACKEND_PID${NC}"
echo -e "Web PID:     ${YELLOW}$WEB_PID${NC}"
echo ""
echo "To start Telegram bot, run: $PYTHON_CMD main.py"
echo ""
echo "View logs:"
echo "  Backend: tail -f backend.log"
echo "  Web:     tail -f web.log"
echo ""
echo "To stop all services:"
echo "  kill $BACKEND_PID $WEB_PID"
echo "  docker-compose down"
echo ""

# Wait for user input
read -p "Press Enter to stop all services and exit..."

# Stop services
echo "Stopping services..."
kill $BACKEND_PID $WEB_PID 2>/dev/null
docker-compose down
echo "Done!"
