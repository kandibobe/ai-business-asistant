# handlers/common.py

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from sqlalchemy.orm import Session

from database.database import SessionLocal
from database import crud

# --- Тексты ---
WELCOME_MESSAGE = "Привет, {}! Я твой AI Business Intelligence Agent. Чем могу помочь?"
HELP_MESSAGE = "..." # (оставим без изменений)

# --- Клавиатуры ---
def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("📚 Мои документы", callback_data='my_docs')],
        [InlineKeyboardButton("❓ Инструкция", callback_data='help')],
        [InlineKeyboardButton("🗑️ Очистить мои данные", callback_data='confirm_clear')],
    ]
    return InlineKeyboardMarkup(keyboard)

# --- Обработчики ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    db: Session = SessionLocal()
    try:
        crud.get_or_create_user(db, user.id, user.username, user.first_name, user.last_name)
        await update.message.reply_html(
            WELCOME_MESSAGE.format(user.mention_html()),
            reply_markup=get_main_menu_keyboard()
        )
    finally:
        db.close()

async def my_docs_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Показывает список документов пользователя."""
    user = update.effective_user
    db: Session = SessionLocal()
    try:
        db_user = crud.get_or_create_user(db, user.id, user.username, user.first_name, user.last_name)
        documents = crud.get_all_user_documents(db, db_user)
        
        if not documents:
            await update.message.reply_text(
                "Вы еще не загрузили ни одного документа. Просто отправьте мне PDF-файл.",
                reply_markup=get_main_menu_keyboard()
            )
            return

        keyboard = []
        for doc in documents:
            # Добавляем эмодзи, если документ активен
            is_active_icon = "🔹" if db_user.active_document_id == doc.id else "🔸"
            button_text = f"{is_active_icon} {doc.filename}"
            keyboard.append([InlineKeyboardButton(button_text, callback_data=f'select_doc_{doc.id}')])
        
        keyboard.append([InlineKeyboardButton("« Назад в меню", callback_data='start')])
        
        await update.message.reply_text(
            "Выберите документ для работы:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    finally:
        db.close()

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатывает все нажатия на инлайн-кнопки."""
    query = update.callback_query
    await query.answer()
    
    user = update.effective_user
    callback_data = query.data
    db: Session = SessionLocal()
    try:
        db_user = crud.get_or_create_user(db, user.id, user.username, user.first_name, user.last_name)

        if callback_data == 'start':
            await query.edit_message_text(
                text=WELCOME_MESSAGE.format(user.mention_html()),
                parse_mode='HTML',
                reply_markup=get_main_menu_keyboard()
            )
        elif callback_data == 'my_docs':
            documents = crud.get_all_user_documents(db, db_user)
            if not documents:
                await query.edit_message_text(
                    text="Вы еще не загрузили ни одного документа. Просто отправьте мне PDF-файл.",
                    reply_markup=get_main_menu_keyboard()
                )
                return
            
            keyboard = []
            for doc in documents:
                is_active_icon = "🔹" if db_user.active_document_id == doc.id else "🔸"
                button_text = f"{is_active_icon} {doc.filename}"
                keyboard.append([InlineKeyboardButton(button_text, callback_data=f'select_doc_{doc.id}')])
            
            keyboard.append([InlineKeyboardButton("« Назад в меню", callback_data='start')])
            await query.edit_message_text(
                text="Выберите документ для работы:",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        elif callback_data.startswith('select_doc_'):
            doc_id = int(callback_data.split('_')[2])
            crud.set_active_document(db, db_user, doc_id)
            active_doc = crud.get_active_document_for_user(db, db_user)
            await query.edit_message_text(
                text=f"✅ Активный документ изменен на:\n\n📄 **{active_doc.filename}**\n\nТеперь можете задавать по нему вопросы.",
                parse_mode='HTML',
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("« К списку документов", callback_data='my_docs')]])
            )
        elif callback_data == 'help':
            await query.edit_message_text(
                text="📖 **Инструкция по использованию:**\n\n"
                     "**Поддерживаемые форматы:**\n"
                     "📄 PDF (.pdf)\n"
                     "📊 Excel (.xlsx, .xls)\n"
                     "📝 Word (.docx)\n"
                     "🎙️ Аудио/Голосовые сообщения\n\n"
                     "**Как работать:**\n"
                     "1. Отправьте файл любого поддерживаемого формата\n"
                     "2. Я автоматически извлеку текст/данные и сделаю документ активным\n"
                     "3. Задавайте вопросы по активному документу через AI-анализ\n"
                     "4. Используйте /mydocs для переключения между документами\n\n"
                     "**Особенности:**\n"
                     "• Excel: извлекаю все листы + статистику по числовым данным\n"
                     "• Word: извлекаю текст + таблицы\n"
                     "• Аудио: транскрибация через Whisper API",
                parse_mode='HTML',
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("« Назад в меню", callback_data='start')]])
            )
        elif callback_data == 'confirm_clear':
            keyboard = [
                [InlineKeyboardButton("✅ Да, удалить все", callback_data='clear_confirmed')],
                [InlineKeyboardButton("❌ Отмена", callback_data='start')]
            ]
            await query.edit_message_text(
                text="⚠️ **Внимание!**\n\nВы уверены, что хотите удалить все свои документы? Это действие необратимо.",
                parse_mode='HTML',
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        elif callback_data == 'clear_confirmed':
            num_deleted = crud.delete_user_documents(db, db_user)
            await query.edit_message_text(
                text=f"✅ Удалено документов: {num_deleted}\n\nВаши данные очищены.",
                reply_markup=get_main_menu_keyboard()
            )
    finally:
        db.close()

async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Команда для очистки всех документов пользователя."""
    user = update.effective_user
    db: Session = SessionLocal()
    try:
        db_user = crud.get_or_create_user(db, user.id, user.username, user.first_name, user.last_name)
        keyboard = [
            [InlineKeyboardButton("✅ Да, удалить все", callback_data='clear_confirmed')],
            [InlineKeyboardButton("❌ Отмена", callback_data='start')]
        ]
        await update.message.reply_text(
            "⚠️ **Внимание!**\n\nВы уверены, что хотите удалить все свои документы? Это действие необратимо.",
            parse_mode='HTML',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    finally:
        db.close()