@echo off
REM Quick start script for Windows
REM AI Business Assistant

echo ========================================
echo  AI Business Assistant - Quick Start
echo ========================================
echo.

REM Check if venv exists
if not exist ".venv\" (
    echo [ERROR] Virtual environment not found!
    echo Please run: python -m venv .venv
    echo.
    pause
    exit /b 1
)

REM Activate venv
echo [1/3] Activating virtual environment...
call .venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo [ERROR] Failed to activate venv
    pause
    exit /b 1
)

REM Check if .env exists
if not exist ".env" (
    echo.
    echo [WARNING] .env file not found!
    echo Please copy .env.example to .env and fill in your API keys
    echo.
    echo Creating .env from .env.example...
    copy .env.example .env
    echo.
    echo Please edit .env file and add your API keys, then run this script again.
    echo.
    pause
    exit /b 1
)

REM Apply database migrations
echo [2/3] Applying database migrations...
python upgrade_db.py
if %errorlevel% neq 0 (
    echo.
    echo [WARNING] Database migration failed
    echo Make sure PostgreSQL is running and .env is configured correctly
    echo.
    pause
)

REM Start the bot
echo [3/3] Starting AI Business Assistant bot...
echo.
echo ========================================
echo  Bot is starting...
echo  Press Ctrl+C to stop
echo ========================================
echo.
python main.py

pause
