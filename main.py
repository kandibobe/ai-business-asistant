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
    load_dotenv()
    init_db()

    # Run language migration
    logger.info("🌍 Running language migration...")
    migrate_language_field()

    try:
        gemini_api_key = os.getenv('GEMINI_API_KEY')
        if not gemini_api_key:
            logger.critical("❌ GEMINI_API_KEY not found!")
            return
        genai.configure(api_key=gemini_api_key)
        gemini_model = genai.GenerativeModel(GEMINI_MODEL_NAME)
        logger.info(f"🤖 AI model '{GEMINI_MODEL_NAME}' successfully initialized.")
    except Exception as e:
        logger.critical(f"❌ Critical error while initializing Gemini: {e}")
        return

    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        logger.critical("❌ TELEGRAM_BOT_TOKEN not found!")
        return

    application = Application.builder().token(token).build()

    # Use partial to bind gemini_model argument to handler
    message_handler_with_model = partial(handle_message, gemini_model=gemini_model)

    # Register global error handler
    application.add_error_handler(error_handler)

    # Commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("mydocs", my_docs_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CommandHandler("clear", clear_command))

    # Callback queries (inline buttons)
    application.add_handler(CallbackQueryHandler(button_callback))

    # Handler for all document types (PDF, Excel, Word)
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))

    # Handler for audio and voice messages
    application.add_handler(MessageHandler(filters.AUDIO | filters.VOICE, handle_audio))

    # Text message handler with priorities:
    # 1. Check Reply Keyboard buttons
    # 2. Process as regular message
    async def text_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
        # First check Reply Keyboard
        if await handle_reply_keyboard(update, context):
            return
        # If not, process as regular message (question/AI chat)
        await message_handler_with_model(update, context)

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_message_handler))


    logger.info("✅ Bot ready and starting...")
    application.run_polling()

if __name__ == '__main__':
    main()
