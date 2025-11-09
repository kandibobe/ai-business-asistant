"""
Handlers for Developer Tools and AI Chat.
Includes developer tools and AI chat without documents.
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from sqlalchemy.orm import Session

from database.database import SessionLocal
from database import crud
from config.i18n import get_text
from utils.user_utils import get_user_language
from utils.developer_tools import (
    format_json, minify_json, validate_json,
    encode_base64, decode_base64,
    generate_hash, generate_uuids,
    parse_regex, format_sql, parse_cron,
    calculate_expression, color_converter,
    generate_password, url_encode, url_decode,
    timestamp_to_date
)
from utils.free_apis import (
    search_github_repos, search_npm_package,
    check_browser_support, get_public_ip,
    get_random_quote, get_random_joke,
    get_crypto_price, generate_qr_code,
    shorten_url, get_github_user_info,
    get_weather
)
from ui.developer_keyboards import (
    get_developer_tools_menu,
    get_utilities_menu,
    get_formatters_menu,
    get_generators_menu,
    get_integrations_menu,
    get_ai_chat_keyboard,
    get_json_tools_keyboard,
    get_hash_algorithms_keyboard,
    get_github_search_keyboard,
    get_crypto_selection_keyboard,
    get_tool_result_keyboard,
)
from ui.formatters import format_ai_answer
from config.ai_personas import build_ai_prompt, AI_ROLES, RESPONSE_STYLES


# --- Developer Tools Main Menu ---

async def handle_developer_tools(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Main menu for developer tools"""
    query = update.callback_query
    await query.answer()

    lang = get_user_language(update, context)
    message = get_text('dev_tools_title', lang)

    await query.edit_message_text(
        text=message,
        reply_markup=get_developer_tools_menu(),
        parse_mode='HTML'
    )


# --- Utilities Menu ---

async def handle_utilities_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Utilities menu"""
    query = update.callback_query
    await query.answer()

    lang = get_user_language(update, context)
    message = get_text('dev_utilities_menu', lang)

    await query.edit_message_text(
        text=message,
        reply_markup=get_utilities_menu(),
        parse_mode='HTML'
    )


# --- JSON Tools ---

async def handle_json_tool(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """JSON tools"""
    query = update.callback_query
    await query.answer()

    lang = get_user_language(update, context)
    message = get_text('json_tools_menu', lang)

    await query.edit_message_text(
        text=message,
        reply_markup=get_json_tools_keyboard(),
        parse_mode='HTML'
    )


async def handle_json_action(update: Update, context: ContextTypes.DEFAULT_TYPE, action: str) -> None:
    """Handle JSON actions"""
    query = update.callback_query
    await query.answer()

    lang = get_user_language(update, context)

    # Set awaiting input
    context.user_data['awaiting_input'] = action

    # Get translated message based on action
    actions_map = {
        'json_validate': 'awaiting_json_validate',
        'json_format': 'awaiting_json_format',
        'json_minify': 'awaiting_json_minify',
    }

    message_key = actions_map.get(action, 'awaiting_json_validate')
    message = get_text(message_key, lang)

    keyboard = [[InlineKeyboardButton(
        get_text('btn_cancel', lang),
        callback_data='dev_utilities'
    )]]

    await query.edit_message_text(
        text=message,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='HTML'
    )


# --- Base64 Tools ---

async def handle_base64_tool(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Base64 encoding/decoding"""
    query = update.callback_query
    await query.answer()

    lang = get_user_language(update, context)
    action = query.data
    context.user_data['awaiting_input'] = action

    if action == 'tool_base64_encode':
        message = get_text('awaiting_base64_encode', lang)
    else:  # decode
        message = get_text('awaiting_base64_decode', lang)

    keyboard = [[InlineKeyboardButton(
        get_text('btn_cancel', lang),
        callback_data='dev_utilities'
    )]]

    await query.edit_message_text(
        text=message,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='HTML'
    )


# --- Hash Tools ---

async def handle_hash_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Hash algorithm selection menu"""
    query = update.callback_query
    await query.answer()

    lang = get_user_language(update, context)
    message = get_text('hash_menu', lang)

    await query.edit_message_text(
        text=message,
        reply_markup=get_hash_algorithms_keyboard(),
        parse_mode='HTML'
    )


async def handle_hash_algorithm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Hash algorithm selection"""
    query = update.callback_query
    await query.answer()

    lang = get_user_language(update, context)
    algorithm = query.data.replace('hash_', '')
    context.user_data['awaiting_input'] = f'hash_{algorithm}'

    message = get_text('awaiting_hash', lang, algorithm=algorithm.upper())

    keyboard = [[InlineKeyboardButton(
        get_text('btn_cancel', lang),
        callback_data='tool_hash'
    )]]

    await query.edit_message_text(
        text=message,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='HTML'
    )


# --- UUID Generator ---

async def handle_uuid_tool(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Генерация UUID"""
    query = update.callback_query
    await query.answer()

    result = generate_uuids(5)

    await query.edit_message_text(
        text=result,
        reply_markup=get_tool_result_keyboard('uuid'),
        parse_mode='HTML'
    )


# --- Regex Tool ---

async def handle_regex_tool(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Regex тестер"""
    query = update.callback_query
    await query.answer()

    context.user_data['awaiting_input'] = 'tool_regex'

    message = """
🔍 <b>Regex Tester</b>

📤 Отправьте данные в формате:

<code>pattern | text</code>

<i>Пример:</i>
<code>\\d+ | My age is 25 years</code>

<i>С флагами:</i>
<code>hello | i | Hello World</code>
(флаги: i - ignorecase, m - multiline, s - dotall)

⏳ Ожидаю pattern и text...
"""

    keyboard = [[InlineKeyboardButton("❌ Отмена", callback_data='dev_utilities')]]

    await query.edit_message_text(
        text=message,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='HTML'
    )


# --- Cron Parser ---

async def handle_cron_tool(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Cron парсер"""
    query = update.callback_query
    await query.answer()

    context.user_data['awaiting_input'] = 'tool_cron'

    message = """
🕐 <b>Cron Parser</b>

📤 Отправьте cron выражение (5 частей)

<i>Примеры:</i>
<code>* * * * *</code> - каждую минуту
<code>0 * * * *</code> - каждый час
<code>0 0 * * *</code> - каждый день
<code>0 0 * * 0</code> - каждое воскресенье

⏳ Ожидаю cron expression...
"""

    keyboard = [[InlineKeyboardButton("❌ Отмена", callback_data='dev_utilities')]]

    await query.edit_message_text(
        text=message,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='HTML'
    )


# --- Calculator ---

async def handle_calc_tool(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Калькулятор"""
    query = update.callback_query
    await query.answer()

    context.user_data['awaiting_input'] = 'tool_calc'

    message = """
🔢 <b>Калькулятор</b>

📤 Отправьте математическое выражение

<i>Примеры:</i>
<code>2 + 2</code>
<code>100 * 50 / 2</code>
<code>(10 + 5) * 3</code>

💡 Поддерживаются: +, -, *, /, (), %
📊 Результат будет показан в разных форматах (DEC, HEX, BIN)

⏳ Ожидаю выражение...
"""

    keyboard = [[InlineKeyboardButton("❌ Отмена", callback_data='dev_utilities')]]

    await query.edit_message_text(
        text=message,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='HTML'
    )


# --- Color Converter ---

async def handle_color_tool(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Конвертер цветов"""
    query = update.callback_query
    await query.answer()

    context.user_data['awaiting_input'] = 'tool_color'

    message = """
🎨 <b>Color Converter</b>

📤 Отправьте цвет в формате HEX или RGB

<i>Примеры:</i>
<code>#FF5733</code>
<code>#00ff00</code>
<code>rgb(255, 87, 51)</code>

⏳ Ожидаю цвет...
"""

    keyboard = [[InlineKeyboardButton("❌ Отмена", callback_data='dev_utilities')]]

    await query.edit_message_text(
        text=message,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='HTML'
    )


# --- Formatters Menu ---

async def handle_formatters_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Меню форматтеров"""
    query = update.callback_query
    await query.answer()

    message = """
💻 <b>Форматтеры кода и данных</b>

Доступные инструменты:

📄 <b>JSON Format</b> - красивое форматирование
🗜️ <b>JSON Minify</b> - сжатие JSON
🗄️ <b>SQL Format</b> - форматирование SQL
🔗 <b>URL Encode</b> - кодирование URL
🔓 <b>URL Decode</b> - декодирование URL
📅 <b>Timestamp</b> - конвертация Unix timestamp

💡 Отправьте данные после выбора инструмента
"""

    await query.edit_message_text(
        text=message,
        reply_markup=get_formatters_menu(),
        parse_mode='HTML'
    )


# --- Generators Menu ---

async def handle_generators_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Меню генераторов"""
    query = update.callback_query
    await query.answer()

    message = """
🔐 <b>Генераторы</b>

Доступные инструменты:

🆔 <b>UUID</b> - генерация UUID v4
🔐 <b>Password</b> - безопасные пароли
🔣 <b>Hash MD5</b> - MD5 хеши
🔐 <b>Hash SHA256</b> - SHA256 хеши
📱 <b>QR Code</b> - создание QR кодов
✂️ <b>Short URL</b> - сокращение ссылок

💡 Некоторые инструменты требуют ввода данных
"""

    await query.edit_message_text(
        text=message,
        reply_markup=get_generators_menu(),
        parse_mode='HTML'
    )


# --- Integrations Menu ---

async def handle_integrations_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Integrations menu"""
    query = update.callback_query
    await query.answer()

    lang = get_user_language(update, context)
    message = get_text('integrations_menu', lang)

    await query.edit_message_text(
        text=message,
        reply_markup=get_integrations_menu(),
        parse_mode='HTML'
    )


# --- API Handlers ---

async def handle_github_search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Поиск на GitHub"""
    query = update.callback_query
    await query.answer()

    context.user_data['awaiting_input'] = 'api_github'

    message = """
🐙 <b>GitHub Repository Search</b>

📤 Отправьте поисковый запрос

<i>Примеры:</i>
<code>react</code>
<code>machine learning python</code>
<code>telegram bot</code>

💡 Будут показаны топ-5 репозиториев по звездам

⏳ Ожидаю запрос...
"""

    keyboard = [[InlineKeyboardButton("❌ Отмена", callback_data='dev_integrations')]]

    await query.edit_message_text(
        text=message,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='HTML'
    )


async def handle_npm_search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Поиск NPM пакетов"""
    query = update.callback_query
    await query.answer()

    context.user_data['awaiting_input'] = 'api_npm'

    message = """
📦 <b>NPM Package Info</b>

📤 Отправьте название пакета

<i>Примеры:</i>
<code>react</code>
<code>express</code>
<code>axios</code>

💡 Будет показана информация о последней версии

⏳ Ожидаю название пакета...
"""

    keyboard = [[InlineKeyboardButton("❌ Отмена", callback_data='dev_integrations')]]

    await query.edit_message_text(
        text=message,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='HTML'
    )


async def handle_github_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Информация о пользователе GitHub"""
    query = update.callback_query
    await query.answer()

    context.user_data['awaiting_input'] = 'api_github_user'

    message = """
👤 <b>GitHub User Info</b>

📤 Отправьте username

<i>Примеры:</i>
<code>torvalds</code>
<code>gvanrossum</code>

💡 Будет показана полная информация о пользователе

⏳ Ожидаю username...
"""

    keyboard = [[InlineKeyboardButton("❌ Отмена", callback_data='dev_integrations')]]

    await query.edit_message_text(
        text=message,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='HTML'
    )


async def handle_crypto_price_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Меню выбора криптовалюты"""
    query = update.callback_query
    await query.answer()

    message = """
💰 <b>Crypto Prices</b>

Выберите криптовалюту или введите свою:

💡 Цены обновляются в реальном времени от CoinGecko
"""

    await query.edit_message_text(
        text=message,
        reply_markup=get_crypto_selection_keyboard(),
        parse_mode='HTML'
    )


async def handle_crypto_price(update: Update, context: ContextTypes.DEFAULT_TYPE, crypto: str = None) -> None:
    """Получение цены криптовалюты"""
    query = update.callback_query

    if crypto:
        # Прямой выбор из меню
        await query.answer("Загрузка цены...")
        success, result = get_crypto_price(crypto)
    else:
        # Пользовательский ввод
        await query.answer()
        context.user_data['awaiting_input'] = 'api_crypto'

        message = """
💰 <b>Custom Crypto</b>

📤 Отправьте название криптовалюты

<i>Примеры:</i>
<code>dogecoin</code>
<code>ripple</code>
<code>litecoin</code>

💡 Используйте ID из CoinGecko

⏳ Ожидаю название...
"""

        keyboard = [[InlineKeyboardButton("⬅️ Назад", callback_data='api_crypto')]]

        await query.edit_message_text(
            text=message,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='HTML'
        )
        return

    keyboard = [
        [InlineKeyboardButton("🔄 Обновить", callback_data=f'crypto_{crypto}')],
        [InlineKeyboardButton("⬅️ Назад", callback_data='api_crypto')],
    ]

    await query.edit_message_text(
        text=result,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='HTML'
    )


async def handle_weather(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Погода"""
    query = update.callback_query
    await query.answer()

    context.user_data['awaiting_input'] = 'api_weather'

    message = """
🌤️ <b>Weather</b>

📤 Отправьте название города

<i>Примеры:</i>
<code>Moscow</code>
<code>London</code>
<code>New York</code>

⏳ Ожидаю город...
"""

    keyboard = [[InlineKeyboardButton("❌ Отмена", callback_data='dev_integrations')]]

    await query.edit_message_text(
        text=message,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='HTML'
    )


async def handle_quote(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Случайная цитата"""
    query = update.callback_query
    await query.answer("Загрузка цитаты...")

    success, result = get_random_quote()

    keyboard = [
        [InlineKeyboardButton("🔄 Еще одна", callback_data='api_quote')],
        [InlineKeyboardButton("⬅️ Назад", callback_data='dev_integrations')],
    ]

    await query.edit_message_text(
        text=result,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='HTML'
    )


async def handle_joke(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Случайная шутка"""
    query = update.callback_query
    await query.answer("Загрузка шутки...")

    success, result = get_random_joke()

    keyboard = [
        [InlineKeyboardButton("🔄 Еще одна", callback_data='api_joke')],
        [InlineKeyboardButton("⬅️ Назад", callback_data='dev_integrations')],
    ]

    await query.edit_message_text(
        text=result,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='HTML'
    )


# --- AI Chat Mode (without documents) ---

async def handle_ai_chat_mode(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """AI Chat mode without documents"""
    query = update.callback_query
    await query.answer()

    lang = get_user_language(update, context)
    user = update.effective_user
    db: Session = SessionLocal()
    try:
        db_user = crud.get_or_create_user(db, user.id, user.username, user.first_name, user.last_name)

        role = db_user.ai_role or 'assistant'
        style = db_user.response_style or 'standard'

        from config.ai_personas import get_role_display_name, get_style_display_name

        message = get_text(
            'ai_chat_title',
            lang,
            role=get_role_display_name(role),
            style=get_style_display_name(style)
        )

        context.user_data['ai_chat_mode'] = True

        await query.edit_message_text(
            text=message,
            reply_markup=get_ai_chat_keyboard(),
            parse_mode='HTML'
        )
    finally:
        db.close()


async def handle_ai_chat_message(update: Update, context: ContextTypes.DEFAULT_TYPE, gemini_model) -> str:
    """
    Обрабатывает сообщения в AI Chat режиме.
    Возвращает ответ AI или None если режим не активен.
    """
    if not context.user_data.get('ai_chat_mode'):
        return None

    user = update.effective_user
    question = update.message.text

    db: Session = SessionLocal()
    try:
        db_user = crud.get_or_create_user(db, user.id, user.username, user.first_name, user.last_name)

        role = db_user.ai_role or 'assistant'
        style = db_user.response_style or 'standard'
        mode = db_user.ai_mode or 'standard'

        # Строим промпт для AI
        prompt = build_ai_prompt(role, style, mode, question, context=None)

        # Получаем ответ от AI
        response = gemini_model.generate_content(prompt)
        answer = response.text

        # Форматируем ответ
        formatted_answer = format_ai_answer(
            answer=answer,
            role=role,
            style=style,
            processing_time=0,
            source_doc=None
        )

        return formatted_answer

    except Exception as e:
        return f"❌ Ошибка при обработке вопроса: {str(e)}"
    finally:
        db.close()


# --- Text Input Handler ---

async def handle_developer_tool_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """
    Обрабатывает текстовый ввод для инструментов разработчика.
    Возвращает True если ввод был обработан, False если нет.
    """
    awaiting = context.user_data.get('awaiting_input')
    if not awaiting:
        return False

    text = update.message.text
    result_text = ""
    success = True

    try:
        # JSON tools
        if awaiting == 'json_validate':
            success, result_text = validate_json(text)
        elif awaiting == 'json_format':
            success, result_text = format_json(text)
        elif awaiting == 'json_minify':
            success, result_text = minify_json(text)

        # Base64
        elif awaiting == 'tool_base64_encode':
            result_text = encode_base64(text)
        elif awaiting == 'tool_base64_decode':
            success, result_text = decode_base64(text)

        # Hash
        elif awaiting.startswith('hash_'):
            algorithm = awaiting.replace('hash_', '')
            result_text = generate_hash(text, algorithm)

        # Regex
        elif awaiting == 'tool_regex':
            parts = text.split('|')
            if len(parts) == 2:
                pattern, test_text = parts[0].strip(), parts[1].strip()
                success, result_text = parse_regex(pattern, test_text)
            elif len(parts) == 3:
                pattern, flags, test_text = parts[0].strip(), parts[1].strip(), parts[2].strip()
                success, result_text = parse_regex(pattern, test_text, flags)
            else:
                success, result_text = False, "❌ Формат: pattern | text или pattern | flags | text"

        # Cron
        elif awaiting == 'tool_cron':
            success, result_text = parse_cron(text)

        # Calculator
        elif awaiting == 'tool_calc':
            success, result_text = calculate_expression(text)

        # Color
        elif awaiting == 'tool_color':
            success, result_text = color_converter(text)

        # SQL Format
        elif awaiting == 'format_sql':
            result_text = format_sql(text)

        # URL
        elif awaiting == 'format_url_encode':
            result_text = url_encode(text)
        elif awaiting == 'format_url_decode':
            success, result_text = url_decode(text)

        # Timestamp
        elif awaiting == 'format_timestamp':
            success, result_text = timestamp_to_date(text)

        # APIs
        elif awaiting == 'api_github':
            success, result_text = search_github_repos(text, limit=5)
        elif awaiting == 'api_npm':
            success, result_text = search_npm_package(text)
        elif awaiting == 'api_github_user':
            success, result_text = get_github_user_info(text)
        elif awaiting == 'api_crypto':
            success, result_text = get_crypto_price(text)
        elif awaiting == 'api_weather':
            success, result_text = get_weather(text)
        elif awaiting == 'gen_password':
            try:
                length = int(text)
                result_text = generate_password(length, include_special=True)
            except:
                success, result_text = False, "❌ Введите число (длина пароля)"
        elif awaiting == 'gen_qr':
            success, result_text = generate_qr_code(text)
        elif awaiting == 'gen_short_url':
            success, result_text = shorten_url(text)

        else:
            return False

        # Очищаем состояние
        context.user_data.pop('awaiting_input', None)

        # Отправляем результат
        keyboard = [[InlineKeyboardButton("🛠️ Developer Tools", callback_data='developer_tools')]]

        await update.message.reply_html(
            result_text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

        return True

    except Exception as e:
        context.user_data.pop('awaiting_input', None)
        await update.message.reply_text(
            f"❌ Ошибка обработки: {str(e)}",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🛠️ Developer Tools", callback_data='developer_tools')
            ]])
        )
        return True


# --- Password Generator ---

async def handle_password_gen(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Генератор паролей"""
    query = update.callback_query
    await query.answer()

    context.user_data['awaiting_input'] = 'gen_password'

    message = """
🔐 <b>Password Generator</b>

📤 Отправьте длину пароля (число)

<i>Рекомендации:</i>
• Минимум 12 символов
• Оптимально 16-20 символов
• Максимум 64 символа

💡 Пароль будет содержать буквы, цифры и спецсимволы

⏳ Ожидаю длину...
"""

    keyboard = [[InlineKeyboardButton("❌ Отмена", callback_data='dev_generators')]]

    await query.edit_message_text(
        text=message,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='HTML'
    )


async def handle_qr_gen(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """QR Code генератор"""
    query = update.callback_query
    await query.answer()

    context.user_data['awaiting_input'] = 'gen_qr'

    message = """
📱 <b>QR Code Generator</b>

📤 Отправьте текст или URL для QR кода

<i>Примеры:</i>
<code>https://github.com</code>
<code>Hello World</code>
<code>+1234567890</code>

💡 QR код будет доступен по ссылке

⏳ Ожидаю текст...
"""

    keyboard = [[InlineKeyboardButton("❌ Отмена", callback_data='dev_generators')]]

    await query.edit_message_text(
        text=message,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='HTML'
    )


async def handle_short_url(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """URL shortener"""
    query = update.callback_query
    await query.answer()

    context.user_data['awaiting_input'] = 'gen_short_url'

    message = """
✂️ <b>URL Shortener</b>

📤 Отправьте длинный URL

<i>Пример:</i>
<code>https://github.com/user/very-long-repository-name</code>

💡 Будет создана короткая ссылка is.gd

⏳ Ожидаю URL...
"""

    keyboard = [[InlineKeyboardButton("❌ Отмена", callback_data='dev_generators')]]

    await query.edit_message_text(
        text=message,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='HTML'
    )
