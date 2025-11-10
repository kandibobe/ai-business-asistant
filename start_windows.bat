@echo off
REM Windows Batch Script для запуска AI Business Assistant API

echo ========================================
echo AI Business Assistant - API Server
echo ========================================
echo.

REM Проверяем наличие виртуального окружения
if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found!
    echo Please create it first: python -m venv venv
    pause
    exit /b 1
)

REM Активируем виртуальное окружение
echo [1/3] Activating virtual environment...
call venv\Scripts\activate.bat

REM Проверяем наличие .env файла
if not exist ".env" (
    echo [WARNING] .env file not found!
    echo Please create .env file with DATABASE_URL, JWT_SECRET, and GEMINI_API_KEY
    echo.
    echo Example .env:
    echo DATABASE_URL=postgresql://postgres:password@localhost:5432/ai_business_assistant
    echo JWT_SECRET=your-secret-key-here
    echo GEMINI_API_KEY=your-gemini-key-here
    echo.
    pause
    exit /b 1
)

echo [2/3] Loading environment variables...
echo [3/3] Starting API server...
echo.
echo ========================================
echo API will be available at:
echo - http://localhost:8000
echo - API Docs: http://localhost:8000/api/docs
echo ========================================
echo.
echo Press Ctrl+C to stop the server
echo.

REM Запускаем uvicorn
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

pause
