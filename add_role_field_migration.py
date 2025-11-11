"""
Simple migration script to add role field to users table.

This script directly adds the role field to existing users table
without using Alembic (for cases where Alembic has issues).

Run: python add_role_field_migration.py
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


def add_role_field():
    """Add role field to users table if it doesn't exist."""
    print("=" * 60)
    print("🔧 Adding role field to users table")
    print("=" * 60)

    try:
        # Create engine
        database_url = get_database_url()
        engine = create_engine(database_url)

        print("\n[1/3] Connecting to database...")
        with engine.connect() as conn:
            # Check if users table exists
            inspector = inspect(engine)
            if 'users' not in inspector.get_table_names():
                print("❌ ERROR: users table does not exist!")
                print("   Please run initial schema migration first.")
                return False

            print("✅ Connected to database")

            # Check if role column already exists
            print("\n[2/3] Checking if role column exists...")
            columns = [col['name'] for col in inspector.get_columns('users')]

            if 'role' in columns:
                print("⚠️  Role column already exists. No changes needed.")
                return True

            print("✅ Role column does not exist. Adding...")

            # Add role column with default value
            print("\n[3/3] Adding role column...")
            conn.execute(text("""
                ALTER TABLE users
                ADD COLUMN role VARCHAR DEFAULT 'free' NOT NULL
            """))
            conn.commit()

            # Create index
            print("   Creating index on role column...")
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS ix_users_role ON users(role)
            """))
            conn.commit()

            print("✅ Role column added successfully!")
            print("   Default role: 'free'")
            print("   Index created: ix_users_role")

            # Update existing users if any
            result = conn.execute(text("SELECT COUNT(*) FROM users"))
            user_count = result.scalar()

            if user_count > 0:
                print(f"\n📊 Updated {user_count} existing users with role='free'")

            print("\n" + "=" * 60)
            print("✅ Migration completed successfully!")
            print("=" * 60)
            return True

    except Exception as e:
        print(f"\n❌ ERROR during migration: {e}")
        print("\n💡 Tips:")
        print("   1. Make sure PostgreSQL is running")
        print("   2. Check .env file has correct database credentials")
        print("   3. Verify database exists")
        print("\n" + "=" * 60)
        return False


if __name__ == "__main__":
    success = add_role_field()
    sys.exit(0 if success else 1)
