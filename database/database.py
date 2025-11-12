# database/database.py

import os
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

from .models import Base

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")

# Use SQLite for testing if DB config is not set
if not all([DB_HOST, DB_PORT, DB_USER, DB_PASS, DB_NAME]) or os.getenv("TESTING") == "true":
    # In-memory SQLite for tests
    DATABASE_URL = "sqlite:///:memory:"
    engine = create_engine(
        DATABASE_URL,
        echo=False,
        connect_args={"check_same_thread": False}  # Needed for SQLite
    )
else:
    # URL-encode credentials to handle special characters and Cyrillic
    db_user_encoded = quote_plus(DB_USER)
    db_pass_encoded = quote_plus(DB_PASS)
    DATABASE_URL = f"postgresql://{db_user_encoded}:{db_pass_encoded}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    # Enhanced connection pooling for production
    # See: https://docs.sqlalchemy.org/en/20/core/pooling.html

    # Determine environment
    is_production = os.getenv("ENVIRONMENT", "development").lower() == "production"

    # Production settings: higher pool size for better concurrency
    # Development settings: smaller pool to reduce resource usage
    pool_size = 20 if is_production else 5
    max_overflow = 40 if is_production else 10
    pool_timeout = 30 if is_production else 10

    engine = create_engine(
        DATABASE_URL,
        echo=False,  # Disable SQL query logging for performance

        # Connection Pool Settings
        pool_size=pool_size,              # Number of persistent connections
        max_overflow=max_overflow,        # Max additional connections when pool is full
        pool_timeout=pool_timeout,        # Seconds to wait for available connection
        pool_recycle=3600,                # Recycle connections after 1 hour (prevents stale connections)
        pool_pre_ping=True,               # Verify connection health before using

        # Connection Settings
        connect_args={
            "connect_timeout": 10,                        # Connection timeout: 10 seconds
            "options": "-c statement_timeout=30000",      # Query timeout: 30 seconds
            "keepalives": 1,                              # Enable TCP keepalive
            "keepalives_idle": 30,                        # Seconds before sending keepalive probes
            "keepalives_interval": 10,                    # Interval between keepalive probes
            "keepalives_count": 5,                        # Max keepalive probes before closing
        }
    )

# "Фабрика" для создания сессий подключения к БД
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Context manager для database sessions.

    Usage:
        with get_db() as db:
            user = crud.get_user(db, user_id)

    Ensures sessions are properly closed even on exceptions.
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()  # Auto-commit on success
    except Exception:
        db.rollback()  # Auto-rollback on error
        raise
    finally:
        db.close()  # Always close


def init_db():
    """
    Инициализирует базу данных, создавая все необходимые таблицы.
    Вызывается один раз при старте бота.
    """
    print("Инициализация базы данных...")
    # Создает таблицы на основе моделей, унаследованных от Base
    Base.metadata.create_all(bind=engine)
    print("База данных успешно инициализирована.")