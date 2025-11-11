#!/usr/bin/env python3
"""
Миграция для добавления полей пользовательских предпочтений.
Добавляет поля: ai_role, response_style, notifications_enabled, auto_analysis_enabled
"""
import os
import sys
from sqlalchemy import text
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

from database.database import engine, SessionLocal

def migrate_user_preferences():
    """Добавляет поля пользовательских предпочтений в таблицу users."""
    print("🔄 Миграция пользовательских предпочтений...")

    db = SessionLocal()

    try:
        # Список полей для добавления
        fields_to_add = [
            ('ai_role', 'VARCHAR', "'assistant'"),
            ('response_style', 'VARCHAR', "'standard'"),
            ('notifications_enabled', 'VARCHAR', "'true'"),
            ('auto_analysis_enabled', 'VARCHAR', "'false'"),
        ]

        for field_name, field_type, default_value in fields_to_add:
            # Проверяем наличие столбца
            check_query = text(f"""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name='users' AND column_name='{field_name}';
            """)

            result = db.execute(check_query).fetchone()

            if not result:
                print(f"➕ Добавляем столбец '{field_name}'...")

                alter_query = text(f"""
                    ALTER TABLE users
                    ADD COLUMN {field_name} {field_type} DEFAULT {default_value};
                """)

                db.execute(alter_query)
                db.commit()
                print(f"✅ Столбец '{field_name}' успешно добавлен.")
            else:
                print(f"ℹ️  Столбец '{field_name}' уже существует.")

        print("\n🎉 Миграция пользовательских предпочтений завершена!")

    except Exception as e:
        print(f"\n❌ Ошибка при миграции: {e}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    migrate_user_preferences()
