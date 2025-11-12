#!/usr/bin/env python3
"""
AI Business Assistant - Setup Checker
======================================

This script checks your environment and identifies any issues
before you start the bot.

Run: python setup_checker.py
"""

import os
import sys
import subprocess
import importlib.util
from pathlib import Path
from typing import List, Tuple

# ANSI color codes
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'


def print_header(text: str):
    """Print section header."""
    print(f"\n{BOLD}{BLUE}{'='*70}{RESET}")
    print(f"{BOLD}{BLUE}{text:^70}{RESET}")
    print(f"{BOLD}{BLUE}{'='*70}{RESET}\n")


def print_success(text: str):
    """Print success message."""
    print(f"{GREEN}✓{RESET} {text}")


def print_warning(text: str):
    """Print warning message."""
    print(f"{YELLOW}⚠{RESET} {text}")


def print_error(text: str):
    """Print error message."""
    print(f"{RED}✗{RESET} {text}")


def print_info(text: str):
    """Print info message."""
    print(f"{BLUE}ℹ{RESET} {text}")


def check_python_version() -> bool:
    """Check Python version."""
    print_header("Python Version Check")

    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"

    print(f"Current Python version: {version_str}")

    if version.major == 3 and version.minor >= 10:
        if version.minor == 13:
            print_warning(f"Python 3.13 detected. Some packages may have compatibility issues.")
            print_info("Recommended: Python 3.10, 3.11, or 3.12")
            return True
        else:
            print_success(f"Python {version_str} is supported")
            return True
    else:
        print_error(f"Python {version_str} is not supported")
        print_info("Required: Python 3.10 or higher")
        print_info("Recommended: Python 3.10, 3.11, or 3.12")
        return False


def check_virtual_env() -> bool:
    """Check if running in virtual environment."""
    print_header("Virtual Environment Check")

    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )

    if in_venv:
        print_success("Running in virtual environment")
        print_info(f"Virtual env path: {sys.prefix}")
        return True
    else:
        print_warning("Not running in virtual environment")
        print_info("Recommended: Create and activate virtual environment")
        print_info("  python -m venv .venv")
        print_info("  source .venv/bin/activate  # Linux/Mac")
        print_info("  .venv\\Scripts\\activate  # Windows")
        return False


def check_required_packages() -> Tuple[bool, List[str]]:
    """Check if required packages are installed."""
    print_header("Required Packages Check")

    required_packages = [
        ('telegram', 'python-telegram-bot'),
        ('dotenv', 'python-dotenv'),
        ('google.generativeai', 'google-generativeai'),
        ('sqlalchemy', 'SQLAlchemy'),
        ('psycopg2', 'psycopg2-binary'),
        ('alembic', 'alembic'),
        ('celery', 'celery'),
        ('redis', 'redis'),
        ('fitz', 'PyMuPDF'),
        ('pandas', 'pandas'),
        ('docx', 'python-docx'),
        ('openpyxl', 'openpyxl'),
        ('pydantic', 'pydantic'),
        ('fastapi', 'fastapi'),
    ]

    missing_packages = []
    all_installed = True

    for import_name, package_name in required_packages:
        spec = importlib.util.find_spec(import_name)
        if spec is None:
            print_error(f"{package_name} not installed")
            missing_packages.append(package_name)
            all_installed = False
        else:
            print_success(f"{package_name} installed")

    if missing_packages:
        print()
        print_info("To install missing packages:")
        print_info("  pip install -r requirements.txt")

    return all_installed, missing_packages


def check_env_file() -> bool:
    """Check .env file existence and required variables."""
    print_header(".env Configuration Check")

    env_path = Path('.env')

    if not env_path.exists():
        print_error(".env file not found")
        print_info("Create .env from .env.example:")
        print_info("  cp .env.example .env")
        return False

    print_success(".env file exists")

    # Load .env file
    from dotenv import dotenv_values
    env_vars = dotenv_values('.env')

    required_vars = [
        ('TELEGRAM_BOT_TOKEN', 'Get from @BotFather in Telegram'),
        ('GEMINI_API_KEY', 'Get from https://makersuite.google.com/'),
        ('DB_HOST', 'PostgreSQL host (localhost or container name)'),
        ('DB_PORT', 'PostgreSQL port (default: 5432)'),
        ('DB_USER', 'PostgreSQL username'),
        ('DB_PASS', 'PostgreSQL password'),
        ('DB_NAME', 'PostgreSQL database name'),
        ('REDIS_URL', 'Redis connection URL (default: redis://localhost:6379/0)'),
        ('JWT_SECRET_KEY', 'Secret key for JWT (min 32 chars)'),
    ]

    missing_vars = []

    print()
    for var_name, description in required_vars:
        var_value = env_vars.get(var_name, '').strip()

        # Check if variable exists and is not placeholder
        if not var_value or 'your_' in var_value.lower() or 'change-this' in var_value.lower():
            print_error(f"{var_name} not configured")
            print_info(f"  Description: {description}")
            missing_vars.append(var_name)
        else:
            # Show masked value for security
            if 'TOKEN' in var_name or 'KEY' in var_name or 'PASS' in var_name or 'SECRET' in var_name:
                masked_value = var_value[:8] + '...' + var_value[-4:] if len(var_value) > 12 else '***'
                print_success(f"{var_name} = {masked_value}")
            else:
                print_success(f"{var_name} = {var_value}")

    if missing_vars:
        print()
        print_warning(f"{len(missing_vars)} variables need configuration")
        return False

    return True


def check_docker() -> bool:
    """Check if Docker is running."""
    print_header("Docker Check")

    try:
        result = subprocess.run(
            ['docker', '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode == 0:
            print_success(f"Docker installed: {result.stdout.strip()}")

            # Check if Docker daemon is running
            result = subprocess.run(
                ['docker', 'ps'],
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode == 0:
                print_success("Docker daemon is running")
                return True
            else:
                print_warning("Docker is installed but not running")
                print_info("Start Docker Desktop and try again")
                return False
        else:
            print_warning("Docker not found")
            return False

    except (subprocess.TimeoutExpired, FileNotFoundError):
        print_warning("Docker not installed or not in PATH")
        print_info("Install from: https://www.docker.com/products/docker-desktop/")
        return False


def check_database_connection() -> bool:
    """Check database connection."""
    print_header("Database Connection Check")

    try:
        from dotenv import load_dotenv
        load_dotenv()

        from sqlalchemy import create_engine, text
        from database.database import get_database_url

        db_url = get_database_url()
        engine = create_engine(db_url)

        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]

        print_success("Database connection successful")
        print_info(f"PostgreSQL version: {version.split()[0]} {version.split()[1]}")
        engine.dispose()
        return True

    except ImportError as e:
        print_warning("Cannot check database (missing dependencies)")
        print_info(f"Error: {e}")
        return False
    except Exception as e:
        print_error("Database connection failed")
        print_info(f"Error: {e}")
        print_info("Make sure PostgreSQL is running:")
        print_info("  docker-compose up -d db")
        return False


def check_redis_connection() -> bool:
    """Check Redis connection."""
    print_header("Redis Connection Check")

    try:
        from dotenv import load_dotenv
        import redis

        load_dotenv()
        redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

        r = redis.from_url(redis_url)
        r.ping()

        print_success("Redis connection successful")
        print_info(f"Redis URL: {redis_url}")
        return True

    except ImportError:
        print_warning("Cannot check Redis (missing dependencies)")
        return False
    except Exception as e:
        print_error("Redis connection failed")
        print_info(f"Error: {e}")
        print_info("Make sure Redis is running:")
        print_info("  docker-compose up -d redis")
        return False


def check_migrations() -> bool:
    """Check if database migrations are up to date."""
    print_header("Database Migrations Check")

    try:
        result = subprocess.run(
            ['alembic', 'current'],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            output = result.stdout.strip()
            if output and '(head)' in output:
                print_success("Database migrations are up to date")
                return True
            else:
                print_warning("Database migrations may be outdated")
                print_info("Run: alembic upgrade head")
                return False
        else:
            print_warning("Could not check migrations")
            print_info(f"Error: {result.stderr}")
            return False

    except (subprocess.TimeoutExpired, FileNotFoundError):
        print_warning("Alembic not found or migration check failed")
        print_info("Make sure alembic is installed: pip install alembic")
        return False


def main():
    """Run all checks."""
    print(f"{BOLD}AI Business Assistant - Setup Checker{RESET}")
    print("Checking your environment...\n")

    results = {}

    # Run all checks
    results['python'] = check_python_version()
    results['venv'] = check_virtual_env()
    results['packages'], missing = check_required_packages()
    results['env'] = check_env_file()
    results['docker'] = check_docker()
    results['database'] = check_database_connection()
    results['redis'] = check_redis_connection()
    results['migrations'] = check_migrations()

    # Summary
    print_header("Summary")

    total_checks = len(results)
    passed_checks = sum(1 for v in results.values() if v)

    print(f"Checks passed: {passed_checks}/{total_checks}")
    print()

    if all(results.values()):
        print_success("All checks passed! You're ready to start the bot.")
        print()
        print_info("To start the bot:")
        print_info("  1. docker-compose up -d  # Start infrastructure")
        print_info("  2. celery -A celery_app worker --loglevel=info  # Start worker")
        print_info("  3. python main.py  # Start bot")
        return 0
    else:
        print_warning("Some checks failed. Please fix the issues above.")
        print()

        if not results['packages']:
            print_info("Install dependencies: pip install -r requirements.txt")

        if not results['env']:
            print_info("Configure .env file with your API keys")

        if not results['database'] or not results['redis']:
            print_info("Start infrastructure: docker-compose up -d")

        if not results['migrations']:
            print_info("Apply migrations: alembic upgrade head")

        return 1


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nSetup check cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n{RED}Unexpected error: {e}{RESET}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
