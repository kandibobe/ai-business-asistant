"""
Migration to add language field to users table.
Runs automatically on bot startup.
"""
import os
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError, ProgrammingError
from dotenv import load_dotenv

load_dotenv()

def migrate_language_field():
    """Adds language field to users table if it doesn't exist"""

    # Build DATABASE_URL from parameters (like in database/database.py)
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASS")
    DB_NAME = os.getenv("DB_NAME")

    if not all([DB_HOST, DB_PORT, DB_USER, DB_PASS, DB_NAME]):
        print("⚠️  Not all DB parameters found - skipping language migration")
        return True  # Not critical, return True to allow bot to continue

    database_url = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    # Add timeout settings for reliability
    engine = create_engine(
        database_url,
        connect_args={
            "connect_timeout": 10,  # 10 second timeout
            "options": "-c statement_timeout=30000"  # 30 second query timeout
        }
    )

    try:
        with engine.connect() as connection:
            # Check if language column already exists
            check_query = text("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name='users' AND column_name='language';
            """)

            result = connection.execute(check_query)
            exists = result.fetchone() is not None

            if exists:
                print("✅ Field 'language' already exists in users table")
                return True

            # Add language column
            print("📝 Adding 'language' field to users table...")

            alter_query = text("""
                ALTER TABLE users
                ADD COLUMN language VARCHAR DEFAULT 'ru';
            """)

            connection.execute(alter_query)
            connection.commit()

            print("✅ Field 'language' successfully added")
            print("🔄 Setting language 'ru' for existing users...")

            # Set Russian language for all existing users
            update_query = text("""
                UPDATE users
                SET language = 'ru'
                WHERE language IS NULL;
            """)

            connection.execute(update_query)
            connection.commit()

            print("✅ Language migration completed!")
            return True

    except (OperationalError, ProgrammingError) as e:
        print(f"⚠️  Migration error: {e}")
        return True  # Not critical, continue
    except Exception as e:
        print(f"⚠️  Unexpected error: {e}")
        return True  # Not critical, continue
    finally:
        engine.dispose()

if __name__ == '__main__':
    migrate_language_field()
