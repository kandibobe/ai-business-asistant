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
from handlers.common_enhanced import start, clear_command, button_callback, my_docs_command, stats_command
from handlers.documents import handle_document
from handlers.messages import handle_message
from handlers.reply_keyboard_handler import handle_reply_keyboard
from audio import handle_audio
from database.database import init_db
from migrate_language import migrate_language_field

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Global error handler for all bot handlers."""
    logger.error("❌ An error occurred while processing update:", exc_info=context.error)

    # Send error message to user
    try:
        if isinstance(update, Update) and update.effective_message:
            error_message = (
                "⚠️ An error occurred while processing your request.\n\n"
                "Please try again or contact administrator."
            )

            # Show details for some critical errors
            if context.error:
                error_type = type(context.error).__name__
                if "Database" in error_type or "SQL" in error_type:
                    error_message += "\n\n💡 Database migration may be required. Run: python migrate_db.py"
                elif "Connection" in error_type or "Network" in error_type:
                    error_message += "\n\n💡 Connection problem. Check Redis and PostgreSQL."

            await update.effective_message.reply_text(error_message)
    except Exception as e:
        logger.error(f"❌ Failed to send error message to user: {e}")

def main() -> None:
    print("=" * 60)
    print("🤖 AI Business Assistant Starting...")
    print("=" * 60)

    print("\n[1/6] Loading environment variables...")
    load_dotenv()
    print("✅ Environment loaded")

    print("\n[2/6] Initializing database...")
    init_db()
    print("✅ Database ready")

    # Run language migration
    print("\n[3/6] Running database migrations...")
    logger.info("🌍 Running language migration...")
    migrate_language_field()
    print("✅ Migrations completed")

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
    print("Бот готов к работе. Нажмите Ctrl+C для остановки.")
    print("=" * 60 + "\n")
    logger.info("✅ Bot ready and starting polling...")

    application.run_polling()

if __name__ == '__main__':
    main()
