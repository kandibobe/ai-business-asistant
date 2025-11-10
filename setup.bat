@echo off
REM Setup script for Windows
REM AI Business Assistant - First time installation

echo ========================================
echo  AI Business Assistant - Setup
echo ========================================
echo.

REM Step 1: Create virtual environment
echo [Step 1/4] Creating virtual environment...
if exist ".venv\" (
    echo Virtual environment already exists
) else (
    python -m venv .venv
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create venv
        echo Please make sure Python 3.10+ is installed
        pause
        exit /b 1
    )
    echo ✅ Virtual environment created
)
echo.

REM Step 2: Activate venv
echo [Step 2/4] Activating virtual environment...
call .venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo [ERROR] Failed to activate venv
    pause
    exit /b 1
)
echo ✅ Virtual environment activated
echo.

REM Step 3: Upgrade pip and install dependencies
echo [Step 3/4] Installing dependencies...
echo This may take a few minutes...
echo.
python -m pip install --upgrade pip
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)
echo ✅ Dependencies installed
echo.

REM Step 4: Create .env file
echo [Step 4/4] Setting up configuration...
if exist ".env" (
    echo .env file already exists
) else (
    copy .env.example .env
    echo ✅ .env file created
)
echo.

echo ========================================
echo  Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Edit .env file and add your API keys:
echo    - TELEGRAM_BOT_TOKEN (from @BotFather)
echo    - GEMINI_API_KEY (from Google AI Studio)
echo.
echo 2. Make sure PostgreSQL and Redis are running:
echo    docker-compose up -d
echo.
echo 3. Run the bot:
echo    start.bat
echo.
echo See QUICKSTART.md for detailed instructions
echo.
pause
