@echo off
REM Скрипт для запуска AI Business Assistant на Windows

echo ========================================
echo AI Business Intelligence Agent v2.0
echo ========================================
echo.

REM Проверяем виртуальное окружение
if not exist ".venv\Scripts\activate.bat" (
    echo [ERROR] Виртуальное окружение не найдено!
    echo Пожалуйста, создайте его: python -m venv .venv
    pause
    exit /b 1
)

REM Активируем виртуальное окружение
echo [1/5] Активация виртуального окружения...
call .venv\Scripts\activate.bat

REM Проверяем .env файл
if not exist ".env" (
    echo [ERROR] Файл .env не найден!
    echo Пожалуйста, создайте его на основе .env.example
    pause
    exit /b 1
)

echo [2/5] Проверка зависимостей...
pip install -q -r requirements.txt

echo [3/5] Запуск миграции базы данных...
python migrate_db.py
if errorlevel 1 (
    echo [ERROR] Ошибка при миграции базы данных!
    pause
    exit /b 1
)

echo.
echo [4/5] Запуск Celery worker в фоновом режиме...
echo Примечание: На Windows Celery работает в режиме 'solo' (один процесс)
start "Celery Worker" cmd /k "call .venv\Scripts\activate.bat && celery -A celery_app worker --loglevel=info --pool=solo"

timeout /t 3 /nobreak >nul

echo [5/5] Запуск Telegram бота...
echo.
echo ========================================
echo Бот готов к работе!
echo ========================================
python main.py

REM При завершении main.py, закрываем Celery
taskkill /FI "WINDOWTITLE eq Celery Worker*" /T /F >nul 2>&1
