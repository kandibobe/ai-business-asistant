"""
Расширенные клавиатуры для AI настроек, ролей и стилей.
"""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config.ai_personas import AI_ROLES, RESPONSE_STYLES, AI_MODES


def get_ai_role_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура выбора роли AI"""
    keyboard = []

    # Группируем роли по 2 в строке
    roles_list = [
        ('analyst', AI_ROLES['analyst']),
        ('consultant', AI_ROLES['consultant']),
        ('teacher', AI_ROLES['teacher']),
        ('researcher', AI_ROLES['researcher']),
        ('creative', AI_ROLES['creative']),
        ('assistant', AI_ROLES['assistant']),
        ('lawyer', AI_ROLES['lawyer']),
    ]

    for i in range(0, len(roles_list), 2):
        row = []
        for j in range(2):
            if i + j < len(roles_list):
                role_key, role_config = roles_list[i + j]
                button_text = f"{role_config['icon']} {role_config['name'].split(' ', 1)[1][:15]}"
                row.append(InlineKeyboardButton(button_text, callback_data=f'set_role_{role_key}'))
        keyboard.append(row)

    # Кнопка назад
    keyboard.append([InlineKeyboardButton("⬅️ Назад к настройкам", callback_data='settings')])

    return InlineKeyboardMarkup(keyboard)


def get_response_style_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура выбора стиля ответов"""
    keyboard = []

    styles_list = [
        ('brief', RESPONSE_STYLES['brief']),
        ('standard', RESPONSE_STYLES['standard']),
        ('detailed', RESPONSE_STYLES['detailed']),
        ('bullets', RESPONSE_STYLES['bullets']),
        ('pros_cons', RESPONSE_STYLES['pros_cons']),
        ('eli5', RESPONSE_STYLES['eli5']),
        ('professional', RESPONSE_STYLES['professional']),
    ]

    for i in range(0, len(styles_list), 2):
        row = []
        for j in range(2):
            if i + j < len(styles_list):
                style_key, style_config = styles_list[i + j]
                button_text = f"{style_config['icon']} {style_config['name'].split(' ', 1)[1][:12]}"
                row.append(InlineKeyboardButton(button_text, callback_data=f'set_style_{style_key}'))
        keyboard.append(row)

    keyboard.append([InlineKeyboardButton("⬅️ Назад к настройкам", callback_data='settings')])

    return InlineKeyboardMarkup(keyboard)


def get_ai_mode_keyboard_advanced() -> InlineKeyboardMarkup:
    """Улучшенная клавиатура выбора режима AI с подробной информацией"""
    keyboard = [
        [InlineKeyboardButton(
            f"{AI_MODES['fast']['icon']} Быстрый - {AI_MODES['fast']['speed']}",
            callback_data='set_mode_fast'
        )],
        [InlineKeyboardButton(
            f"{AI_MODES['standard']['icon']} Стандартный - {AI_MODES['standard']['speed']}",
            callback_data='set_mode_standard'
        )],
        [InlineKeyboardButton(
            f"{AI_MODES['advanced']['icon']} Продвинутый - {AI_MODES['advanced']['speed']}",
            callback_data='set_mode_advanced'
        )],
        [InlineKeyboardButton("⬅️ Назад к настройкам", callback_data='settings')],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_advanced_settings_keyboard() -> InlineKeyboardMarkup:
    """Расширенное меню настроек с новыми опциями"""
    keyboard = [
        [
            InlineKeyboardButton("🎭 Роль AI", callback_data='ai_role_menu'),
            InlineKeyboardButton("📝 Стиль ответов", callback_data='response_style_menu'),
        ],
        [
            InlineKeyboardButton("⚡ Режим работы", callback_data='ai_mode'),
            InlineKeyboardButton("🌐 Язык", callback_data='language'),
        ],
        [
            InlineKeyboardButton("🔔 Уведомления", callback_data='toggle_notifications'),
            InlineKeyboardButton("📊 Авто-анализ", callback_data='toggle_auto_analysis'),
        ],
        [
            InlineKeyboardButton("💾 Сохранить все", callback_data='save_settings'),
            InlineKeyboardButton("🔄 Сбросить", callback_data='reset_settings'),
        ],
        [
            InlineKeyboardButton("⬅️ Главное меню", callback_data='main_menu'),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_quick_actions_keyboard(doc_id: int = None, doc_type: str = None) -> InlineKeyboardMarkup:
    """
    Быстрые действия с контекстными кнопками.

    Args:
        doc_id: ID документа (если есть активный)
        doc_type: Тип документа для контекстных действий

    Returns:
        Клавиатура с быстрыми действиями
    """
    keyboard = []

    if doc_id:
        # Если есть активный документ - показываем действия с ним
        keyboard.append([
            InlineKeyboardButton("💬 Задать вопрос", callback_data=f'quick_ask_{doc_id}'),
            InlineKeyboardButton("📋 Краткое содержание", callback_data=f'quick_summary_{doc_id}'),
        ])

        # Контекстные действия в зависимости от типа
        if doc_type == 'excel':
            keyboard.append([
                InlineKeyboardButton("📊 Визуализация", callback_data=f'visualize_{doc_id}'),
                InlineKeyboardButton("📥 Экспорт PDF", callback_data=f'export_pdf_{doc_id}'),
            ])
        else:
            keyboard.append([
                InlineKeyboardButton("🔍 Ключевые слова", callback_data=f'keywords_{doc_id}'),
                InlineKeyboardButton("📥 Экспорт PDF", callback_data=f'export_pdf_{doc_id}'),
            ])

        keyboard.append([
            InlineKeyboardButton("📚 Все документы", callback_data='my_docs'),
        ])
    else:
        # Если нет активного документа - общие действия
        keyboard.append([
            InlineKeyboardButton("📤 Загрузить файл", callback_data='upload_hint'),
            InlineKeyboardButton("📚 Мои документы", callback_data='my_docs'),
        ])

    keyboard.append([
        InlineKeyboardButton("⚙️ Настройки", callback_data='settings'),
        InlineKeyboardButton("❓ Помощь", callback_data='help_context'),
    ])

    return InlineKeyboardMarkup(keyboard)


def get_confirmation_keyboard(action: str, item_id: int = None) -> InlineKeyboardMarkup:
    """
    Клавиатура подтверждения действия.

    Args:
        action: Действие для подтверждения
        item_id: ID элемента (опционально)

    Returns:
        Клавиатура с кнопками Да/Нет
    """
    callback_confirm = f'confirm_{action}' + (f'_{item_id}' if item_id else '')
    callback_cancel = f'cancel_{action}' + (f'_{item_id}' if item_id else '')

    keyboard = [
        [
            InlineKeyboardButton("✅ Да, подтверждаю", callback_data=callback_confirm),
            InlineKeyboardButton("❌ Отмена", callback_data=callback_cancel),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_document_quick_menu(doc_id: int, doc_type: str) -> InlineKeyboardMarkup:
    """
    Быстрое меню для документа с часто используемыми действиями.

    Args:
        doc_id: ID документа
        doc_type: Тип документа

    Returns:
        Компактная клавиатура с основными действиями
    """
    keyboard = [
        [
            InlineKeyboardButton("💬 Вопрос", callback_data=f'ask_{doc_id}'),
            InlineKeyboardButton("📋 Сводка", callback_data=f'summary_{doc_id}'),
            InlineKeyboardButton("🔍 Слова", callback_data=f'keywords_{doc_id}'),
        ],
    ]

    # Вторая строка зависит от типа
    if doc_type == 'excel':
        keyboard.append([
            InlineKeyboardButton("📊 График", callback_data=f'visualize_{doc_id}'),
            InlineKeyboardButton("📥 PDF", callback_data=f'export_pdf_{doc_id}'),
            InlineKeyboardButton("✅ Активный", callback_data=f'activate_{doc_id}'),
        ])
    else:
        keyboard.append([
            InlineKeyboardButton("📥 PDF", callback_data=f'export_pdf_{doc_id}'),
            InlineKeyboardButton("✅ Активный", callback_data=f'activate_{doc_id}'),
            InlineKeyboardButton("🗑️ Удалить", callback_data=f'delete_{doc_id}'),
        ])

    keyboard.append([InlineKeyboardButton("⬅️ Назад", callback_data='my_docs')])

    return InlineKeyboardMarkup(keyboard)


def get_help_topics_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура с темами справки"""
    keyboard = [
        [
            InlineKeyboardButton("📄 Документы", callback_data='help_documents'),
            InlineKeyboardButton("💬 Вопросы", callback_data='help_questions'),
        ],
        [
            InlineKeyboardButton("⚙️ Настройки", callback_data='help_settings'),
            InlineKeyboardButton("📊 Экспорт", callback_data='help_export'),
        ],
        [
            InlineKeyboardButton("🎭 Роли AI", callback_data='help_roles'),
            InlineKeyboardButton("📝 Стили", callback_data='help_styles'),
        ],
        [InlineKeyboardButton("⬅️ Главное меню", callback_data='main_menu')],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_post_answer_keyboard(doc_id: int = None) -> InlineKeyboardMarkup:
    """
    Клавиатура, показываемая после AI ответа.

    Args:
        doc_id: ID документа, по которому был ответ

    Returns:
        Клавиатура с опциями что делать дальше
    """
    keyboard = [
        [
            InlineKeyboardButton("🔄 Другой стиль", callback_data='change_style'),
            InlineKeyboardButton("📊 Визуализировать", callback_data=f'visualize_{doc_id}' if doc_id else 'no_doc'),
        ],
        [
            InlineKeyboardButton("📥 Экспорт PDF", callback_data=f'export_pdf_{doc_id}' if doc_id else 'export_stats_pdf'),
            InlineKeyboardButton("💬 Ещё вопрос", callback_data='ask_again'),
        ],
        [
            InlineKeyboardButton("🏠 Главное меню", callback_data='main_menu'),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)
