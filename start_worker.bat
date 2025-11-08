@echo off
REM Скрипт для запуска только Celery worker на Windows

echo ========================================
echo Запуск Celery Worker (Windows)
echo ========================================
echo.

REM Активируем виртуальное окружение
if not exist ".venv\Scripts\activate.bat" (
    echo [ERROR] Виртуальное окружение не найдено!
    pause
    exit /b 1
)

call .venv\Scripts\activate.bat

echo Запуск Celery worker в режиме 'solo' (оптимизировано для Windows)...
echo.

celery -A celery_app worker --loglevel=info --pool=solo

pause
