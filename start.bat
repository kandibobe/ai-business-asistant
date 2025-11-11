@echo off
echo ================================
echo AI Business Assistant - Launcher
echo ================================
echo.

REM Check Python
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python not found! Please install Python 3.9+
    pause
    exit /b 1
)

REM Check Node.js
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Node.js not found! Please install Node.js 18+
    pause
    exit /b 1
)

REM Check Docker
where docker >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [WARNING] Docker not found! Make sure PostgreSQL and Redis are running.
    echo.
) else (
    echo [1/5] Starting Docker services...
    docker-compose up -d
    echo Done!
    echo.
)

REM Check .env file
if not exist .env (
    echo [ERROR] .env file not found!
    echo Please create .env file:
    echo   1. Copy .env.example to .env
    echo   2. Fill in your API keys
    pause
    exit /b 1
)

echo [2/5] Activating Python virtual environment...
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
) else (
    echo [WARNING] Virtual environment not found
)
echo Done!
echo.

echo [3/5] Applying database migrations...
python upgrade_db.py 2>nul
echo Done!
echo.

echo [4/5] Starting Backend API...
start "AI Backend API" cmd /k "cd api && python main.py"
timeout /t 3 /nobreak >nul
echo Done!
echo.

echo [5/5] Starting Web Application...
start "AI Web App" cmd /k "cd web-app && npm run dev"
echo Done!
echo.

echo ================================
echo All services started!
echo ================================
echo.
echo Web App:    http://localhost:3000
echo Backend:    http://localhost:8000
echo API Docs:   http://localhost:8000/docs
echo.
echo To start Telegram bot, run: python main.py
echo.
pause
