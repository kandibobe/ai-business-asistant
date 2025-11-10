#!/usr/bin/env python3
"""
Automatic database migration and upgrade script.
Ensures database schema is up to date with current models.
"""
import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

def main():
    """Apply database migrations."""
    print("=" * 60)
    print("🔄 Applying Database Migrations...")
    print("=" * 60)

    try:
        from alembic.config import Config
        from alembic import command

        # Get alembic config
        alembic_cfg = Config("alembic.ini")

        # Check current version
        print("\n📊 Checking current database version...")
        try:
            command.current(alembic_cfg)
        except Exception as e:
            print(f"⚠️  Database not versioned yet: {e}")
            print("📌 Stamping database with initial version...")
            command.stamp(alembic_cfg, "head")

        # Apply all migrations
        print("\n⬆️  Upgrading to latest version...")
        command.upgrade(alembic_cfg, "head")

        print("\n✅ Database migrations applied successfully!")
        print("=" * 60)

        # Show current version
        print("\n📊 Current database version:")
        command.current(alembic_cfg, verbose=True)

        return 0

    except ImportError:
        print("❌ Alembic not installed!")
        print("Install it with: pip install alembic")
        return 1

    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure PostgreSQL is running")
        print("2. Check your .env file has correct DB credentials")
        print("3. Verify database exists: psql -U ai_bot_user -d ai_bot_db")
        return 1


if __name__ == "__main__":
    sys.exit(main())
