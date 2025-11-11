"""
Standalone migration script to add email and password_hash fields for web users.

This script adds missing fields to users table for FastAPI web authentication.
Telegram users don't need these fields (they will remain NULL).

Run: python add_web_user_fields.py
"""
import os
import sys
from sqlalchemy import create_engine, text, inspect
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def get_database_url():
    """Construct database URL from environment variables."""
    db_user = os.getenv('DB_USER', 'ai_bot_user')
    db_pass = os.getenv('DB_PASS', 'password')
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '5432')
    db_name = os.getenv('DB_NAME', 'ai_bot_db')

    return f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"


def add_web_user_fields():
    """Add email and password_hash fields to users table if they don't exist."""
    print("=" * 60)
    print("🔧 Adding web user fields (email, password_hash)")
    print("=" * 60)

    try:
        # Create engine
        database_url = get_database_url()
        engine = create_engine(database_url)

        print("\n[1/5] Connecting to database...")
        with engine.connect() as conn:
            # Check if users table exists
            inspector = inspect(engine)
            if 'users' not in inspector.get_table_names():
                print("❌ ERROR: users table does not exist!")
                print("   Please run initial schema migration first.")
                return False

            print("✅ Connected to database")

            # Get existing columns
            print("\n[2/5] Checking existing columns...")
            columns = {col['name']: col for col in inspector.get_columns('users')}

            fields_to_add = []
            if 'email' not in columns:
                fields_to_add.append('email')
            if 'password_hash' not in columns:
                fields_to_add.append('password_hash')

            if not fields_to_add:
                print("⚠️  Both email and password_hash columns already exist.")
                print("   No changes needed.")
                return True

            print(f"✅ Need to add: {', '.join(fields_to_add)}")

            # Add email column
            if 'email' in fields_to_add:
                print("\n[3/5] Adding email column...")
                conn.execute(text("""
                    ALTER TABLE users
                    ADD COLUMN email VARCHAR NULL
                """))
                conn.commit()
                print("✅ Email column added")

            # Add password_hash column
            if 'password_hash' in fields_to_add:
                print("\n[4/5] Adding password_hash column...")
                conn.execute(text("""
                    ALTER TABLE users
                    ADD COLUMN password_hash VARCHAR NULL
                """))
                conn.commit()
                print("✅ Password_hash column added")

            # Create unique index on email (excluding NULLs)
            print("\n[5/5] Creating unique index on email...")
            try:
                conn.execute(text("""
                    CREATE UNIQUE INDEX ix_users_email
                    ON users(email)
                    WHERE email IS NOT NULL
                """))
                conn.commit()
                print("✅ Unique index created on email")
            except Exception as e:
                if 'already exists' in str(e):
                    print("⚠️  Index already exists, skipping")
                else:
                    raise

            # Show user count
            result = conn.execute(text("SELECT COUNT(*) FROM users"))
            user_count = result.scalar()

            print("\n" + "=" * 60)
            print("✅ Migration completed successfully!")
            print("=" * 60)
            print(f"\n📊 Current users: {user_count}")
            print("   Telegram users: email and password_hash are NULL")
            print("   Web users: Can now register with email/password")
            print("\n" + "=" * 60)
            return True

    except Exception as e:
        print(f"\n❌ ERROR during migration: {e}")
        print("\n💡 Tips:")
        print("   1. Make sure PostgreSQL is running")
        print("   2. Check .env file has correct database credentials")
        print("   3. Verify database exists")
        import traceback
        traceback.print_exc()
        print("\n" + "=" * 60)
        return False


if __name__ == "__main__":
    success = add_web_user_fields()
    sys.exit(0 if success else 1)
