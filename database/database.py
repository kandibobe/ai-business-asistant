# database/database.py

import os
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

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

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

def init_db():
    """
    Инициализирует базу данных, создавая все необходимые таблицы.
    Вызывается один раз при старте бота.
    """
    print("Инициализация базы данных...")
    # Создает таблицы на основе моделей, унаследованных от Base
    Base.metadata.create_all(bind=engine)
    print("База данных успешно инициализирована.")