#!/usr/bin/env python3
"""
Скрипт миграции базы данных для добавления полей language, mode и active_document_id в таблицу users.
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

        # Проверяем наличие столбца active_document_id
        check_active_doc = text("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name='users' AND column_name='active_document_id';
        """)

        result = db.execute(check_active_doc).fetchone()

        if not result:
            print("➕ Добавляем столбец 'active_document_id' в таблицу 'users'...")
            db.execute(text("""
                ALTER TABLE users
                ADD COLUMN active_document_id INTEGER;
            """))
            db.commit()

            # Добавляем внешний ключ
            print("➕ Добавляем внешний ключ для 'active_document_id'...")
            db.execute(text("""
                ALTER TABLE users
                ADD CONSTRAINT fk_active_document
                FOREIGN KEY (active_document_id) REFERENCES documents(id) ON DELETE SET NULL;
            """))
            db.commit()
            print("✅ Столбец 'active_document_id' успешно добавлен.")
        else:
            print("ℹ️  Столбец 'active_document_id' уже существует.")

        # Проверяем наличие столбца email
        check_email = text("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name='users' AND column_name='email';
        """)

        result = db.execute(check_email).fetchone()

        if not result:
            print("➕ Добавляем столбец 'email' в таблицу 'users'...")
            db.execute(text("""
                ALTER TABLE users
                ADD COLUMN email VARCHAR;
            """))
            db.commit()

            # Добавляем unique constraint на email
            print("➕ Добавляем unique constraint на 'email'...")
            try:
                db.execute(text("""
                    ALTER TABLE users
                    ADD CONSTRAINT users_email_unique UNIQUE (email);
                """))
                db.commit()
            except Exception as e:
                print(f"⚠️  Constraint уже существует или ошибка: {e}")
                db.rollback()

            print("✅ Столбец 'email' успешно добавлен.")
        else:
            print("ℹ️  Столбец 'email' уже существует.")

        # Проверяем наличие столбца password_hash
        check_password = text("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name='users' AND column_name='password_hash';
        """)

        result = db.execute(check_password).fetchone()

        if not result:
            print("➕ Добавляем столбец 'password_hash' в таблицу 'users'...")
            db.execute(text("""
                ALTER TABLE users
                ADD COLUMN password_hash VARCHAR;
            """))
            db.commit()
            print("✅ Столбец 'password_hash' успешно добавлен.")
        else:
            print("ℹ️  Столбец 'password_hash' уже существует.")

        print("\n🎉 Миграция успешно завершена!")

    except Exception as e:
        print(f"\n❌ Ошибка при выполнении миграции: {e}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    migrate_add_language_mode()
