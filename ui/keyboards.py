"""
Красивые клавиатуры и UI элементы для Telegram бота.
Профессиональный дизайн для Fiverr демо.
"""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    """Главное меню с красивыми иконками"""
    keyboard = [
        [
            InlineKeyboardButton("📄 Мои документы", callback_data='my_docs'),
            InlineKeyboardButton("📊 Статистика", callback_data='stats'),
        ],
        [
            InlineKeyboardButton("⚙️ Настройки", callback_data='settings'),
            InlineKeyboardButton("❓ Помощь", callback_data='help'),
        ],
        [
            InlineKeyboardButton("🌐 Язык / Language", callback_data='language'),
            InlineKeyboardButton("💎 Premium", callback_data='premium'),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_post_analysis_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура после анализа документа"""
    keyboard = [
        [
            InlineKeyboardButton("💬 Задать вопрос", switch_inline_query_current_chat=""),
            InlineKeyboardButton("📋 Краткое содержание", callback_data='summarize'),
        ],
        [
            InlineKeyboardButton("📊 Извлечь данные", callback_data='extract_data'),
            InlineKeyboardButton("📈 Визуализировать", callback_data='visualize'),
        ],
        [
            InlineKeyboardButton("📥 Экспорт", callback_data='export'),
            InlineKeyboardButton("📚 Все документы", callback_data='my_docs'),
        ],
        [
            InlineKeyboardButton("🏠 Главное меню", callback_data='main_menu'),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_document_actions_keyboard(doc_id: int) -> InlineKeyboardMarkup:
    """Действия с документом"""
    keyboard = [
        [
            InlineKeyboardButton("✅ Сделать активным", callback_data=f'activate_{doc_id}'),
            InlineKeyboardButton("💬 Задать вопрос", callback_data=f'ask_{doc_id}'),
        ],
        [
            InlineKeyboardButton("📋 Краткое содержание", callback_data=f'summary_{doc_id}'),
            InlineKeyboardButton("🔍 Ключевые слова", callback_data=f'keywords_{doc_id}'),
        ],
        [
            InlineKeyboardButton("📥 Скачать отчет", callback_data=f'export_{doc_id}'),
            InlineKeyboardButton("🗑️ Удалить", callback_data=f'delete_{doc_id}'),
        ],
        [
            InlineKeyboardButton("⬅️ Назад", callback_data='my_docs'),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_export_format_keyboard(doc_id: int) -> InlineKeyboardMarkup:
    """Выбор формата экспорта"""
    keyboard = [
        [
            InlineKeyboardButton("📄 PDF", callback_data=f'export_pdf_{doc_id}'),
            InlineKeyboardButton("📊 Excel", callback_data=f'export_excel_{doc_id}'),
        ],
        [
            InlineKeyboardButton("📝 Word", callback_data=f'export_word_{doc_id}'),
            InlineKeyboardButton("📋 Text", callback_data=f'export_txt_{doc_id}'),
        ],
        [
            InlineKeyboardButton("⬅️ Назад", callback_data=f'doc_{doc_id}'),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_language_keyboard() -> InlineKeyboardMarkup:
    """Выбор языка"""
    keyboard = [
        [
            InlineKeyboardButton("🇷🇺 Русский", callback_data='lang_ru'),
            InlineKeyboardButton("🇬🇧 English", callback_data='lang_en'),
        ],
        [
            InlineKeyboardButton("🇪🇸 Español", callback_data='lang_es'),
            InlineKeyboardButton("🇩🇪 Deutsch", callback_data='lang_de'),
        ],
        [
            InlineKeyboardButton("🇫🇷 Français", callback_data='lang_fr'),
            InlineKeyboardButton("🇨🇳 中文", callback_data='lang_zh'),
        ],
        [
            InlineKeyboardButton("⬅️ Назад", callback_data='main_menu'),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_settings_keyboard() -> InlineKeyboardMarkup:
    """Меню настроек"""
    keyboard = [
        [
            InlineKeyboardButton("🌐 Язык интерфейса", callback_data='language'),
            InlineKeyboardButton("🤖 Режим AI", callback_data='ai_mode'),
        ],
        [
            InlineKeyboardButton("🔔 Уведомления", callback_data='notifications'),
            InlineKeyboardButton("📊 Отчеты", callback_data='reports_settings'),
        ],
        [
            InlineKeyboardButton("🗑️ Очистить все", callback_data='clear_all'),
            InlineKeyboardButton("⬅️ Назад", callback_data='main_menu'),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_ai_mode_keyboard() -> InlineKeyboardMarkup:
    """Выбор режима AI"""
    keyboard = [
        [InlineKeyboardButton("⚡ Быстрый (быстро, базово)", callback_data='mode_fast')],
        [InlineKeyboardButton("⭐ Стандартный (баланс)", callback_data='mode_standard')],
        [InlineKeyboardButton("💎 Продвинутый (медленно, детально)", callback_data='mode_advanced')],
        [InlineKeyboardButton("⬅️ Назад", callback_data='settings')],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_premium_keyboard() -> InlineKeyboardMarkup:
    """Меню Premium подписки"""
    keyboard = [
        [InlineKeyboardButton("💎 Купить Premium", url='https://your-payment-link.com')],
        [InlineKeyboardButton("🎁 Попробовать бесплатно", callback_data='trial')],
        [InlineKeyboardButton("📋 Сравнить тарифы", callback_data='compare_plans')],
        [InlineKeyboardButton("⬅️ Назад", callback_data='main_menu')],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_confirm_keyboard(action: str, item_id: int) -> InlineKeyboardMarkup:
    """Подтверждение действия"""
    keyboard = [
        [
            InlineKeyboardButton("✅ Да", callback_data=f'confirm_{action}_{item_id}'),
            InlineKeyboardButton("❌ Нет", callback_data=f'cancel_{action}_{item_id}'),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_quick_actions_reply_keyboard() -> ReplyKeyboardMarkup:
    """Быстрые действия (постоянная клавиатура)"""
    keyboard = [
        [KeyboardButton("📄 Мои документы"), KeyboardButton("📊 Статистика")],
        [KeyboardButton("📤 Загрузить файл"), KeyboardButton("🔗 Добавить URL")],
        [KeyboardButton("❓ Помощь"), KeyboardButton("⚙️ Настройки")],
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_pagination_keyboard(page: int, total_pages: int, callback_prefix: str) -> InlineKeyboardMarkup:
    """Пагинация для списков"""
    keyboard = []

    # Кнопки навигации
    nav_buttons = []
    if page > 1:
        nav_buttons.append(InlineKeyboardButton("⬅️ Пред.", callback_data=f'{callback_prefix}_{page-1}'))

    nav_buttons.append(InlineKeyboardButton(f"📄 {page}/{total_pages}", callback_data='page_info'))

    if page < total_pages:
        nav_buttons.append(InlineKeyboardButton("След. ➡️", callback_data=f'{callback_prefix}_{page+1}'))

    keyboard.append(nav_buttons)
    keyboard.append([InlineKeyboardButton("⬅️ Назад", callback_data='main_menu')])

    return InlineKeyboardMarkup(keyboard)
