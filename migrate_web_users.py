"""
Database migration: Add email and password_hash fields for web users.
"""
from sqlalchemy import text
from database.database import engine
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def migrate():
    """Add email and password_hash columns to users table."""
    with engine.connect() as connection:
        try:
            # Check if columns already exist
            result = connection.execute(text("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name='users' AND column_name IN ('email', 'password_hash');
            """))

            existing_columns = [row[0] for row in result]

            # Add email column if it doesn't exist
            if 'email' not in existing_columns:
                logger.info("Adding 'email' column to users table...")
                connection.execute(text("""
                    ALTER TABLE users
                    ADD COLUMN email VARCHAR,
                    ADD CONSTRAINT users_email_unique UNIQUE (email);
                """))
                connection.execute(text("CREATE INDEX ix_users_email ON users (email);"))
                logger.info("✅ 'email' column added successfully")
            else:
                logger.info("'email' column already exists")

            # Add password_hash column if it doesn't exist
            if 'password_hash' not in existing_columns:
                logger.info("Adding 'password_hash' column to users table...")
                connection.execute(text("""
                    ALTER TABLE users
                    ADD COLUMN password_hash VARCHAR;
                """))
                logger.info("✅ 'password_hash' column added successfully")
            else:
                logger.info("'password_hash' column already exists")

            # Make sure username is indexed
            try:
                connection.execute(text("CREATE INDEX IF NOT EXISTS ix_users_username ON users (username);"))
                logger.info("✅ Username index verified")
            except:
                logger.info("Username index already exists or not needed")

            connection.commit()
            logger.info("✅ Migration completed successfully!")

        except Exception as e:
            logger.error(f"❌ Migration failed: {e}")
            connection.rollback()
            raise


if __name__ == "__main__":
    logger.info("Starting database migration for web users...")
    migrate()
    logger.info("Migration completed!")
