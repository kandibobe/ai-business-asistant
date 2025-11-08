@echo off
REM Полная перезагрузка и исправление всех проблем

echo ========================================
echo AI Business Intelligence Agent v2.0
echo Автоматическое исправление и запуск
echo ========================================
echo.

REM Проверяем виртуальное окружение
if not exist ".venv\Scripts\activate.bat" (
    echo [ERROR] Виртуальное окружение не найдено!
    echo Создание виртуального окружения...
    python -m venv .venv
)

REM Активируем виртуальное окружение
echo [1/7] Активация виртуального окружения...
call .venv\Scripts\activate.bat

REM Проверяем .env файл
if not exist ".env" (
    echo [ERROR] Файл .env не найден!
    echo Пожалуйста, создайте его на основе .env.example
    pause
    exit /b 1
)

echo [2/7] Проверка зависимостей...
python check_dependencies.py
if errorlevel 1 (
    echo.
    echo [ВНИМАНИЕ] Некоторые зависимости отсутствуют.
    echo Устанавливаем все зависимости из requirements.txt...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Ошибка при установке зависимостей!
        pause
        exit /b 1
    )
    echo [OK] Зависимости установлены!
)

echo [3/7] Остановка всех старых процессов Celery...
taskkill /F /IM celery.exe /T >nul 2>&1

echo [4/7] Очистка кэша Python...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
del /s /q *.pyc >nul 2>&1

echo [5/7] Запуск миграции базы данных...
python migrate_db.py
if errorlevel 1 (
    echo.
    echo [ERROR] Ошибка при миграции базы данных!
    echo Проверьте:
    echo 1. PostgreSQL запущен
    echo 2. Параметры в .env корректны
    echo 3. База данных существует
    pause
    exit /b 1
)

echo.
echo [6/7] Запуск Celery worker в фоновом режиме...
echo Режим: solo (оптимизировано для Windows)
start "Celery Worker" cmd /k "call .venv\Scripts\activate.bat && celery -A celery_app worker --loglevel=info --pool=solo"

echo Ожидание запуска worker (5 секунд)...
timeout /t 5 /nobreak >nul

echo [7/7] Запуск Telegram бота...
echo.
echo ========================================
echo Все проблемы исправлены!
echo Бот готов к работе!
echo ========================================
echo.
python main.py

REM При завершении main.py, закрываем Celery
echo.
echo Остановка Celery worker...
taskkill /FI "WINDOWTITLE eq Celery Worker*" /T /F >nul 2>&1
