# handlers/tasks.py
import os
import fitz # PyMuPDF
from telegram import Bot
from sqlalchemy.orm import Session
from dotenv import load_dotenv

# Загружаем переменные окружения, так как воркер - отдельный процесс
load_dotenv()

from celery_app import app # Импортируем наш экземпляр Celery
from database.database import SessionLocal
from database import crud

# Загружаем токен бота один раз при старте воркера
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Проверяем, что токен загрузился
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN не найден в .env файле!")
    
bot = Bot(token=TELEGRAM_BOT_TOKEN)

@app.task
def process_pdf_task(chat_id: int, user_id: int, username: str, first_name: str, last_name: str, file_path: str, file_name: str):
    """
    Celery-задача для асинхронной обработки PDF.
    Эта функция выполняется в отдельном процессе (воркером).
    """
    print(f"Celery Worker: Начал обработку файла {file_name} для chat_id {chat_id}")
    
    text = ""
    try:
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text()
    except Exception as e:
        # Если произошла ошибка, сообщаем пользователю
        bot.send_message(chat_id, f"❌ Не удалось обработать файл '{file_name}'. Ошибка: {e}")
        return

    # Работа с базой данных внутри воркера
    db: Session = SessionLocal()
    try:
        db_user = crud.get_or_create_user(db, user_id, username, first_name, last_name)
        crud.create_user_document(db, db_user, file_name, file_path, text)
        
        # Отправляем уведомление об успехе
        bot.send_message(
            chat_id,
            f"✅ Файл '{file_name}' успешно проанализирован и сохранен. "
            f"Извлечено {len(text)} символов. Теперь вы можете задавать по нему вопросы."
        )
    finally:
        db.close()
    
    print(f"Celery Worker: Закончил обработку файла {file_name}")