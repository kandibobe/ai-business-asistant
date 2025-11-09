"""
Enhanced command handlers with professional UI.
Version for Fiverr demo with extended functionality.
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
    get_stats_actions_keyboard,
    get_pagination_keyboard,
    get_main_reply_keyboard,
    format_welcome_message,
    format_stats_message,
    format_document_list,
    format_document_info,
    format_help_message,
    format_premium_promo,
    format_comparison_table,
)
from config.i18n import get_text
from analytics import get_user_stats, get_document_stats
from handlers.export_handlers import (
    handle_export_menu,
    handle_export_pdf,
    handle_export_stats_pdf,
    handle_visualize_stats,
    handle_visualize_document,
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Command /start - welcome and main menu"""
    user = update.effective_user
    db: Session = SessionLocal()
    try:
        # Check if user is new
        existing_user = db.query(crud.models.User).filter(
            crud.models.User.user_id == user.id
        ).first()
        is_new = existing_user is None

        # Create or get user
        db_user = crud.get_or_create_user(db, user.id, user.username, user.first_name, user.last_name)

        # Get user's language
        lang = db_user.language or 'ru'

        # Send welcome message with i18n support
        if is_new:
            welcome_text = get_text('welcome_new', lang, name=user.first_name or user.username or 'там')
        else:
            welcome_text = get_text('welcome_back', lang, name=user.first_name or user.username or 'там')

        if update.message:
            # Send main menu (inline keyboard)
            await update.message.reply_html(
                welcome_text,
                reply_markup=get_main_menu_keyboard()
            )
            # Send persistent keyboard at bottom (reply keyboard)
            quick_access_text = "⬇️ Use the buttons below for quick access" if lang == 'en' else (
                "⬇️ Используйте кнопки внизу для быстрого доступа" if lang == 'ru' else
                "⬇️ Verwenden Sie die Schaltflächen unten für schnellen Zugriff"
            )
            await update.message.reply_text(
                quick_access_text,
                reply_markup=get_main_reply_keyboard(lang)
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
    """Command /stats - show user statistics with export option"""
    user = update.effective_user
    db: Session = SessionLocal()
    try:
        # Get statistics
        stats = get_user_stats(db, user.id)

        if not stats:
            message = "📊 Statistics unavailable. Start using the bot!"
            keyboard = get_main_menu_keyboard()
        else:
            message = format_stats_message(stats)
            keyboard = get_stats_actions_keyboard()

        if update.message:
            await update.message.reply_html(
                message,
                reply_markup=keyboard
            )
        elif update.callback_query:
            await update.callback_query.edit_message_text(
                text=message,
                reply_markup=keyboard,
                parse_mode='HTML'
            )
    finally:
        db.close()

async def my_docs_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Command /mydocs - list all documents"""
    user = update.effective_user
    db: Session = SessionLocal()
    try:
        db_user = crud.get_or_create_user(db, user.id, user.username, user.first_name, user.last_name)
        documents = crud.get_all_user_documents(db, db_user)

        # Convert documents to display format
        docs_list = []
        for doc in documents:
            # Determine type
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
                'questions_count': 0,  # TODO: add tracking
                'is_active': db_user.active_document_id == doc.id,
            })

        # Format list
        page = context.user_data.get('docs_page', 1)
        per_page = 5
        total_pages = (len(docs_list) + per_page - 1) // per_page

        message = format_document_list(docs_list, page, per_page)

        # Create keyboard with documents
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

    # === EXPORT HANDLERS ===

    # Меню экспорта документа
    elif callback_data.startswith('export_') and not callback_data.startswith('export_pdf_') and not callback_data.startswith('export_stats'):
        doc_id = int(callback_data.split('_')[1])
        await handle_export_menu(update, context, doc_id)

    # Экспорт документа в PDF
    elif callback_data.startswith('export_pdf_'):
        doc_id = int(callback_data.split('_')[2])
        await handle_export_pdf(update, context, doc_id)

    # Экспорт статистики в PDF
    elif callback_data == 'export_stats_pdf':
        await handle_export_stats_pdf(update, context)

    # Визуализация статистики
    elif callback_data == 'visualize_stats':
        await handle_visualize_stats(update, context)

    # Визуализация данных документа
    elif callback_data.startswith('visualize_'):
        doc_id = int(callback_data.split('_')[1])
        await handle_visualize_document(update, context, doc_id)

    # Краткое содержание документа
    elif callback_data.startswith('summary_'):
        doc_id = int(callback_data.split('_')[1])
        await query.answer("📋 Генерация краткого содержания... (в разработке)", show_alert=True)

    # Ключевые слова документа
    elif callback_data.startswith('keywords_'):
        doc_id = int(callback_data.split('_')[1])
        await query.answer("🔍 Извлечение ключевых слов... (в разработке)", show_alert=True)

    # Задать вопрос по документу
    elif callback_data.startswith('ask_'):
        doc_id = int(callback_data.split('_')[1])
        await query.answer("💬 Просто напишите ваш вопрос в чат!", show_alert=True)

    # === DEVELOPER TOOLS ===

    # Главное меню Developer Tools
    elif callback_data == 'developer_tools':
        from handlers.developer_handlers import handle_developer_tools
        await handle_developer_tools(update, context)

    # Меню утилит
    elif callback_data == 'dev_utilities':
        from handlers.developer_handlers import handle_utilities_menu
        await handle_utilities_menu(update, context)

    # Меню форматтеров
    elif callback_data == 'dev_formatters':
        from handlers.developer_handlers import handle_formatters_menu
        await handle_formatters_menu(update, context)

    # Меню генераторов
    elif callback_data == 'dev_generators':
        from handlers.developer_handlers import handle_generators_menu
        await handle_generators_menu(update, context)

    # Меню интеграций
    elif callback_data == 'dev_integrations':
        from handlers.developer_handlers import handle_integrations_menu
        await handle_integrations_menu(update, context)

    # AI Chat Mode
    elif callback_data == 'ai_chat_mode':
        from handlers.developer_handlers import handle_ai_chat_mode
        await handle_ai_chat_mode(update, context)

    # JSON Tools
    elif callback_data == 'tool_json':
        from handlers.developer_handlers import handle_json_tool
        await handle_json_tool(update, context)
    elif callback_data in ['json_validate', 'json_format', 'json_minify']:
        from handlers.developer_handlers import handle_json_action
        await handle_json_action(update, context, callback_data)

    # Base64
    elif callback_data in ['tool_base64', 'tool_base64_encode', 'tool_base64_decode']:
        from handlers.developer_handlers import handle_base64_tool
        await handle_base64_tool(update, context)

    # Hash
    elif callback_data == 'tool_hash':
        from handlers.developer_handlers import handle_hash_menu
        await handle_hash_menu(update, context)
    elif callback_data in ['hash_md5', 'hash_sha1', 'hash_sha256', 'hash_sha512']:
        from handlers.developer_handlers import handle_hash_algorithm
        await handle_hash_algorithm(update, context)

    # UUID
    elif callback_data == 'tool_uuid' or callback_data == 'gen_uuid':
        from handlers.developer_handlers import handle_uuid_tool
        await handle_uuid_tool(update, context)

    # Regex
    elif callback_data == 'tool_regex':
        from handlers.developer_handlers import handle_regex_tool
        await handle_regex_tool(update, context)

    # Cron
    elif callback_data == 'tool_cron':
        from handlers.developer_handlers import handle_cron_tool
        await handle_cron_tool(update, context)

    # Calculator
    elif callback_data == 'tool_calc':
        from handlers.developer_handlers import handle_calc_tool
        await handle_calc_tool(update, context)

    # Color Converter
    elif callback_data == 'tool_color':
        from handlers.developer_handlers import handle_color_tool
        await handle_color_tool(update, context)

    # Formatters
    elif callback_data == 'format_json':
        from handlers.developer_handlers import handle_json_action
        await handle_json_action(update, context, 'json_format')
    elif callback_data == 'format_json_min':
        from handlers.developer_handlers import handle_json_action
        await handle_json_action(update, context, 'json_minify')
    elif callback_data in ['format_sql', 'format_url_encode', 'format_url_decode', 'format_timestamp']:
        context.user_data['awaiting_input'] = callback_data
        await query.answer("📤 Отправьте данные в чат", show_alert=True)

    # Generators
    elif callback_data == 'gen_password':
        from handlers.developer_handlers import handle_password_gen
        await handle_password_gen(update, context)
    elif callback_data in ['gen_hash_md5', 'gen_hash_sha256']:
        algorithm = callback_data.replace('gen_hash_', '')
        context.user_data['awaiting_input'] = f'hash_{algorithm}'
        await query.answer(f"📤 Отправьте текст для {algorithm.upper()}", show_alert=True)
    elif callback_data == 'gen_qr':
        from handlers.developer_handlers import handle_qr_gen
        await handle_qr_gen(update, context)
    elif callback_data == 'gen_short_url':
        from handlers.developer_handlers import handle_short_url
        await handle_short_url(update, context)

    # API Integrations
    elif callback_data == 'api_github':
        from handlers.developer_handlers import handle_github_search
        await handle_github_search(update, context)
    elif callback_data == 'api_npm':
        from handlers.developer_handlers import handle_npm_search
        await handle_npm_search(update, context)
    elif callback_data == 'api_github_user':
        from handlers.developer_handlers import handle_github_user
        await handle_github_user(update, context)
    elif callback_data == 'api_crypto':
        from handlers.developer_handlers import handle_crypto_price_menu
        await handle_crypto_price_menu(update, context)
    elif callback_data.startswith('crypto_'):
        from handlers.developer_handlers import handle_crypto_price
        crypto = callback_data.replace('crypto_', '')
        await handle_crypto_price(update, context, crypto)
    elif callback_data == 'api_weather':
        from handlers.developer_handlers import handle_weather
        await handle_weather(update, context)
    elif callback_data == 'api_quote':
        from handlers.developer_handlers import handle_quote
        await handle_quote(update, context)
    elif callback_data == 'api_joke':
        from handlers.developer_handlers import handle_joke
        await handle_joke(update, context)
    elif callback_data == 'api_caniuse':
        await query.answer("🌐 Отправьте название веб-фичи (например: flexbox)", show_alert=True)
        context.user_data['awaiting_input'] = 'api_caniuse'

    # Заглушка для неизвестных callback
    else:
        await query.answer(f"⚙️ Feature в разработке: {callback_data}", show_alert=True)
