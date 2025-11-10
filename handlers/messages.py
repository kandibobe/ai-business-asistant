# handlers/messages.py

from telegram import Update
from telegram.ext import ContextTypes
import google.generativeai as genai
from sqlalchemy.orm import Session
import re
from urllib.parse import urlparse
import logging

from database.database import SessionLocal
from database import crud
from ui import get_main_menu_keyboard
from tasks import scrape_url_task

# Импортируем систему безопасности
from utils.security import sanitize_text_input, validate_url, SecurityError
from middleware.rate_limiter import rate_limit

# Импортируем AI helpers с retry logic
from utils.ai_helpers import generate_ai_response, safe_get_text, AIServiceError, truncate_context

# Импортируем кэширование
from utils.cache import ai_chat_cache

logger = logging.getLogger(__name__)

@rate_limit('ai_requests')
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE, gemini_model: genai.GenerativeModel):
    user = update.effective_user
    question = update.message.text

    # БЕЗОПАСНОСТЬ: Санитизация входного текста
    try:
        question = sanitize_text_input(question, max_length=5000)
    except SecurityError as e:
        await update.message.reply_text(
            f"⚠️ Обнаружены потенциально опасные паттерны в вашем сообщении.\n\n"
            f"Пожалуйста, перефразируйте вопрос и попробуйте снова."
        )
        return

    # === PRIORITY 1: Developer Tools Input ===
    # Check if input is expected for developer tools
    from handlers.developer_handlers import handle_developer_tool_input
    if await handle_developer_tool_input(update, context):
        return  # Input processed, exit

    # === PRIORITY 2: AI Chat Mode (without documents) ===
    # Check if AI Chat mode without documents is active
    from handlers.developer_handlers import handle_ai_chat_message
    ai_response = await handle_ai_chat_message(update, context, gemini_model)
    if ai_response:
        # AI Chat mode is active, send response
        await update.message.reply_html(ai_response)
        return

    # === PRIORITY 3: URL Detection ===
    # Check if message contains URL
    url_pattern = r'https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&/=]*)'
    urls = re.findall(url_pattern, question)

    if urls:
        # If URL found, start scraping
        url = urls[0]  # Take the first URL found

        # БЕЗОПАСНОСТЬ: Валидация URL
        is_valid, error_msg = validate_url(url)
        if not is_valid:
            await update.message.reply_text(
                f"❌ Недопустимый URL: {error_msg}\n\n"
                f"URL: {url}\n\n"
                "Пожалуйста, убедитесь, что URL начинается с http:// или https:// "
                "и не ссылается на локальные ресурсы."
            )
            return

        await update.message.reply_text(
            f"🌐 URL обнаружен!\n\n"
            f"Начинаю анализ веб-страницы: {url}\n"
            f"Это может занять некоторое время... Уведомлю когда будет готово."
        )

        scrape_url_task.delay(
            chat_id=update.message.chat_id,
            user_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            url=url
        )
        return

    # === PRIORITY 4: Document Q&A ===
    db: Session = SessionLocal()
    try:
        db_user = crud.get_or_create_user(db, user.id, user.username, user.first_name, user.last_name)

        # Get active document (not latest)
        active_document = crud.get_active_document_for_user(db, db_user)

        if not active_document:
            await update.message.reply_text(
                "You don't have an active document selected.\n\n"
                "💡 Or use <b>🤖 AI Chat</b> to chat without documents!",
                reply_markup=get_main_menu_keyboard(),
                parse_mode='HTML'
            )
            return

        # Truncate document text if too long
        document_text = truncate_context(active_document.extracted_text, max_tokens=25000)

        thinking_message = await update.message.reply_text("🧠 Thinking about your question...")

        prompt = f"""
        You are a business analytics expert. Analyze the document text provided below and answer the user's question.
        Your answer should be clear, concise and based EXCLUSIVELY on the information from the document.
        Do not make up anything that is not in the text.

        --- DOCUMENT TEXT ---
        {document_text}
        --- END OF DOCUMENT TEXT ---

        USER'S QUESTION:
        "{question}"
        """

        try:
            # Check cache first
            cache_key = f"doc_{active_document.id}_{question}"
            cached_response = ai_chat_cache.get(cache_key)

            if cached_response:
                logger.info(f"Using cached response for user {user.id}")
                answer_text = cached_response.get('text', 'No answer available.')
            else:
                # Use retry logic helper
                logger.info(f"Generating AI response for user {user.id} (doc: {active_document.id})")
                response = generate_ai_response(gemini_model, prompt)
                answer_text = safe_get_text(response)

                if not answer_text:
                    raise AIServiceError("AI did not return a valid response")

                # Cache the response
                ai_chat_cache.set(cache_key, {'text': answer_text}, ttl=3600)

            await context.bot.edit_message_text(
                text=answer_text,
                chat_id=thinking_message.chat_id,
                message_id=thinking_message.message_id
            )

        except AIServiceError as e:
            logger.error(f"AI service error for user {user.id}: {str(e)}")
            await context.bot.edit_message_text(
                text=f"❌ AI service temporarily unavailable.\n\n{str(e)}\n\nPlease try again in a few moments.",
                chat_id=thinking_message.chat_id,
                message_id=thinking_message.message_id
            )
        except Exception as e:
            logger.exception(f"Unexpected error in message handler for user {user.id}")
            await context.bot.edit_message_text(
                text=f"❌ An unexpected error occurred. Our team has been notified.\n\nPlease try again later.",
                chat_id=thinking_message.chat_id,
                message_id=thinking_message.message_id
            )
    finally:
        db.close()