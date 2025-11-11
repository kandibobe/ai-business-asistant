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

    # echo=False, чтобы не выводить все SQL-запросы в консоль
    # Added connection timeout and pool settings for better reliability
    engine = create_engine(
        DATABASE_URL,
        echo=False,
        pool_pre_ping=True,  # Verify connections before using
        pool_size=5,         # Connection pool size
        max_overflow=10,     # Max overflow connections
        connect_args={
            "connect_timeout": 10,  # 10 second connection timeout
            "options": "-c statement_timeout=30000"  # 30 second query timeout
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