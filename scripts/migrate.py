#!/usr/bin/env python3
"""
Database migration management script.
Wrapper around Alembic for common migration tasks.
"""
import sys
import subprocess
from pathlib import Path


def run_command(cmd: list[str]) -> int:
    """Run a command and return exit code."""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    return result.returncode


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("""
Database Migration Manager

Usage:
    python migrate.py <command> [args]

Commands:
    upgrade         - Upgrade to latest version (alembic upgrade head)
    downgrade       - Downgrade one version (alembic downgrade -1)
    current         - Show current database version
    history         - Show migration history
    create <msg>    - Create new migration with description
    autogen <msg>   - Auto-generate migration from model changes
    stamp <rev>     - Stamp database with specific revision

Examples:
    python migrate.py upgrade
    python migrate.py create "Add user preferences"
    python migrate.py autogen "Add avatar field to users"
    python migrate.py history
    python migrate.py current
        """)
        return 1

    command = sys.argv[1]

    # Check if alembic.ini exists
    if not Path("alembic.ini").exists():
        print("Error: alembic.ini not found. Are you in the project root?")
        return 1

    if command == "upgrade":
        return run_command(["alembic", "upgrade", "head"])

    elif command == "downgrade":
        confirm = input("⚠️  This will downgrade the database. Continue? (yes/no): ")
        if confirm.lower() != "yes":
            print("Aborted.")
            return 0
        return run_command(["alembic", "downgrade", "-1"])

    elif command == "current":
        return run_command(["alembic", "current"])

    elif command == "history":
        return run_command(["alembic", "history", "--verbose"])

    elif command == "create":
        if len(sys.argv) < 3:
            print("Error: Please provide a migration message")
            print("Example: python migrate.py create 'Add new field'")
            return 1
        message = sys.argv[2]
        return run_command(["alembic", "revision", "-m", message])

    elif command == "autogen":
        if len(sys.argv) < 3:
            print("Error: Please provide a migration message")
            print("Example: python migrate.py autogen 'Add avatar field'")
            return 1
        message = sys.argv[2]
        return run_command(["alembic", "revision", "--autogenerate", "-m", message])

    elif command == "stamp":
        if len(sys.argv) < 3:
            print("Error: Please provide a revision id")
            print("Example: python migrate.py stamp head")
            return 1
        revision = sys.argv[2]
        return run_command(["alembic", "stamp", revision])

    else:
        print(f"Unknown command: {command}")
        print("Run 'python migrate.py' for help")
        return 1


if __name__ == "__main__":
    sys.exit(main())
