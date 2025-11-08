@echo off
REM Скрипт установки всех зависимостей

echo ========================================
echo Установка зависимостей
echo AI Business Intelligence Agent v2.0
echo ========================================
echo.

REM Проверяем виртуальное окружение
if not exist ".venv\Scripts\activate.bat" (
    echo [1/3] Создание виртуального окружения...
    python -m venv .venv
    if errorlevel 1 (
        echo [ERROR] Не удалось создать виртуальное окружение!
        echo Убедитесь что Python 3.10+ установлен.
        pause
        exit /b 1
    )
    echo [OK] Виртуальное окружение создано!
) else (
    echo [1/3] Виртуальное окружение найдено.
)

echo.
echo [2/3] Активация виртуального окружения...
call .venv\Scripts\activate.bat

echo.
echo [3/3] Установка зависимостей из requirements.txt...
echo Это может занять несколько минут...
echo.

pip install --upgrade pip
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo [ERROR] Ошибка при установке зависимостей!
    echo.
    echo Возможные причины:
    echo 1. Нет подключения к интернету
    echo 2. Старая версия pip
    echo 3. Проблемы с правами доступа
    echo.
    echo Попробуйте:
    echo   python -m pip install --upgrade pip
    echo   pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo ✅ ВСЕ ЗАВИСИМОСТИ УСТАНОВЛЕНЫ!
echo ========================================
echo.
echo Проверка установленных пакетов:
python check_dependencies.py

echo.
echo Готово! Теперь вы можете запустить бота:
echo   fix_and_start.bat  (автоматически)
echo   или
echo   python main.py     (вручную)
echo.
pause
