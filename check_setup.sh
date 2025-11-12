#!/bin/bash

# ==============================================================================
# Setup Checker Script for AI Business Assistant
# ==============================================================================
# This script checks if your environment is ready to run the bot
# ==============================================================================

echo "🔍 Checking AI Business Assistant Setup..."
echo "============================================="
echo ""

ERRORS=0
WARNINGS=0

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# ==============================================================================
# 1. Check Python version
# ==============================================================================
echo "📌 Checking Python version..."
PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
REQUIRED_VERSION="3.10"

if python -c "import sys; exit(0 if sys.version_info >= (3, 10) else 1)"; then
    echo -e "${GREEN}✓${NC} Python $PYTHON_VERSION (>= 3.10 required)"
else
    echo -e "${RED}✗${NC} Python $PYTHON_VERSION is too old (>= 3.10 required)"
    ERRORS=$((ERRORS + 1))
fi
echo ""

# ==============================================================================
# 2. Check .env file
# ==============================================================================
echo "📌 Checking .env file..."
if [ -f ".env" ]; then
    echo -e "${GREEN}✓${NC} .env file exists"

    # Check critical variables
    if grep -q "TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here" .env; then
        echo -e "${YELLOW}⚠${NC}  TELEGRAM_BOT_TOKEN not configured (using example value)"
        WARNINGS=$((WARNINGS + 1))
    else
        echo -e "${GREEN}✓${NC} TELEGRAM_BOT_TOKEN configured"
    fi

    if grep -q "GEMINI_API_KEY=your_gemini_api_key_here" .env; then
        echo -e "${YELLOW}⚠${NC}  GEMINI_API_KEY not configured (using example value)"
        WARNINGS=$((WARNINGS + 1))
    else
        echo -e "${GREEN}✓${NC} GEMINI_API_KEY configured"
    fi
else
    echo -e "${RED}✗${NC} .env file missing"
    echo "   Run: cp .env.example .env"
    ERRORS=$((ERRORS + 1))
fi
echo ""

# ==============================================================================
# 3. Check Docker
# ==============================================================================
echo "📌 Checking Docker..."
if command -v docker &> /dev/null; then
    echo -e "${GREEN}✓${NC} Docker installed ($(docker --version))"

    if docker ps &> /dev/null; then
        echo -e "${GREEN}✓${NC} Docker daemon running"
    else
        echo -e "${RED}✗${NC} Docker daemon not running"
        echo "   Start Docker Desktop or run: sudo systemctl start docker"
        ERRORS=$((ERRORS + 1))
    fi
else
    echo -e "${YELLOW}⚠${NC}  Docker not found (optional if running without Docker)"
    WARNINGS=$((WARNINGS + 1))
fi
echo ""

# ==============================================================================
# 4. Check Python dependencies
# ==============================================================================
echo "📌 Checking Python dependencies..."
if pip show python-telegram-bot &> /dev/null; then
    echo -e "${GREEN}✓${NC} python-telegram-bot installed"
else
    echo -e "${RED}✗${NC} python-telegram-bot not installed"
    echo "   Run: pip install -r requirements.txt"
    ERRORS=$((ERRORS + 1))
fi

if pip show pydantic &> /dev/null; then
    echo -e "${GREEN}✓${NC} pydantic installed"
else
    echo -e "${RED}✗${NC} pydantic not installed"
    echo "   Run: pip install -r requirements.txt"
    ERRORS=$((ERRORS + 1))
fi

if pip show sqlalchemy &> /dev/null; then
    echo -e "${GREEN}✓${NC} sqlalchemy installed"
else
    echo -e "${RED}✗${NC} sqlalchemy not installed"
    echo "   Run: pip install -r requirements.txt"
    ERRORS=$((ERRORS + 1))
fi
echo ""

# ==============================================================================
# 5. Check database files
# ==============================================================================
echo "📌 Checking required files..."
REQUIRED_FILES=("main.py" "tasks.py" "celery_app.py" "docker-compose.yml" "requirements.txt")

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC} $file exists"
    else
        echo -e "${RED}✗${NC} $file missing"
        ERRORS=$((ERRORS + 1))
    fi
done
echo ""

# ==============================================================================
# 6. Check web app (optional)
# ==============================================================================
echo "📌 Checking web application..."
if [ -d "web-app" ] && [ -f "web-app/package.json" ]; then
    echo -e "${GREEN}✓${NC} Web app configured"

    if [ -f "web-app/.env" ]; then
        echo -e "${GREEN}✓${NC} Web app .env exists"
    else
        echo -e "${YELLOW}⚠${NC}  Web app .env missing (optional)"
        echo "   Run: cd web-app && cp .env.example .env"
        WARNINGS=$((WARNINGS + 1))
    fi
else
    echo -e "${YELLOW}⚠${NC}  Web app not found (optional)"
    WARNINGS=$((WARNINGS + 1))
fi
echo ""

# ==============================================================================
# Summary
# ==============================================================================
echo "============================================="
echo "📊 Summary:"
echo "============================================="

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}✅ All checks passed! You're ready to go!${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. Configure API keys in .env file"
    echo "  2. Run: docker-compose up -d"
    echo "  3. Or without Docker:"
    echo "     - Install dependencies: pip install -r requirements.txt"
    echo "     - Start services manually (see QUICKSTART.md)"
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo -e "${YELLOW}⚠️  Setup OK with $WARNINGS warning(s)${NC}"
    echo "   Review warnings above"
    exit 0
else
    echo -e "${RED}❌ Setup has $ERRORS error(s) and $WARNINGS warning(s)${NC}"
    echo "   Fix errors above before running"
    exit 1
fi
