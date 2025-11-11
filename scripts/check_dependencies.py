#!/usr/bin/env python3
"""
Скрипт проверки и установки зависимостей.
Автоматически проверяет наличие всех необходимых пакетов.
"""
import sys
import subprocess
from pathlib import Path

def check_module(module_name):
    """Проверить наличие модуля"""
    try:
        __import__(module_name)
        return True
    except ImportError:
        return False

# Список критически важных модулей
CRITICAL_MODULES = {
    'telegram': 'python-telegram-bot>=21.1.1',
    'sqlalchemy': 'sqlalchemy>=2.0.29',
    'psycopg2': 'psycopg2-binary>=2.9.9',
    'celery': 'celery>=5.4.0',
    'redis': 'redis>=5.0.4',
    'dotenv': 'python-dotenv>=1.0.1',
    'google.generativeai': 'google-generativeai>=0.5.4',
}

# Опциональные модули
OPTIONAL_MODULES = {
    'pandas': 'pandas>=2.2.2',
    'openpyxl': 'openpyxl>=3.1.2',
    'fitz': 'PyMuPDF>=1.24.4',
    'docx': 'python-docx>=1.1.0',
    'pydub': 'pydub>=0.25.1',
    'openai': 'openai>=1.12.0',
    'bs4': 'beautifulsoup4>=4.12.3',
    'requests': 'requests>=2.31.0',
    'matplotlib': 'matplotlib>=3.8.0',
    'reportlab': 'reportlab>=4.0.0',
}

def main():
    print("=" * 60)
    print("🔍 ПРОВЕРКА ЗАВИСИМОСТЕЙ")
    print("=" * 60)
    print()

    missing_critical = []
    missing_optional = []

    # Проверка критически важных модулей
    print("📦 Критически важные модули:")
    for module, package in CRITICAL_MODULES.items():
        if check_module(module):
            print(f"  ✅ {module:<30} установлен")
        else:
            print(f"  ❌ {module:<30} ОТСУТСТВУЕТ!")
            missing_critical.append(package)

    print()

    # Проверка опциональных модулей
    print("📦 Опциональные модули (для расширенных функций):")
    for module, package in OPTIONAL_MODULES.items():
        if check_module(module):
            print(f"  ✅ {module:<30} установлен")
        else:
            print(f"  ⚠️  {module:<30} отсутствует (опционально)")
            missing_optional.append(package)

    print()
    print("=" * 60)

    if missing_critical:
        print()
        print("🔴 КРИТИЧЕСКИЕ МОДУЛИ ОТСУТСТВУЮТ!")
        print()
        print("Бот НЕ СМОЖЕТ работать без этих модулей.")
        print()
        print("Для установки выполните:")
        print()
        print("  pip install " + " ".join(missing_critical))
        print()
        print("Или установите все зависимости:")
        print()
        print("  pip install -r requirements.txt")
        print()
        return 1

    if missing_optional:
        print()
        print("⚠️  ОПЦИОНАЛЬНЫЕ МОДУЛИ ОТСУТСТВУЮТ")
        print()
        print("Некоторые функции будут недоступны:")
        print("  - Excel обработка (pandas, openpyxl)")
        print("  - PDF обработка (PyMuPDF)")
        print("  - Word обработка (python-docx)")
        print("  - Аудио обработка (pydub)")
        print("  - Веб-скрапинг (beautifulsoup4, requests)")
        print("  - Транскрибация (openai)")
        print("  - Визуализация (matplotlib)")
        print("  - Экспорт в PDF (reportlab)")
        print()
        print("Для установки всех функций:")
        print()
        print("  pip install " + " ".join(missing_optional))
        print()

        response = input("Установить опциональные модули сейчас? (y/n): ").strip().lower()
        if response == 'y':
            print()
            print("📥 Установка опциональных модулей...")
            subprocess.run([sys.executable, "-m", "pip", "install"] + missing_optional)
            print()
            print("✅ Установка завершена!")
            return 0
        else:
            print()
            print("⏭️  Пропускаем установку опциональных модулей.")
            print("   Бот будет работать с ограниченным функционалом.")
            return 0

    print()
    print("✅ ВСЕ ЗАВИСИМОСТИ УСТАНОВЛЕНЫ!")
    print()
    print("Бот готов к работе! 🚀")
    print()
    return 0

if __name__ == "__main__":
    sys.exit(main())
