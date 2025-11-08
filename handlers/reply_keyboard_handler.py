"""
Обработчик для кнопок быстрого доступа (ReplyKeyboard).
Обрабатывает текстовые команды от кнопок внизу экрана.
"""
from telegram import Update
from telegram.ext import ContextTypes
from sqlalchemy.orm import Session

from database.database import SessionLocal
from database import crud
from config.i18n import get_text
from handlers.common_enhanced import (
    my_docs_command,
    stats_command,
    settings_command,
    help_command
)


async def handle_reply_keyboard(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """
    Обрабатывает нажатия на кнопки быстрого доступа (ReplyKeyboard).

    Returns:
        True если сообщение было обработано как команда от ReplyKeyboard
        False если это обычное сообщение
    """
    if not update.message or not update.message.text:
        return False

    text = update.message.text.strip()
    user = update.effective_user

    # Получаем язык пользователя
    db: Session = SessionLocal()
    try:
        db_user = crud.get_or_create_user(
            db, user.id, user.username, user.first_name, user.last_name
        )
        lang = db_user.language or 'ru'
    finally:
        db.close()

    # Проверяем соответствие текста кнопкам для всех языков
    button_handlers = {
        # Загрузить / Upload / Hochladen
        (get_text('quick_upload', 'ru'),
         get_text('quick_upload', 'en'),
         get_text('quick_upload', 'de')): handle_upload_command,

        # Документы / Documents / Dokumente
        (get_text('quick_docs', 'ru'),
         get_text('quick_docs', 'en'),
         get_text('quick_docs', 'de')): my_docs_command,

        # Чат / Chat
        (get_text('quick_chat', 'ru'),
         get_text('quick_chat', 'en'),
         get_text('quick_chat', 'de')): handle_chat_command,

        # Инструменты / Tools / Werkzeuge
        (get_text('quick_tools', 'ru'),
         get_text('quick_tools', 'en'),
         get_text('quick_tools', 'de')): handle_tools_command,

        # Настройки / Settings / Einstellungen
        (get_text('btn_settings', 'ru'),
         get_text('btn_settings', 'en'),
         get_text('btn_settings', 'de')): settings_command,

        # Помощь / Help / Hilfe
        (get_text('btn_help', 'ru'),
         get_text('btn_help', 'en'),
         get_text('btn_help', 'de')): help_command,

        # Главное меню / Main Menu / Hauptmenü
        (get_text('btn_main_menu', 'ru'),
         get_text('btn_main_menu', 'en'),
         get_text('btn_main_menu', 'de')): handle_main_menu_command,
    }

    # Проверяем, соответствует ли текст какой-либо кнопке
    for button_texts, handler in button_handlers.items():
        if text in button_texts:
            await handler(update, context)
            return True

    return False


async def handle_upload_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка команды 'Загрузить'"""
    user = update.effective_user
    db: Session = SessionLocal()
    try:
        db_user = crud.get_or_create_user(
            db, user.id, user.username, user.first_name, user.last_name
        )
        lang = db_user.language or 'ru'

        message = get_text('upload_instruction', lang)
        if message == '[upload_instruction]':
            # Fallback на русский если перевод не найден
            message = (
                "📤 <b>Загрузка документа</b>\n\n"
                "Отправьте мне файл одного из форматов:\n"
                "• 📄 PDF\n"
                "• 📊 Excel (.xlsx, .xls)\n"
                "• 📝 Word (.docx)\n"
                "• 🎤 Аудио (для транскрипции)\n"
                "• 🌐 URL (ссылка на веб-страницу)\n\n"
                "Я обработаю его и вы сможете задавать вопросы по содержимому!"
            )

        from ui import get_main_menu_keyboard
        await update.message.reply_html(
            message,
            reply_markup=get_main_menu_keyboard()
        )
    finally:
        db.close()


async def handle_chat_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка команды 'Чат' - открывает AI Chat mode"""
    from handlers.developer_handlers import handle_ai_chat_mode

    # Создаем фейковый callback query для handler
    class FakeCallbackQuery:
        def __init__(self, message):
            self.message = message
            self.data = 'ai_chat_mode'

        async def answer(self, *args, **kwargs):
            pass

        async def edit_message_text(self, text, reply_markup=None, parse_mode=None):
            await self.message.reply_html(text, reply_markup=reply_markup)

    fake_query = FakeCallbackQuery(update.message)
    update.callback_query = fake_query

    await handle_ai_chat_mode(update, context)


async def handle_tools_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка команды 'Инструменты' - открывает Developer Tools"""
    from handlers.developer_handlers import handle_developer_tools

    # Создаем фейковый callback query
    class FakeCallbackQuery:
        def __init__(self, message):
            self.message = message
            self.data = 'developer_tools'

        async def answer(self, *args, **kwargs):
            pass

        async def edit_message_text(self, text, reply_markup=None, parse_mode=None):
            await self.message.reply_html(text, reply_markup=reply_markup)

    fake_query = FakeCallbackQuery(update.message)
    update.callback_query = fake_query

    await handle_developer_tools(update, context)


async def handle_main_menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка команды 'Главное меню'"""
    from handlers.common_enhanced import start
    await start(update, context)
