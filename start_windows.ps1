# PowerShell Script для запуска AI Business Assistant API

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "AI Business Assistant - API Server" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Проверяем наличие виртуального окружения
if (-Not (Test-Path "venv\Scripts\Activate.ps1")) {
    Write-Host "[ERROR] Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please create it first: python -m venv venv" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Активируем виртуальное окружение
Write-Host "[1/3] Activating virtual environment..." -ForegroundColor Green
& ".\venv\Scripts\Activate.ps1"

# Проверяем наличие .env файла
if (-Not (Test-Path ".env")) {
    Write-Host "[WARNING] .env file not found!" -ForegroundColor Yellow
    Write-Host "Please create .env file with DATABASE_URL, JWT_SECRET, and GEMINI_API_KEY" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Example .env:" -ForegroundColor Cyan
    Write-Host "DATABASE_URL=postgresql://postgres:password@localhost:5432/ai_business_assistant"
    Write-Host "JWT_SECRET=your-secret-key-here"
    Write-Host "GEMINI_API_KEY=your-gemini-key-here"
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "[2/3] Loading environment variables..." -ForegroundColor Green
Write-Host "[3/3] Starting API server..." -ForegroundColor Green
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "API will be available at:" -ForegroundColor Green
Write-Host "- http://localhost:8000" -ForegroundColor White
Write-Host "- API Docs: http://localhost:8000/api/docs" -ForegroundColor White
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Запускаем uvicorn
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
