"""
Улучшенные обработчики команд с профессиональным UI.
Версия для Fiverr демо с расширенным функционалом.
"""
from telegram import Update
from telegram.ext import ContextTypes
from sqlalchemy.orm import Session

from database.database import SessionLocal
from database import crud
from ui import (
    get_main_menu_keyboard,
    get_settings_keyboard,
    get_language_keyboard,
    get_ai_mode_keyboard,
    get_premium_keyboard,
    get_document_actions_keyboard,
    get_pagination_keyboard,
    format_welcome_message,
    format_stats_message,
    format_document_list,
    format_document_info,
    format_help_message,
    format_premium_promo,
    format_comparison_table,
)
from analytics import get_user_stats, get_document_stats

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Команда /start - приветствие и главное меню"""
    user = update.effective_user
    db: Session = SessionLocal()
    try:
        # Проверяем, новый ли пользователь
        existing_user = db.query(crud.models.User).filter(
            crud.models.User.user_id == user.id
        ).first()
        is_new = existing_user is None

        # Создаем или получаем пользователя
        crud.get_or_create_user(db, user.id, user.username, user.first_name, user.last_name)

        # Отправляем приветственное сообщение
        welcome_text = format_welcome_message(
            user.first_name or user.username or 'там',
            is_new=is_new
        )

        if update.message:
            await update.message.reply_html(
                welcome_text,
                reply_markup=get_main_menu_keyboard()
            )
        elif update.callback_query:
            await update.callback_query.edit_message_text(
                text=welcome_text,
                reply_markup=get_main_menu_keyboard(),
                parse_mode='HTML'
            )
    finally:
        db.close()

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Команда /stats - показать статистику пользователя"""
    user = update.effective_user
    db: Session = SessionLocal()
    try:
        # Получаем статистику
        stats = get_user_stats(db, user.id)

        if not stats:
            message = "📊 Статистика недоступна. Начните использовать бота!"
        else:
            message = format_stats_message(stats)

        if update.message:
            await update.message.reply_html(
                message,
                reply_markup=get_main_menu_keyboard()
            )
        elif update.callback_query:
            await update.callback_query.edit_message_text(
                text=message,
                reply_markup=get_main_menu_keyboard(),
                parse_mode='HTML'
            )
    finally:
        db.close()

async def my_docs_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Команда /mydocs - список всех документов"""
    user = update.effective_user
    db: Session = SessionLocal()
    try:
        db_user = crud.get_or_create_user(db, user.id, user.username, user.first_name, user.last_name)
        documents = crud.get_all_user_documents(db, db_user)

        # Преобразуем документы в формат для отображения
        docs_list = []
        for doc in documents:
            # Определяем тип
            file_name = doc.file_name.lower()
            if file_name.endswith('.pdf'):
                doc_type = 'pdf'
            elif file_name.endswith(('.xlsx', '.xls')):
                doc_type = 'excel'
            elif file_name.endswith('.docx'):
                doc_type = 'word'
            elif doc.file_path.startswith('http'):
                doc_type = 'url'
            else:
                doc_type = 'other'

            docs_list.append({
                'id': doc.id,
                'name': doc.file_name,
                'type': doc_type,
                'created_at': doc.created_at.strftime('%d.%m.%Y'),
                'questions_count': 0,  # TODO: добавить tracking
                'is_active': db_user.active_document_id == doc.id,
            })

        # Форматируем список
        page = context.user_data.get('docs_page', 1)
        per_page = 5
        total_pages = (len(docs_list) + per_page - 1) // per_page

        message = format_document_list(docs_list, page, per_page)

        # Создаем клавиатуру с документами
        keyboard_buttons = []
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        page_docs = docs_list[start_idx:end_idx]

        for doc in page_docs:
            icon = {'pdf': '📄', 'excel': '📊', 'word': '📝', 'url': '🌐', 'audio': '🎤'}.get(doc['type'], '📎')
            active_mark = " ✅" if doc['is_active'] else ""
            button_text = f"{icon} {doc['name'][:30]}{active_mark}"

            from telegram import InlineKeyboardButton
            keyboard_buttons.append([
                InlineKeyboardButton(button_text, callback_data=f"doc_{doc['id']}")
            ])

        # Добавляем пагинацию если нужно
        if total_pages > 1:
            nav_buttons = []
            if page > 1:
                from telegram import InlineKeyboardButton
                nav_buttons.append(InlineKeyboardButton("⬅️", callback_data=f"docs_page_{page-1}"))
            nav_buttons.append(InlineKeyboardButton(f"{page}/{total_pages}", callback_data="page_info"))
            if page < total_pages:
                from telegram import InlineKeyboardButton
                nav_buttons.append(InlineKeyboardButton("➡️", callback_data=f"docs_page_{page+1}"))
            keyboard_buttons.append(nav_buttons)

        # Добавляем кнопку "Назад"
        from telegram import InlineKeyboardButton, InlineKeyboardMarkup
        keyboard_buttons.append([InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")])

        if update.message:
            await update.message.reply_html(
                message,
                reply_markup=InlineKeyboardMarkup(keyboard_buttons)
            )
        elif update.callback_query:
            await update.callback_query.edit_message_text(
                text=message,
                reply_markup=InlineKeyboardMarkup(keyboard_buttons),
                parse_mode='HTML'
            )
    finally:
        db.close()

async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Команда /clear - очистить все документы"""
    user = update.effective_user
    db: Session = SessionLocal()
    try:
        db_user = crud.get_or_create_user(db, user.id, user.username, user.first_name, user.last_name)
        crud.clear_user_documents(db, db_user)

        message = """
🗑️ <b>Все документы удалены!</b>

Ваши данные успешно очищены.
Вы можете загрузить новые документы.
"""

        if update.message:
            await update.message.reply_html(
                message,
                reply_markup=get_main_menu_keyboard()
            )
        elif update.callback_query:
            await update.callback_query.edit_message_text(
                text=message,
                reply_markup=get_main_menu_keyboard(),
                parse_mode='HTML'
            )
    finally:
        db.close()

async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Команда /settings - настройки бота"""
    message = """
⚙️ <b>Настройки</b>

Выберите параметр для настройки:
"""

    if update.message:
        await update.message.reply_html(
            message,
            reply_markup=get_settings_keyboard()
        )
    elif update.callback_query:
        await update.callback_query.edit_message_text(
            text=message,
            reply_markup=get_settings_keyboard(),
            parse_mode='HTML'
        )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Команда /help - справка"""
    message = format_help_message()

    if update.message:
        await update.message.reply_html(
            message,
            reply_markup=get_main_menu_keyboard()
        )
    elif update.callback_query:
        await update.callback_query.edit_message_text(
            text=message,
            reply_markup=get_main_menu_keyboard(),
            parse_mode='HTML'
        )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик всех callback кнопок"""
    query = update.callback_query
    await query.answer()

    callback_data = query.data

    # Главное меню
    if callback_data == 'main_menu':
        await start(update, context)

    # Мои документы
    elif callback_data == 'my_docs':
        await my_docs_command(update, context)

    # Статистика
    elif callback_data == 'stats':
        await stats_command(update, context)

    # Настройки
    elif callback_data == 'settings':
        await settings_command(update, context)

    # Помощь
    elif callback_data == 'help':
        await help_command(update, context)

    # Язык
    elif callback_data == 'language':
        await query.edit_message_text(
            text="🌐 <b>Выберите язык интерфейса:</b>",
            reply_markup=get_language_keyboard(),
            parse_mode='HTML'
        )

    # Изменение языка
    elif callback_data.startswith('lang_'):
        lang_code = callback_data.split('_')[1]
        # TODO: Сохранить язык в БД
        await query.edit_message_text(
            text=f"✅ Язык изменен! (Feature в разработке)\n\nSelected: {lang_code.upper()}",
            reply_markup=get_main_menu_keyboard(),
            parse_mode='HTML'
        )

    # Режим AI
    elif callback_data == 'ai_mode':
        await query.edit_message_text(
            text="🤖 <b>Выберите режим AI:</b>",
            reply_markup=get_ai_mode_keyboard(),
            parse_mode='HTML'
        )

    # Изменение режима AI
    elif callback_data.startswith('mode_'):
        mode = callback_data.split('_')[1]
        # TODO: Сохранить режим в БД
        mode_names = {'fast': 'Быстрый', 'standard': 'Стандартный', 'advanced': 'Продвинутый'}
        await query.edit_message_text(
            text=f"✅ Режим изменен на: <b>{mode_names.get(mode, mode)}</b>",
            reply_markup=get_settings_keyboard(),
            parse_mode='HTML'
        )

    # Premium
    elif callback_data == 'premium':
        await query.edit_message_text(
            text=format_premium_promo(),
            reply_markup=get_premium_keyboard(),
            parse_mode='HTML'
        )

    # Сравнение тарифов
    elif callback_data == 'compare_plans':
        await query.edit_message_text(
            text=format_comparison_table(),
            reply_markup=get_premium_keyboard(),
            parse_mode='HTML'
        )

    # Пробный период
    elif callback_data == 'trial':
        await query.edit_message_text(
            text="🎁 <b>Пробный период активирован!</b>\n\nУ вас есть 7 дней Premium доступа.\n(Feature в разработке)",
            reply_markup=get_main_menu_keyboard(),
            parse_mode='HTML'
        )

    # Просмотр документа
    elif callback_data.startswith('doc_'):
        doc_id = int(callback_data.split('_')[1])
        db: Session = SessionLocal()
        try:
            doc_stats = get_document_stats(db, doc_id)
            if doc_stats:
                await query.edit_message_text(
                    text=format_document_info(doc_stats),
                    reply_markup=get_document_actions_keyboard(doc_id),
                    parse_mode='HTML'
                )
        finally:
            db.close()

    # Активировать документ
    elif callback_data.startswith('activate_'):
        doc_id = int(callback_data.split('_')[1])
        user = update.effective_user
        db: Session = SessionLocal()
        try:
            db_user = crud.get_or_create_user(db, user.id, user.username, user.first_name, user.last_name)
            crud.set_active_document(db, db_user, doc_id)
            await query.answer("✅ Документ активирован!")
            # Обновляем сообщение
            doc_stats = get_document_stats(db, doc_id)
            await query.edit_message_text(
                text=format_document_info(doc_stats),
                reply_markup=get_document_actions_keyboard(doc_id),
                parse_mode='HTML'
            )
        finally:
            db.close()

    # Удалить документ
    elif callback_data.startswith('delete_'):
        doc_id = int(callback_data.split('_')[1])
        # TODO: Добавить подтверждение удаления
        await query.answer("🗑️ Удаление документов будет добавлено", show_alert=True)

    # Очистить все
    elif callback_data == 'clear_all':
        await clear_command(update, context)

    # Пагинация документов
    elif callback_data.startswith('docs_page_'):
        page = int(callback_data.split('_')[2])
        context.user_data['docs_page'] = page
        await my_docs_command(update, context)

    # Заглушка для неизвестных callback
    else:
        await query.answer(f"⚙️ Feature в разработке: {callback_data}", show_alert=True)
