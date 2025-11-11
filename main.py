# main.py
import os
import logging
import traceback
import signal
import sys
import asyncio
import time
import google.generativeai as genai
from dotenv import load_dotenv
from functools import partial

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes

from config import GEMINI_MODEL_NAME
from handlers.common_enhanced import start, clear_command, button_callback, my_docs_command, stats_command
from handlers.documents import handle_document
from handlers.messages import handle_message
from handlers.reply_keyboard_handler import handle_reply_keyboard
from audio import handle_audio
from database.database import init_db, engine

# Import monitoring and health check utilities
from utils.metrics import metrics, track_startup_time
from utils.health_check import health_checker

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Global application instance for graceful shutdown
app_instance = None
startup_start_time = None

def graceful_shutdown(signum, frame):
    """Handle graceful shutdown on SIGINT/SIGTERM."""
    print("\n")
    logger.info("=" * 60)
    logger.info("🛑 Shutdown signal received. Cleaning up...")
    logger.info("=" * 60)

    try:
        # Close database connections
        if engine:
            logger.info("   Closing database connections...")
            engine.dispose()
            logger.info("   ✅ Database connections closed")

        # Close Redis connections
        try:
            from utils.cache import redis_client
            if redis_client:
                logger.info("   Closing Redis connections...")
                redis_client.close()
                logger.info("   ✅ Redis connections closed")
        except Exception as e:
            logger.warning(f"   ⚠️ Error closing Redis: {e}")

        logger.info("=" * 60)
        logger.info("✅ Cleanup complete. Goodbye!")
        logger.info("=" * 60)

    except Exception as e:
        logger.error(f"❌ Error during cleanup: {e}")
    finally:
        sys.exit(0)


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Global error handler for all bot handlers."""
    # Log detailed error information
    error_type = type(context.error).__name__ if context.error else "Unknown"
    error_msg = str(context.error) if context.error else "No error details"

    logger.error(
        f"❌ Error: {error_type}\n"
        f"Message: {error_msg}\n"
        f"Update: {update}",
        exc_info=context.error
    )

    # Send error message to user
    try:
        if isinstance(update, Update):
            # Determine user language
            user_id = update.effective_user.id if update.effective_user else None
            lang = 'ru'  # Default

            if user_id:
                try:
                    from database.database import SessionLocal
                    from database import crud
                    db = SessionLocal()
                    db_user = crud.get_or_create_user(db, user_id, None, None, None)
                    lang = db_user.language or 'ru'
                    db.close()
                except:
                    pass

            # Build error message
            if lang == 'ru':
                error_message = "⚠️ Произошла ошибка при обработке запроса.\n\nПопробуйте еще раз или обратитесь к администратору."
            else:
                error_message = "⚠️ An error occurred while processing your request.\n\nPlease try again or contact administrator."

            # Add helpful hints for specific errors
            if context.error:
                if "Database" in error_type or "SQL" in error_type:
                    if lang == 'ru':
                        error_message += "\n\n💡 Возможно требуется миграция БД: python upgrade_db.py"
                    else:
                        error_message += "\n\n💡 Database migration may be required: python upgrade_db.py"
                elif "Connection" in error_type or "Network" in error_type:
                    if lang == 'ru':
                        error_message += "\n\n💡 Проблема с подключением. Проверьте Redis и PostgreSQL."
                    else:
                        error_message += "\n\n💡 Connection problem. Check Redis and PostgreSQL."
                elif "Timeout" in error_type:
                    if lang == 'ru':
                        error_message += "\n\n💡 Превышено время ожидания. Попробуйте еще раз."
                    else:
                        error_message += "\n\n💡 Request timeout. Please try again."

            # Try to send error message
            if update.effective_message:
                await update.effective_message.reply_text(error_message)
            elif update.callback_query:
                await update.callback_query.answer(error_message, show_alert=True)

    except Exception as e:
        logger.error(f"❌ Failed to send error message to user: {e}", exc_info=e)

def main() -> None:
    global app_instance, startup_start_time

    # Track startup time
    startup_start_time = time.time()

    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, graceful_shutdown)
    signal.signal(signal.SIGTERM, graceful_shutdown)

    print("=" * 60)
    print("🤖 AI Business Assistant Starting...")
    print("=" * 60)

    print("\n[1/6] Loading environment variables...")
    load_dotenv()
    print("✅ Environment loaded")

    print("\n[2/6] Initializing database...")
    init_db()
    print("✅ Database ready")

    # Note: Database migrations should be run separately using Alembic
    # Run: alembic upgrade head
    print("\n[3/6] Checking database schema...")
    print("💡 Tip: Run 'alembic upgrade head' to apply latest migrations")
    print("✅ Database schema check completed")

    print("\n[4/6] Initializing AI model...")
    try:
        gemini_api_key = os.getenv('GEMINI_API_KEY')
        if not gemini_api_key:
            logger.critical("❌ GEMINI_API_KEY not found!")
            print("❌ ERROR: GEMINI_API_KEY not found in .env file!")
            return

        print("   Configuring Gemini API...")
        genai.configure(api_key=gemini_api_key)

        print(f"   Loading model: {GEMINI_MODEL_NAME}...")
        gemini_model = genai.GenerativeModel(GEMINI_MODEL_NAME)

        logger.info(f"🤖 AI model '{GEMINI_MODEL_NAME}' successfully initialized.")
        print(f"✅ AI model ready: {GEMINI_MODEL_NAME}")
    except Exception as e:
        logger.critical(f"❌ Critical error while initializing Gemini: {e}")
        print(f"❌ ERROR: Failed to initialize AI: {e}")
        traceback.print_exc()
        return

    print("\n[5/6] Configuring Telegram bot...")
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        logger.critical("❌ TELEGRAM_BOT_TOKEN not found!")
        print("❌ ERROR: TELEGRAM_BOT_TOKEN not found in .env file!")
        return

    print("   Building bot application...")
    application = Application.builder().token(token).build()
    print("✅ Bot application configured")

    print("\n[6/6] Registering handlers...")
    # Use partial to bind gemini_model argument to handler
    message_handler_with_model = partial(handle_message, gemini_model=gemini_model)

    # Register global error handler
    print("   - Error handler")
    application.add_error_handler(error_handler)

    # Commands
    print("   - Command handlers (/start, /mydocs, /stats, /clear)")
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("mydocs", my_docs_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CommandHandler("clear", clear_command))

    # Callback queries (inline buttons)
    print("   - Inline button handler")
    application.add_handler(CallbackQueryHandler(button_callback))

    # Handler for all document types (PDF, Excel, Word)
    print("   - Document handler")
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))

    # Handler for audio and voice messages
    print("   - Audio/voice handler")
    application.add_handler(MessageHandler(filters.AUDIO | filters.VOICE, handle_audio))

    # Text message handler with priorities:
    # 1. Check Reply Keyboard buttons
    # 2. Process as regular message
    print("   - Text message handler")
    async def text_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
        # First check Reply Keyboard
        if await handle_reply_keyboard(update, context):
            return
        # If not, process as regular message (question/AI chat)
        await message_handler_with_model(update, context)

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_message_handler))
    print("✅ All handlers registered")

    print("\n" + "=" * 60)
    print("✅ Бот успешно запущен!")

    # Track startup time
    startup_duration_ms = (time.time() - startup_start_time) * 1000
    track_startup_time(startup_duration_ms)
    print(f"⏱️  Startup completed in {startup_duration_ms:.2f}ms")

    # Run health check
    print("\n🏥 Running health check...")
    health_status = health_checker.get_full_status()
    print(f"   Database: {health_status['services']['database']['status']}")
    print(f"   Redis: {health_status['services']['redis']['status']}")
    print(f"   AI Service: {health_status['services']['ai_service']['status']}")
    print(f"   Overall: {health_status['status'].upper()}")

    print("\n" + "=" * 60)
    print("Бот готов к работе. Нажмите Ctrl+C для остановки.")
    print("=" * 60 + "\n")
    logger.info("✅ Bot ready and starting polling...")

    application.run_polling()

if __name__ == '__main__':
    main()
