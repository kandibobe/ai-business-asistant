@echo off
REM ============================================================================
REM AI Business Assistant - Windows Setup Script
REM ============================================================================
REM
REM This script automates the setup process for Windows users
REM It will:
REM 1. Check Python version
REM 2. Create virtual environment
REM 3. Install dependencies
REM 4. Check .env configuration
REM 5. Setup database
REM 6. Provide instructions for running the bot
REM
REM ============================================================================

echo ============================================================================
echo     AI Business Assistant - Windows Setup
echo ============================================================================
echo.

REM Check if Python is installed
echo [1/7] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python 3.10+ from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

python --version
echo [OK] Python is installed
echo.

REM Check Python version (should be 3.10+)
for /f "tokens=2" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo Python version: %PYTHON_VERSION%
echo NOTE: Python 3.10-3.12 recommended. Python 3.13 is supported but may have compatibility issues.
echo.

REM Check if virtual environment exists
echo [2/7] Setting up virtual environment...
if exist ".venv" (
    echo Virtual environment already exists
) else (
    echo Creating virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
)
echo.

REM Activate virtual environment
echo [3/7] Activating virtual environment...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit /b 1
)
echo [OK] Virtual environment activated
echo.

REM Upgrade pip
echo [4/7] Upgrading pip...
python -m pip install --upgrade pip
echo.

REM Install dependencies
echo [5/7] Installing dependencies...
echo This may take a few minutes...
pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo [WARNING] Some packages failed to install
    echo This might be due to Python 3.13 compatibility issues
    echo.
    echo TROUBLESHOOTING:
    echo 1. Try using Python 3.10 or 3.11 instead
    echo 2. Install Visual C++ Build Tools if you haven't:
    echo    https://visualstudio.microsoft.com/visual-cpp-build-tools/
    echo 3. For PyMuPDF issues, try: pip install --upgrade PyMuPDF
    echo.
    pause
) else (
    echo [OK] All dependencies installed successfully
)
echo.

REM Check .env file
echo [6/7] Checking .env configuration...
if exist ".env" (
    echo [OK] .env file exists
    echo.
    echo Please verify your .env file contains:
    echo   - TELEGRAM_BOT_TOKEN
    echo   - GEMINI_API_KEY
    echo   - REDIS_URL
    echo   - Database credentials
) else (
    echo [WARNING] .env file not found!
    echo.
    if exist ".env.example" (
        echo Creating .env from .env.example...
        copy .env.example .env
        echo.
        echo [ACTION REQUIRED] Please edit .env file and add your API keys:
        echo   1. TELEGRAM_BOT_TOKEN (get from @BotFather)
        echo   2. GEMINI_API_KEY (get from https://makersuite.google.com/)
        echo   3. OPENAI_API_KEY (optional, for audio transcription)
        echo.
        echo Press any key to open .env file in notepad...
        pause >nul
        notepad .env
    ) else (
        echo [ERROR] .env.example not found!
        echo Please create .env file manually
    )
)
echo.

REM Check if Docker is running (for PostgreSQL and Redis)
echo [7/7] Checking Docker...
docker --version >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Docker is not installed or not running
    echo.
    echo You have two options:
    echo.
    echo OPTION 1 - Use Docker (Recommended):
    echo   1. Install Docker Desktop: https://www.docker.com/products/docker-desktop/
    echo   2. Start Docker Desktop
    echo   3. Run: docker-compose up -d
    echo.
    echo OPTION 2 - Manual installation:
    echo   1. Install PostgreSQL: https://www.postgresql.org/download/windows/
    echo   2. Install Redis: https://github.com/microsoftarchive/redis/releases
    echo   3. Create database and user (see QUICKSTART.md)
    echo   4. Update .env with your database credentials
    echo.
) else (
    docker --version
    echo [OK] Docker is installed
    echo.
    echo To start the infrastructure (PostgreSQL + Redis):
    echo   docker-compose up -d
    echo.
    echo To check status:
    echo   docker-compose ps
    echo.
)

echo ============================================================================
echo     Setup Complete!
echo ============================================================================
echo.
echo NEXT STEPS:
echo.
echo 1. Make sure Docker is running (or PostgreSQL/Redis manually)
echo    docker-compose up -d
echo.
echo 2. Apply database migrations:
echo    alembic upgrade head
echo.
echo 3. Start Celery worker (in a new terminal):
echo    .venv\Scripts\activate
echo    celery -A celery_app worker --loglevel=info --pool=solo
echo.
echo 4. Start the Telegram bot (in another new terminal):
echo    .venv\Scripts\activate
echo    python main.py
echo.
echo 5. (Optional) Start the REST API:
echo    .venv\Scripts\activate
echo    python run_api.py
echo.
echo 6. (Optional) Start the Web App:
echo    cd web-app
echo    npm install
echo    npm run dev
echo.
echo ============================================================================
echo For troubleshooting, see QUICKSTART.md
echo ============================================================================
echo.
pause
