# handlers/messages.py

from telegram import Update
from telegram.ext import ContextTypes
import google.generativeai as genai
from sqlalchemy.orm import Session
import re
from urllib.parse import urlparse

from database.database import SessionLocal
from database import crud
from ui import get_main_menu_keyboard
from tasks import scrape_url_task

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE, gemini_model: genai.GenerativeModel):
    user = update.effective_user
    question = update.message.text

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
        await update.message.reply_text(
            f"🌐 URL detected!\n\n"
            f"Starting web page analysis: {url}\n"
            f"This may take some time... Will notify when ready."
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

        document_text = active_document.extracted_text
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
            response = gemini_model.generate_content(prompt)
            await context.bot.edit_message_text(
                text=response.text,
                chat_id=thinking_message.chat_id,
                message_id=thinking_message.message_id
            )
        except Exception as e:
            await context.bot.edit_message_text(
                text=f"❌ An error occurred while contacting AI. Please try again.\nDetails: {e}",
                chat_id=thinking_message.chat_id,
                message_id=thinking_message.message_id
            )
    finally:
        db.close()