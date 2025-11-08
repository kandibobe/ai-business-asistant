# handlers/messages.py

from telegram import Update
from telegram.ext import ContextTypes
import google.generativeai as genai
from sqlalchemy.orm import Session

from database.database import SessionLocal
from database import crud

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE, gemini_model: genai.GenerativeModel):
    user = update.effective_user
    question = update.message.text
    
    db: Session = SessionLocal()
    try:
        db_user = crud.get_or_create_user(db, user.id, user.username, user.first_name, user.last_name)
        
        # --- КЛЮЧЕВОЕ ИЗМЕНЕНИЕ ---
        # active_document = crud.get_latest_document_for_user(db, db_user) # СТАРАЯ ЛОГИКА
        active_document = crud.get_active_document_for_user(db, db_user) # НОВАЯ ЛОГИКА
        
        if not active_document:
            await update.message.reply_text(
                "У вас не выбран активный документ. Выберите его из списка /mydocs или загрузите новый.",
                reply_markup=get_main_menu_keyboard() # Импортируем из common
            )
            return
            
        document_text = latest_document.extracted_text
        thinking_message = await update.message.reply_text("🧠 Думаю над вашим вопросом...")

        prompt = f"""
        Ты — эксперт по бизнес-аналитике. Проанализируй предоставленный ниже текст документа и ответь на вопрос пользователя.
        Твой ответ должен быть четким, по существу и основываться ИСКЛЮЧИТЕЛЬНО на информации из документа.
        Не придумывай ничего, чего нет в тексте.

        --- ТЕКСТ ДОКУМЕНТА ---
        {document_text}
        --- КОНЕЦ ТЕКСТА ДОКУМЕНТА ---

        ВОПРОС ПОЛЬЗОВАТЕЛЯ:
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
                text=f"❌ Произошла ошибка при обращении к AI. Попробуйте еще раз.\nДетали: {e}",
                chat_id=thinking_message.chat_id,
                message_id=thinking_message.message_id
            )
    finally:
        db.close()