"""
Миграция для добавления поля language в таблицу users.
Запускается автоматически при старте бота.
"""
import os
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError, ProgrammingError
from dotenv import load_dotenv

load_dotenv()

def migrate_language_field():
    """Добавляет поле language в таблицу users если оно отсутствует"""

    # Собираем DATABASE_URL из параметров (как в database/database.py)
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASS")
    DB_NAME = os.getenv("DB_NAME")

    if not all([DB_HOST, DB_PORT, DB_USER, DB_PASS, DB_NAME]):
        print("⚠️  Не все параметры БД найдены - пропускаем миграцию языков")
        return True  # Не критично, вернем True чтобы бот продолжил работу

    database_url = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(database_url)

    try:
        with engine.connect() as connection:
            # Проверяем, существует ли уже колонка language
            check_query = text("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name='users' AND column_name='language';
            """)

            result = connection.execute(check_query)
            exists = result.fetchone() is not None

            if exists:
                print("✅ Поле 'language' уже существует в таблице users")
                return True

            # Добавляем колонку language
            print("📝 Добавляем поле 'language' в таблицу users...")

            alter_query = text("""
                ALTER TABLE users
                ADD COLUMN language VARCHAR DEFAULT 'ru';
            """)

            connection.execute(alter_query)
            connection.commit()

            print("✅ Поле 'language' успешно добавлено")
            print("🔄 Устанавливаем язык 'ru' для существующих пользователей...")

            # Устанавливаем русский язык для всех существующих пользователей
            update_query = text("""
                UPDATE users
                SET language = 'ru'
                WHERE language IS NULL;
            """)

            connection.execute(update_query)
            connection.commit()

            print("✅ Миграция language завершена!")
            return True

    except (OperationalError, ProgrammingError) as e:
        print(f"⚠️  Ошибка миграции: {e}")
        return True  # Не критично, продолжаем
    except Exception as e:
        print(f"⚠️  Неожиданная ошибка: {e}")
        return True  # Не критично, продолжаем
    finally:
        engine.dispose()

if __name__ == '__main__':
    migrate_language_field()
