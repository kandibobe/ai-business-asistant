#!/usr/bin/env python3
"""
Комплексная миграция таблицы documents для добавления всех недостающих полей.
"""
import os
import sys
from sqlalchemy import text
from dotenv import load_dotenv

# Добавляем корневую директорию проекта в PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

from database.database import engine, SessionLocal

def migrate_documents_table():
    """Добавляет все недостающие поля в таблицу documents."""
    print("🔄 Начинаем миграцию таблицы documents...")

    db = SessionLocal()

    try:
        # Список всех полей, которые нужно добавить
        fields_to_add = [
            ('document_type', 'VARCHAR', None),
            ('source_url', 'VARCHAR', None),
            ('file_size', 'INTEGER', None),
            ('word_count', 'INTEGER', None),
            ('char_count', 'INTEGER', None),
            ('language_detected', 'VARCHAR', None),
            ('summary', 'TEXT', None),
            ('keywords', 'TEXT', None),
            ('processed_at', 'TIMESTAMP WITH TIME ZONE', None),
        ]

        for field_name, field_type, default_value in fields_to_add:
            # Проверяем наличие столбца
            check_query = text(f"""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name='documents' AND column_name='{field_name}';
            """)

            result = db.execute(check_query).fetchone()

            if not result:
                print(f"➕ Добавляем столбец '{field_name}' ({field_type})...")

                # Формируем SQL для добавления столбца
                default_clause = f" DEFAULT {default_value}" if default_value else ""
                alter_query = text(f"""
                    ALTER TABLE documents
                    ADD COLUMN {field_name} {field_type}{default_clause};
                """)

                db.execute(alter_query)
                db.commit()
                print(f"✅ Столбец '{field_name}' успешно добавлен.")
            else:
                print(f"ℹ️  Столбец '{field_name}' уже существует.")

        # Проверяем, нужно ли обновить существующие записи
        print("\n➕ Обновление существующих документов...")

        # Определяем document_type на основе filename
        update_type_query = text("""
            UPDATE documents
            SET document_type = CASE
                WHEN LOWER(filename) LIKE '%.pdf' THEN 'pdf'
                WHEN LOWER(filename) LIKE '%.xlsx' OR LOWER(filename) LIKE '%.xls' THEN 'excel'
                WHEN LOWER(filename) LIKE '%.docx' OR LOWER(filename) LIKE '%.doc' THEN 'word'
                WHEN LOWER(filename) LIKE '%.mp3' OR LOWER(filename) LIKE '%.wav' OR LOWER(filename) LIKE '%.m4a' THEN 'audio'
                WHEN file_path LIKE 'http%' THEN 'url'
                ELSE 'unknown'
            END
            WHERE document_type IS NULL;
        """)

        result = db.execute(update_type_query)
        db.commit()
        print(f"✅ Обновлено {result.rowcount} документов с определением типа.")

        # Подсчитываем количество слов и символов для существующих документов
        update_counts_query = text("""
            UPDATE documents
            SET
                char_count = LENGTH(extracted_text),
                word_count = (LENGTH(extracted_text) - LENGTH(REPLACE(extracted_text, ' ', '')) + 1)
            WHERE extracted_text IS NOT NULL
            AND (char_count IS NULL OR word_count IS NULL);
        """)

        result = db.execute(update_counts_query)
        db.commit()
        print(f"✅ Обновлено {result.rowcount} документов с подсчетом слов и символов.")

        print("\n🎉 Миграция таблицы documents успешно завершена!")

    except Exception as e:
        print(f"\n❌ Ошибка при выполнении миграции: {e}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    migrate_documents_table()
