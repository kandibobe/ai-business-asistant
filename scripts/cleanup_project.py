#!/usr/bin/env python3
"""
Скрипт для очистки и оптимизации структуры проекта.
Удаляет дубликаты, организует файлы в папки.

Использование:
    python cleanup_project.py
"""
import os
import shutil
from pathlib import Path

print("=" * 70)
print("🧹 Очистка и оптимизация структуры проекта")
print("=" * 70)

# Создаем структуру папок
print("\n[1/5] Создание структуры папок...")

folders = {
    "docs": "Документация проекта",
    "scripts": "Скрипты запуска и установки",
}

for folder, desc in folders.items():
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"   ✅ Created {folder}/ - {desc}")
    else:
        print(f"   ℹ️  {folder}/ already exists")

# Перемещаем документацию
print("\n[2/5] Организация документации...")

docs_to_move = [
    ("FEATURES_DEMO.md", "docs/"),
    ("FIX_ERRORS.md", "docs/archive/"),  # В архив
    ("GIT_WORKFLOW.md", "docs/"),
    ("IMPROVEMENT_PLAN.md", "docs/archive/"),  # В архив
    ("INTEGRATION_GUIDE.md", "docs/"),
    ("MULTILINGUAL_GUIDE.md", "docs/"),
    ("PRODUCTION_READINESS_PLAN.md", "docs/"),
    ("QUICK_START.md", "docs/archive/"),  # Дубликат QUICKSTART.md
    ("ROADMAP.md", "docs/"),
    ("SESSION_SUMMARY.md", "docs/archive/"),  # Устаревший
    ("START_HERE.md", "docs/archive/"),  # Дубликат README
    ("TOP_10_IMPROVEMENTS.md", "docs/"),
    ("WEB_APP_PROGRESS.md", "docs/archive/"),  # Устаревший
    ("WEB_APP_README.md", "docs/"),
    ("API_README.md", "docs/"),
]

# Создаем archive
if not os.path.exists("docs/archive"):
    os.makedirs("docs/archive")

moved_count = 0
for file, dest in docs_to_move:
    if os.path.exists(file):
        dest_path = os.path.join(dest, os.path.basename(file))
        # Создаем директорию если нужно
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)

        if not os.path.exists(dest_path):
            shutil.move(file, dest_path)
            print(f"   ✅ Moved {file} -> {dest}")
            moved_count += 1
        else:
            print(f"   ℹ️  {dest_path} already exists, skipping")

print(f"   📝 Moved {moved_count} documentation files")

# Перемещаем скрипты
print("\n[3/5] Организация скриптов...")

scripts_to_move = [
    "fix_and_start.bat",
    "install_dependencies.bat",
    "start_bot.bat",
    "start_worker.bat",
    "start_api.sh",
]

scripts_moved = 0
for script in scripts_to_move:
    if os.path.exists(script):
        dest = os.path.join("scripts", script)
        if not os.path.exists(dest):
            shutil.move(script, dest)
            print(f"   ✅ Moved {script} -> scripts/")
            scripts_moved += 1

print(f"   📜 Moved {scripts_moved} script files")

# Удаляем дубликаты миграций (используем Alembic)
print("\n[4/5] Очистка старых миграций...")

old_migrations = [
    "migrate_documents.py",
    "migrate_user_preferences.py",
    "migrate_web_users.py",
]

removed_migrations = 0
for migration in old_migrations:
    if os.path.exists(migration):
        # Создаем backup в docs/archive
        backup_path = os.path.join("docs/archive", migration)
        shutil.copy2(migration, backup_path)
        os.remove(migration)
        print(f"   ✅ Removed {migration} (backed up to docs/archive/)")
        removed_migrations += 1

print(f"   🗑️  Removed {removed_migrations} old migration files")

# Создаем .gitignore для docs/archive
print("\n[5/5] Финализация...")

gitignore_archive = """# Archive files - old/deprecated documentation
# These files are kept for reference but not actively maintained
"""

with open("docs/archive/.gitignore", "w") as f:
    f.write(gitignore_archive)

print("   ✅ Created docs/archive/.gitignore")

# Создаем README для docs
docs_readme = """# 📚 Документация AI Business Assistant

## Основная документация

- **[README.md](../README.md)** - Обзор проекта
- **[QUICKSTART.md](../QUICKSTART.md)** - Быстрый старт
- **[DEPLOYMENT.md](../DEPLOYMENT.md)** - Деплой в production
- **[TESTING_GUIDE.md](../TESTING_GUIDE.md)** - Тестирование
- **[SECURITY.md](../SECURITY.md)** - Безопасность
- **[MAJOR_IMPROVEMENTS.md](../MAJOR_IMPROVEMENTS.md)** - Последние улучшения

## Дополнительная документация

- **[API_README.md](API_README.md)** - REST API документация
- **[WEB_APP_README.md](WEB_APP_README.md)** - Web приложение
- **[GIT_WORKFLOW.md](GIT_WORKFLOW.md)** - Git workflow
- **[INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)** - Интеграция
- **[MULTILINGUAL_GUIDE.md](MULTILINGUAL_GUIDE.md)** - Мультиязычность
- **[PRODUCTION_READINESS_PLAN.md](PRODUCTION_READINESS_PLAN.md)** - Production readiness
- **[ROADMAP.md](ROADMAP.md)** - Дорожная карта
- **[TOP_10_IMPROVEMENTS.md](TOP_10_IMPROVEMENTS.md)** - Топ 10 улучшений
- **[FEATURES_DEMO.md](FEATURES_DEMO.md)** - Демо возможностей

## Архив

Старая и устаревшая документация находится в [archive/](archive/).
"""

with open("docs/README.md", "w", encoding="utf-8") as f:
    f.write(docs_readme)

print("   ✅ Created docs/README.md")

# Создаем README для scripts
scripts_readme = """# 📜 Скрипты

## Windows (.bat)

- **setup.bat** - Первичная настройка проекта
- **start.bat** - Запуск бота (с миграциями)
- **start_bot.bat** - Запуск только бота
- **start_worker.bat** - Запуск Celery worker
- **install_dependencies.bat** - Установка зависимостей

## Linux/Mac (.sh)

- **start_api.sh** - Запуск REST API

## Python

- **apply_improvements.py** - Применение последних улучшений
- **cleanup_project.py** - Очистка и оптимизация структуры
- **upgrade_db.py** - Применение миграций БД

Все скрипты должны запускаться из корневой директории проекта.
"""

with open("scripts/README.md", "w", encoding="utf-8") as f:
    f.write(scripts_readme)

print("   ✅ Created scripts/README.md")

print("\n" + "=" * 70)
print("✅ Очистка завершена!")
print("=" * 70)

print("\n📊 Результаты:")
print(f"   📁 Создано папок: 3 (docs/, docs/archive/, scripts/)")
print(f"   📝 Перемещено документов: {moved_count}")
print(f"   📜 Перемещено скриптов: {scripts_moved}")
print(f"   🗑️  Удалено старых миграций: {removed_migrations}")
print(f"   ✨ Создано README файлов: 2")

print("\n📂 Новая структура:")
print("""
   ai-business-assistant/
   ├── 📄 README.md              (главная документация)
   ├── 📄 QUICKSTART.md          (быстрый старт)
   ├── 📄 DEPLOYMENT.md          (деплой)
   ├── 📄 TESTING_GUIDE.md       (тестирование)
   ├── 📄 SECURITY.md            (безопасность)
   ├── 📄 MAJOR_IMPROVEMENTS.md  (последние улучшения)
   │
   ├── 📁 docs/                  (вся документация)
   │   ├── 📄 README.md
   │   ├── 📁 archive/           (старые файлы)
   │   └── ...
   │
   ├── 📁 scripts/               (все скрипты)
   │   ├── 📄 README.md
   │   ├── setup.bat
   │   ├── start.bat
   │   └── ...
   │
   ├── 📁 api/                   (REST API)
   ├── 📁 database/              (модели и БД)
   ├── 📁 handlers/              (обработчики бота)
   ├── 📁 utils/                 (утилиты)
   │   ├── health_check.py       (новое!)
   │   ├── metrics.py            (новое!)
   │   └── ...
   │
   ├── 📄 main.py                (точка входа бота)
   ├── 📄 requirements.txt
   └── ...
""")

print("\n💡 Рекомендации:")
print("   1. Проверьте что всё работает: python main.py")
print("   2. Коммитьте изменения: git add . && git commit -m 'Clean up project structure'")
print("   3. Обновите .gitignore если нужно")
print("")
