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
    """Generate UUID"""
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
    """Regex tester"""
    query = update.callback_query
    await query.answer()

    context.user_data['awaiting_input'] = 'tool_regex'

    message = """
🔍 <b>Regex Tester</b>

📤 Send data in format:

<code>pattern | text</code>

<i>Example:</i>
<code>\\d+ | My age is 25 years</code>

<i>With flags:</i>
<code>hello | i | Hello World</code>
(flags: i - ignorecase, m - multiline, s - dotall)

⏳ Awaiting pattern and text...
"""

    keyboard = [[InlineKeyboardButton("❌ Cancel", callback_data='dev_utilities')]]

    await query.edit_message_text(
        text=message,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='HTML'
    )


# --- Cron Parser ---

async def handle_cron_tool(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Cron parser"""
    query = update.callback_query
    await query.answer()

    context.user_data['awaiting_input'] = 'tool_cron'

    message = """
🕐 <b>Cron Parser</b>

📤 Send cron expression (5 parts)

<i>Examples:</i>
<code>* * * * *</code> - every minute
<code>0 * * * *</code> - every hour
<code>0 0 * * *</code> - every day
<code>0 0 * * 0</code> - every Sunday

⏳ Awaiting cron expression...
"""

    keyboard = [[InlineKeyboardButton("❌ Cancel", callback_data='dev_utilities')]]

    await query.edit_message_text(
        text=message,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='HTML'
    )


# --- Calculator ---

async def handle_calc_tool(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Calculator"""
    query = update.callback_query
    await query.answer()

    context.user_data['awaiting_input'] = 'tool_calc'

    message = """
🔢 <b>Calculator</b>

📤 Send mathematical expression

<i>Examples:</i>
<code>2 + 2</code>
<code>100 * 50 / 2</code>
<code>(10 + 5) * 3</code>

💡 Supported: +, -, *, /, (), %
📊 Result will be shown in different formats (DEC, HEX, BIN)

⏳ Awaiting expression...
"""

    keyboard = [[InlineKeyboardButton("❌ Cancel", callback_data='dev_utilities')]]

    await query.edit_message_text(
        text=message,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='HTML'
    )


# --- Color Converter ---

async def handle_color_tool(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Color converter"""
    query = update.callback_query
    await query.answer()

    context.user_data['awaiting_input'] = 'tool_color'

    message = """
🎨 <b>Color Converter</b>

📤 Send color in HEX or RGB format

<i>Examples:</i>
<code>#FF5733</code>
<code>#00ff00</code>
<code>rgb(255, 87, 51)</code>

⏳ Awaiting color...
"""

    keyboard = [[InlineKeyboardButton("❌ Cancel", callback_data='dev_utilities')]]

    await query.edit_message_text(
        text=message,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='HTML'
    )


# --- Formatters Menu ---

async def handle_formatters_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Formatters menu"""
    query = update.callback_query
    await query.answer()

    message = """
💻 <b>Code and Data Formatters</b>

Available tools:

📄 <b>JSON Format</b> - beautiful formatting
🗜️ <b>JSON Minify</b> - JSON compression
🗄️ <b>SQL Format</b> - SQL formatting
🔗 <b>URL Encode</b> - URL encoding
🔓 <b>URL Decode</b> - URL decoding
📅 <b>Timestamp</b> - Unix timestamp conversion

💡 Send data after selecting a tool
"""

    await query.edit_message_text(
        text=message,
        reply_markup=get_formatters_menu(),
        parse_mode='HTML'
    )


# --- Generators Menu ---

async def handle_generators_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Generators menu"""
    query = update.callback_query
    await query.answer()

    message = """
🔐 <b>Generators</b>

Available tools:

🆔 <b>UUID</b> - UUID v4 generation
🔐 <b>Password</b> - secure passwords
🔣 <b>Hash MD5</b> - MD5 hashes
🔐 <b>Hash SHA256</b> - SHA256 hashes
📱 <b>QR Code</b> - QR code creation
✂️ <b>Short URL</b> - URL shortening

💡 Some tools require data input
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
    """GitHub search"""
    query = update.callback_query
    await query.answer()

    context.user_data['awaiting_input'] = 'api_github'

    message = """
🐙 <b>GitHub Repository Search</b>

📤 Send search query

<i>Examples:</i>
<code>react</code>
<code>machine learning python</code>
<code>telegram bot</code>

💡 Top 5 repositories by stars will be shown

⏳ Awaiting query...
"""

    keyboard = [[InlineKeyboardButton("❌ Cancel", callback_data='dev_integrations')]]

    await query.edit_message_text(
        text=message,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='HTML'
    )


async def handle_npm_search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """NPM package search"""
    query = update.callback_query
    await query.answer()

    context.user_data['awaiting_input'] = 'api_npm'

    message = """
📦 <b>NPM Package Info</b>

📤 Send package name

<i>Examples:</i>
<code>react</code>
<code>express</code>
<code>axios</code>

💡 Latest version info will be shown

⏳ Awaiting package name...
"""

    keyboard = [[InlineKeyboardButton("❌ Cancel", callback_data='dev_integrations')]]

    await query.edit_message_text(
        text=message,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='HTML'
    )


async def handle_github_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """GitHub user info"""
    query = update.callback_query
    await query.answer()

    context.user_data['awaiting_input'] = 'api_github_user'

    message = """
👤 <b>GitHub User Info</b>

📤 Send username

<i>Examples:</i>
<code>torvalds</code>
<code>gvanrossum</code>

💡 Full user information will be shown

⏳ Awaiting username...
"""

    keyboard = [[InlineKeyboardButton("❌ Cancel", callback_data='dev_integrations')]]

    await query.edit_message_text(
        text=message,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='HTML'
    )


async def handle_crypto_price_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Cryptocurrency selection menu"""
    query = update.callback_query
    await query.answer()

    message = """
💰 <b>Crypto Prices</b>

Select cryptocurrency or enter your own:

💡 Prices updated in real-time from CoinGecko
"""

    await query.edit_message_text(
        text=message,
        reply_markup=get_crypto_selection_keyboard(),
        parse_mode='HTML'
    )


async def handle_crypto_price(update: Update, context: ContextTypes.DEFAULT_TYPE, crypto: str = None) -> None:
    """Get cryptocurrency price"""
    query = update.callback_query

    if crypto:
        # Direct selection from menu
        await query.answer("Loading price...")
        success, result = get_crypto_price(crypto)
    else:
        # User input
        await query.answer()
        context.user_data['awaiting_input'] = 'api_crypto'

        message = """
💰 <b>Custom Crypto</b>

📤 Send cryptocurrency name

<i>Examples:</i>
<code>dogecoin</code>
<code>ripple</code>
<code>litecoin</code>

💡 Use ID from CoinGecko

⏳ Awaiting name...
"""

        keyboard = [[InlineKeyboardButton("⬅️ Back", callback_data='api_crypto')]]

        await query.edit_message_text(
            text=message,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='HTML'
        )
        return

    keyboard = [
        [InlineKeyboardButton("🔄 Refresh", callback_data=f'crypto_{crypto}')],
        [InlineKeyboardButton("⬅️ Back", callback_data='api_crypto')],
    ]

    await query.edit_message_text(
        text=result,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='HTML'
    )


async def handle_weather(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Weather"""
    query = update.callback_query
    await query.answer()

    context.user_data['awaiting_input'] = 'api_weather'

    message = """
🌤️ <b>Weather</b>

📤 Send city name

<i>Examples:</i>
<code>Moscow</code>
<code>London</code>
<code>New York</code>

⏳ Awaiting city...
"""

    keyboard = [[InlineKeyboardButton("❌ Cancel", callback_data='dev_integrations')]]

    await query.edit_message_text(
        text=message,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='HTML'
    )


async def handle_quote(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Random quote"""
    query = update.callback_query
    await query.answer("Loading quote...")

    success, result = get_random_quote()

    keyboard = [
        [InlineKeyboardButton("🔄 Another one", callback_data='api_quote')],
        [InlineKeyboardButton("⬅️ Back", callback_data='dev_integrations')],
    ]

    await query.edit_message_text(
        text=result,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='HTML'
    )


async def handle_joke(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Random joke"""
    query = update.callback_query
    await query.answer("Loading joke...")

    success, result = get_random_joke()

    keyboard = [
        [InlineKeyboardButton("🔄 Another one", callback_data='api_joke')],
        [InlineKeyboardButton("⬅️ Back", callback_data='dev_integrations')],
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
    Processes messages in AI Chat mode.
    Returns AI response or None if mode is not active.
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

        # Build prompt for AI
        prompt = build_ai_prompt(role, style, mode, question, context=None)

        # Get AI response
        response = gemini_model.generate_content(prompt)
        answer = response.text

        # Format response
        formatted_answer = format_ai_answer(
            answer=answer,
            role=role,
            style=style,
            processing_time=0,
            source_doc=None
        )

        return formatted_answer

    except Exception as e:
        return f"❌ Error processing question: {str(e)}"
    finally:
        db.close()


# --- Text Input Handler ---

async def handle_developer_tool_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """
    Processes text input for developer tools.
    Returns True if input was processed, False if not.
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
                success, result_text = False, "❌ Format: pattern | text or pattern | flags | text"

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
                success, result_text = False, "❌ Enter a number (password length)"
        elif awaiting == 'gen_qr':
            success, result_text = generate_qr_code(text)
        elif awaiting == 'gen_short_url':
            success, result_text = shorten_url(text)

        else:
            return False

        # Clear state
        context.user_data.pop('awaiting_input', None)

        # Send result
        keyboard = [[InlineKeyboardButton("🛠️ Developer Tools", callback_data='developer_tools')]]

        await update.message.reply_html(
            result_text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

        return True

    except Exception as e:
        context.user_data.pop('awaiting_input', None)
        await update.message.reply_text(
            f"❌ Processing error: {str(e)}",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🛠️ Developer Tools", callback_data='developer_tools')
            ]])
        )
        return True


# --- Password Generator ---

async def handle_password_gen(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Password generator"""
    query = update.callback_query
    await query.answer()

    context.user_data['awaiting_input'] = 'gen_password'

    message = """
🔐 <b>Password Generator</b>

📤 Send password length (number)

<i>Recommendations:</i>
• Minimum 12 characters
• Optimal 16-20 characters
• Maximum 64 characters

💡 Password will contain letters, numbers and special characters

⏳ Awaiting length...
"""

    keyboard = [[InlineKeyboardButton("❌ Cancel", callback_data='dev_generators')]]

    await query.edit_message_text(
        text=message,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='HTML'
    )


async def handle_qr_gen(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """QR Code generator"""
    query = update.callback_query
    await query.answer()

    context.user_data['awaiting_input'] = 'gen_qr'

    message = """
📱 <b>QR Code Generator</b>

📤 Send text or URL for QR code

<i>Examples:</i>
<code>https://github.com</code>
<code>Hello World</code>
<code>+1234567890</code>

💡 QR code will be available via link

⏳ Awaiting text...
"""

    keyboard = [[InlineKeyboardButton("❌ Cancel", callback_data='dev_generators')]]

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

📤 Send long URL

<i>Example:</i>
<code>https://github.com/user/very-long-repository-name</code>

💡 Short link via is.gd will be created

⏳ Awaiting URL...
"""

    keyboard = [[InlineKeyboardButton("❌ Cancel", callback_data='dev_generators')]]

    await query.edit_message_text(
        text=message,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='HTML'
    )
