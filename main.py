# main.py
import os
import logging
import traceback
import google.generativeai as genai
from dotenv import load_dotenv
from functools import partial

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes

from config import GEMINI_MODEL_NAME
from handlers.common import start, clear_command, button_callback, my_docs_command
from handlers.documents import handle_document
from handlers.messages import handle_message
from audio import handle_audio
from database.database import init_db

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Глобальный обработчик ошибок для всех хендлеров бота."""
    logger.error("❌ Произошла ошибка при обработке обновления:", exc_info=context.error)

    # Отправляем сообщение пользователю о том, что произошла ошибка
    try:
        if isinstance(update, Update) and update.effective_message:
            error_message = (
                "⚠️ Произошла ошибка при обработке вашего запроса.\n\n"
                "Пожалуйста, попробуйте еще раз или обратитесь к администратору."
            )

            # Для некоторых критических ошибок показываем детали
            if context.error:
                error_type = type(context.error).__name__
                if "Database" in error_type or "SQL" in error_type:
                    error_message += "\n\n💡 Возможно, требуется миграция базы данных. Запустите: python migrate_db.py"
                elif "Connection" in error_type or "Network" in error_type:
                    error_message += "\n\n💡 Проблема с подключением. Проверьте Redis и PostgreSQL."

            await update.effective_message.reply_text(error_message)
    except Exception as e:
        logger.error(f"❌ Не удалось отправить сообщение об ошибке пользователю: {e}")

def main() -> None:
    load_dotenv()
    init_db()
    
    try:
        gemini_api_key = os.getenv('GEMINI_API_KEY')
        if not gemini_api_key:
            logger.critical("❌ GEMINI_API_KEY не найден!")
            return
        genai.configure(api_key=gemini_api_key)
        gemini_model = genai.GenerativeModel(GEMINI_MODEL_NAME)
        logger.info(f"🤖 Модель AI '{GEMINI_MODEL_NAME}' успешно инициализирована.")
    except Exception as e:
        logger.critical(f"❌ Критическая ошибка при инициализации Gemini: {e}")
        return

    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        logger.critical("❌ TELEGRAM_BOT_TOKEN не найден!")
        return
        
    application = Application.builder().token(token).build()
    
    # Используем partial, чтобы "закрепить" аргумент gemini_model за обработчиком
    message_handler_with_model = partial(handle_message, gemini_model=gemini_model)

    # Регистрируем глобальный обработчик ошибок
    application.add_error_handler(error_handler)

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("mydocs", my_docs_command))
    application.add_handler(CommandHandler("clear", clear_command))

    application.add_handler(CallbackQueryHandler(button_callback))

    # Обработчик для всех типов документов (PDF, Excel, Word)
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))

    # Обработчик для аудио и голосовых сообщений
    application.add_handler(MessageHandler(filters.AUDIO | filters.VOICE, handle_audio))

    # Обработчик текстовых сообщений (вопросы по документам)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler_with_model))


    logger.info("✅ Бот готов к работе и запускается...")
    application.run_polling()

if __name__ == '__main__':
    main()