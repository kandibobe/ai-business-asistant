"""
Клавиатуры для инструментов разработчика и интеграций.
"""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def get_developer_tools_menu() -> InlineKeyboardMarkup:
    """Главное меню инструментов разработчика"""
    keyboard = [
        [
            InlineKeyboardButton("🛠️ Утилиты", callback_data='dev_utilities'),
            InlineKeyboardButton("🔌 Интеграции", callback_data='dev_integrations'),
        ],
        [
            InlineKeyboardButton("💻 Форматтеры", callback_data='dev_formatters'),
            InlineKeyboardButton("🔐 Генераторы", callback_data='dev_generators'),
        ],
        [
            InlineKeyboardButton("🤖 AI Chat", callback_data='ai_chat_mode'),
            InlineKeyboardButton("❓ Помощь", callback_data='dev_help'),
        ],
        [InlineKeyboardButton("⬅️ Главное меню", callback_data='main_menu')],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_utilities_menu() -> InlineKeyboardMarkup:
    """Меню утилит"""
    keyboard = [
        [
            InlineKeyboardButton("📊 JSON", callback_data='tool_json'),
            InlineKeyboardButton("🔣 Base64", callback_data='tool_base64'),
        ],
        [
            InlineKeyboardButton("🔐 Hash", callback_data='tool_hash'),
            InlineKeyboardButton("🆔 UUID", callback_data='tool_uuid'),
        ],
        [
            InlineKeyboardButton("🔍 Regex", callback_data='tool_regex'),
            InlineKeyboardButton("🕐 Cron", callback_data='tool_cron'),
        ],
        [
            InlineKeyboardButton("🔢 Калькулятор", callback_data='tool_calc'),
            InlineKeyboardButton("🎨 Цвета", callback_data='tool_color'),
        ],
        [InlineKeyboardButton("⬅️ Назад", callback_data='developer_tools')],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_formatters_menu() -> InlineKeyboardMarkup:
    """Меню форматтеров"""
    keyboard = [
        [
            InlineKeyboardButton("📄 JSON Format", callback_data='format_json'),
            InlineKeyboardButton("🗜️ JSON Minify", callback_data='format_json_min'),
        ],
        [
            InlineKeyboardButton("🗄️ SQL Format", callback_data='format_sql'),
            InlineKeyboardButton("🔗 URL Encode", callback_data='format_url_encode'),
        ],
        [
            InlineKeyboardButton("🔓 URL Decode", callback_data='format_url_decode'),
            InlineKeyboardButton("📅 Timestamp", callback_data='format_timestamp'),
        ],
        [InlineKeyboardButton("⬅️ Назад", callback_data='developer_tools')],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_generators_menu() -> InlineKeyboardMarkup:
    """Меню генераторов"""
    keyboard = [
        [
            InlineKeyboardButton("🆔 UUID", callback_data='gen_uuid'),
            InlineKeyboardButton("🔐 Password", callback_data='gen_password'),
        ],
        [
            InlineKeyboardButton("🔣 Hash MD5", callback_data='gen_hash_md5'),
            InlineKeyboardButton("🔐 Hash SHA256", callback_data='gen_hash_sha256'),
        ],
        [
            InlineKeyboardButton("📱 QR Code", callback_data='gen_qr'),
            InlineKeyboardButton("✂️ Short URL", callback_data='gen_short_url'),
        ],
        [InlineKeyboardButton("⬅️ Назад", callback_data='developer_tools')],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_integrations_menu() -> InlineKeyboardMarkup:
    """Меню интеграций"""
    keyboard = [
        [
            InlineKeyboardButton("🐙 GitHub", callback_data='api_github'),
            InlineKeyboardButton("📦 NPM", callback_data='api_npm'),
        ],
        [
            InlineKeyboardButton("👤 GitHub User", callback_data='api_github_user'),
            InlineKeyboardButton("🌐 Can I Use", callback_data='api_caniuse'),
        ],
        [
            InlineKeyboardButton("💰 Crypto Price", callback_data='api_crypto'),
            InlineKeyboardButton("🌤️ Weather", callback_data='api_weather'),
        ],
        [
            InlineKeyboardButton("💭 Quote", callback_data='api_quote'),
            InlineKeyboardButton("😄 Joke", callback_data='api_joke'),
        ],
        [InlineKeyboardButton("⬅️ Назад", callback_data='developer_tools')],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_ai_chat_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для AI chat режима"""
    keyboard = [
        [
            InlineKeyboardButton("🎭 Сменить роль", callback_data='ai_role_menu'),
            InlineKeyboardButton("📝 Сменить стиль", callback_data='response_style_menu'),
        ],
        [
            InlineKeyboardButton("💾 История", callback_data='chat_history'),
            InlineKeyboardButton("🗑️ Очистить чат", callback_data='clear_chat'),
        ],
        [
            InlineKeyboardButton("📄 К документам", callback_data='my_docs'),
            InlineKeyboardButton("🏠 Главное меню", callback_data='main_menu'),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_json_tools_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для JSON инструментов"""
    keyboard = [
        [
            InlineKeyboardButton("✅ Validate", callback_data='json_validate'),
            InlineKeyboardButton("📝 Format", callback_data='json_format'),
        ],
        [
            InlineKeyboardButton("🗜️ Minify", callback_data='json_minify'),
            InlineKeyboardButton("⬅️ Назад", callback_data='dev_utilities'),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_hash_algorithms_keyboard() -> InlineKeyboardMarkup:
    """Выбор алгоритма хеширования"""
    keyboard = [
        [
            InlineKeyboardButton("MD5", callback_data='hash_md5'),
            InlineKeyboardButton("SHA1", callback_data='hash_sha1'),
        ],
        [
            InlineKeyboardButton("SHA256", callback_data='hash_sha256'),
            InlineKeyboardButton("SHA512", callback_data='hash_sha512'),
        ],
        [InlineKeyboardButton("⬅️ Назад", callback_data='dev_generators')],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_github_search_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для GitHub поиска"""
    keyboard = [
        [
            InlineKeyboardButton("🔍 Repos", callback_data='github_repos'),
            InlineKeyboardButton("👤 Users", callback_data='github_users'),
        ],
        [
            InlineKeyboardButton("💬 Issues", callback_data='github_issues'),
            InlineKeyboardButton("⬅️ Назад", callback_data='dev_integrations'),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_quick_dev_actions() -> InlineKeyboardMarkup:
    """Быстрые действия для разработчиков (всегда доступны)"""
    keyboard = [
        [
            InlineKeyboardButton("💻 Dev Tools", callback_data='developer_tools'),
            InlineKeyboardButton("🤖 AI Chat", callback_data='ai_chat_mode'),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_crypto_selection_keyboard() -> InlineKeyboardMarkup:
    """Выбор криптовалюты"""
    keyboard = [
        [
            InlineKeyboardButton("₿ Bitcoin", callback_data='crypto_bitcoin'),
            InlineKeyboardButton("Ξ Ethereum", callback_data='crypto_ethereum'),
        ],
        [
            InlineKeyboardButton("💎 BNB", callback_data='crypto_binancecoin'),
            InlineKeyboardButton("⚡ Solana", callback_data='crypto_solana'),
        ],
        [
            InlineKeyboardButton("🔵 Cardano", callback_data='crypto_cardano'),
            InlineKeyboardButton("⚪ Polkadot", callback_data='crypto_polkadot'),
        ],
        [
            InlineKeyboardButton("✏️ Другая", callback_data='crypto_custom'),
            InlineKeyboardButton("⬅️ Назад", callback_data='dev_integrations'),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_main_menu_with_dev_tools() -> InlineKeyboardMarkup:
    """Главное меню с кнопкой Developer Tools"""
    keyboard = [
        [
            InlineKeyboardButton("📄 Мои документы", callback_data='my_docs'),
            InlineKeyboardButton("📊 Статистика", callback_data='stats'),
        ],
        [
            InlineKeyboardButton("💻 Developer Tools", callback_data='developer_tools'),
            InlineKeyboardButton("🤖 AI Chat", callback_data='ai_chat_mode'),
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


def get_tool_result_keyboard(tool_type: str) -> InlineKeyboardMarkup:
    """Клавиатура после результата инструмента"""
    keyboard = [
        [
            InlineKeyboardButton("🔄 Еще раз", callback_data=f'tool_{tool_type}'),
            InlineKeyboardButton("💾 Сохранить", callback_data=f'save_{tool_type}_result'),
        ],
        [
            InlineKeyboardButton("🛠️ Другой инструмент", callback_data='dev_utilities'),
            InlineKeyboardButton("🏠 Главное меню", callback_data='main_menu'),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)
