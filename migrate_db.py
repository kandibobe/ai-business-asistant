#!/usr/bin/env python3
"""
Скрипт миграции базы данных для добавления полей language и mode в таблицу users.
"""
import os
import sys
from sqlalchemy import text
from dotenv import load_dotenv

# Добавляем корневую директорию проекта в PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

from database.database import engine, SessionLocal

def migrate_add_language_mode():
    """Добавляет поля language и mode в таблицу users, если их еще нет."""
    print("🔄 Начинаем миграцию базы данных...")

    db = SessionLocal()

    try:
        # Проверяем наличие столбца language
        check_language = text("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name='users' AND column_name='language';
        """)

        result = db.execute(check_language).fetchone()

        if not result:
            print("➕ Добавляем столбец 'language' в таблицу 'users'...")
            db.execute(text("""
                ALTER TABLE users
                ADD COLUMN language VARCHAR DEFAULT 'ru';
            """))
            db.commit()
            print("✅ Столбец 'language' успешно добавлен.")
        else:
            print("ℹ️  Столбец 'language' уже существует.")

        # Проверяем наличие столбца mode
        check_mode = text("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name='users' AND column_name='mode';
        """)

        result = db.execute(check_mode).fetchone()

        if not result:
            print("➕ Добавляем столбец 'mode' в таблицу 'users'...")
            db.execute(text("""
                ALTER TABLE users
                ADD COLUMN mode VARCHAR DEFAULT 'standard';
            """))
            db.commit()
            print("✅ Столбец 'mode' успешно добавлен.")
        else:
            print("ℹ️  Столбец 'mode' уже существует.")

        print("\n🎉 Миграция успешно завершена!")

    except Exception as e:
        print(f"\n❌ Ошибка при выполнении миграции: {e}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    migrate_add_language_mode()
