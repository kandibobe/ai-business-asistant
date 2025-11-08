import os
import fitz  # PyMuPDF
from pydub import AudioSegment
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from sqlalchemy.orm import Session
from dotenv import load_dotenv

load_dotenv()

from celery_app import app
from database.database import SessionLocal
from database import crud

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN не найден в .env файле!")
bot = Bot(token=TELEGRAM_BOT_TOKEN)

def get_post_analysis_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура, отправляемая после успешного анализа."""
    keyboard = [
        [InlineKeyboardButton("❓ Задать вопрос по этому документу", switch_inline_query_current_chat="")],
        [InlineKeyboardButton("📚 Показать все мои документы", callback_data='my_docs')],
    ]
    return InlineKeyboardMarkup(keyboard)

@app.task
def process_pdf_task(chat_id: int, user_id: int, username: str, first_name: str, last_name: str, file_path: str, file_name: str):
    """Celery-задача для асинхронной обработки PDF."""
    print(f"WORKER: Начал обработку PDF {file_name}")
    text = ""
    try:
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text()
    except Exception as e:
        bot.send_message(chat_id, f"❌ Не удалось обработать PDF '{file_name}'. Ошибка: {e}")
        return

    db: Session = SessionLocal()
    try:
        db_user = crud.get_or_create_user(db, user_id, username, first_name, last_name)
        new_doc = crud.create_user_document(db, db_user, file_name, file_path, text)
        # АВТОМАТИЧЕСКИ делаем новый документ активным
        crud.set_active_document(db, db_user, new_doc.id)
        
        bot.send_message(
            chat_id,
            f"✅ PDF '{file_name}' успешно проанализирован и сохранен.\n"
            f"📄 **Он назначен активным для диалога.**\n\n"
            f"Извлечено {len(text)} символов. Что делаем дальше?",
            parse_mode='HTML',
            reply_markup=get_post_analysis_keyboard()
        )
    finally:
        db.close()
    print(f"WORKER: Закончил обработку PDF {file_name}")

@app.task
def transcribe_audio_task(chat_id: int, user_id: int, username: str, first_name: str, last_name: str, file_path: str, file_name: str):
    """Celery-задача для транскрибации аудио."""
    print(f"WORKER: Начал транскрибацию {file_name}")
    try:
        # Конвертируем аудио в нужный формат (WAV) и извлекаем текст
        # Это заглушка, сюда нужно будет вставить реальную модель транскрибации (например, Whisper)
        # Пока что мы просто имитируем долгий процесс и создаем текстовый файл
        
        # Имитация долгой работы
        import time
        time.sleep(10) 
        
        sound = AudioSegment.from_file(file_path)
        # В будущем здесь будет вызов AI-модели для транскрибации
        # text = speech_to_text_model(sound)
        text = f"Это транскрибированный текст из файла {file_name}. Длительность: {len(sound) / 1000:.2f} секунд."

    except Exception as e:
        bot.send_message(chat_id, f"❌ Не удалось обработать аудио '{file_name}'. Ошибка: {e}")
        return

    db: Session = SessionLocal()
    try:
        db_user = crud.get_or_create_user(db, user_id, username, first_name, last_name)
        new_doc = crud.create_user_document(db, db_user, file_name, file_path, text)
        # АВТОМАТИЧЕСКИ делаем новый документ активным
        crud.set_active_document(db, db_user, new_doc.id)
        
        bot.send_message(
            chat_id,
            f"✅ Аудио '{file_name}' успешно транскрибировано и сохранено.\n"
            f"📄 **Запись назначена активной для диалога.**\n\n"
            f"Распознано {len(text)} символов. Что делаем дальше?",
            parse_mode='HTML',
            reply_markup=get_post_analysis_keyboard()
        )
    finally:
        db.close()
    print(f"WORKER: Закончил транскрибацию {file_name}")