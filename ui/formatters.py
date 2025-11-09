"""
Advanced message formatting with beautiful output.
Used for AI responses, settings, tooltips, etc.
"""
from typing import Dict, Any, List
from datetime import datetime


def format_ai_answer(
    answer: str,
    role: str = 'assistant',
    style: str = 'standard',
    processing_time: float = 0,
    source_doc: str = None
) -> str:
    """
    Formats AI answer with beautiful styling.

    Args:
        answer: AI response text
        role: AI role (for icon)
        style: Response style (for context)
        processing_time: Processing time in seconds
        source_doc: Source document name

    Returns:
        Formatted message
    """
    from config.ai_personas import get_role_display_name, get_style_display_name

    role_display = get_role_display_name(role)
    style_display = get_style_display_name(style)

    # Add decorative line at top
    header = f"╭─────────────────────────╮\n"
    header += f"│  {role_display}  │\n"
    header += f"╰─────────────────────────╯\n\n"

    # Main answer
    formatted_answer = header + answer

    # Add footer with metadata
    footer = "\n\n"
    footer += "─" * 30 + "\n"

    if source_doc:
        footer += f"📎 <i>Source: {source_doc[:40]}{'...' if len(source_doc) > 40 else ''}</i>\n"

    footer += f"⚙️ <i>Style: {style_display}</i>\n"

    if processing_time > 0:
        footer += f"⏱️ <i>Processed in {processing_time:.1f} sec</i>\n"

    footer += "\n💡 <i>Ask a follow-up question or use buttons below</i>"

    return formatted_answer + footer


def format_settings_overview(user_settings: Dict[str, Any]) -> str:
    """
    Formats user settings overview.

    Args:
        user_settings: Dictionary with user settings

    Returns:
        Beautifully formatted settings overview
    """
    from config.ai_personas import (
        get_role_display_name,
        get_style_display_name,
        get_mode_display_name,
        LANGUAGES
    )

    role = user_settings.get('ai_role', 'assistant')
    style = user_settings.get('response_style', 'standard')
    mode = user_settings.get('ai_mode', 'standard')
    lang = user_settings.get('language', 'ru')

    lang_info = LANGUAGES.get(lang, LANGUAGES['ru'])

    return f"""
⚙️ <b>Your Settings</b>

<b>AI Configuration:</b>
🎭 Role: {get_role_display_name(role)}
📝 Response Style: {get_style_display_name(style)}
⚡ Work Mode: {get_mode_display_name(mode)}

<b>Interface:</b>
🌐 Language: {lang_info['flag']} {lang_info['name']}
🔔 Notifications: {'✅ On' if user_settings.get('notifications', True) else '❌ Off'}

<b>Premium:</b>
{'💎 Premium subscription active' if user_settings.get('is_premium') else '✨ Premium not active'}

📌 <i>Click on section below to change settings</i>
"""


def format_role_selection() -> str:
    """Formats AI role selection menu"""
    return """
🎭 <b>Select AI Assistant Role</b>

Role determines the style and approach to responses:

📊 <b>Business Analyst</b> - focus on numbers and metrics
💼 <b>Business Consultant</b> - strategic recommendations
👨‍🏫 <b>Teacher</b> - simple explanations
🔬 <b>Researcher</b> - deep detailed analysis
🎨 <b>Creative</b> - unconventional approach
🤖 <b>Universal</b> - balanced (default)
⚖️ <b>Lawyer</b> - legal aspects

💡 <i>Choose the role that best fits your task</i>
"""


def format_style_selection() -> str:
    """Formats response style selection menu"""
    return """
📝 <b>Select Response Style</b>

Style determines format and volume of responses:

⚡ <b>Brief</b> - only key facts (2-3 sentences)
📝 <b>Standard</b> - balanced response (default)
📚 <b>Detailed</b> - detailed answer with all nuances
📋 <b>List</b> - structured bullet points
⚖️ <b>Pros/Cons</b> - analysis of advantages and disadvantages
👶 <b>Simple Terms</b> - explain like to a child
💎 <b>Professional</b> - business style for reports

💡 <i>You can change style anytime</i>
"""


def format_processing_status(
    status: str,
    progress: int = 0,
    doc_name: str = None,
    step: str = None
) -> str:
    """
    Formats processing status with progress bar.

    Args:
        status: Status ('processing', 'analyzing', 'done', 'error')
        progress: Progress from 0 to 100
        doc_name: Document name
        step: Current processing step

    Returns:
        Formatted status message
    """
    status_icons = {
        'uploading': '📤',
        'processing': '⚙️',
        'analyzing': '🤖',
        'done': '✅',
        'error': '❌'
    }

    status_texts = {
        'uploading': 'Uploading document...',
        'processing': 'Processing document...',
        'analyzing': 'AI content analysis...',
        'done': 'Ready!',
        'error': 'Processing error'
    }

    icon = status_icons.get(status, '⏳')
    text = status_texts.get(status, 'Processing...')

    # Create progress bar
    bar_length = 20
    filled = int((progress / 100) * bar_length)
    bar = '█' * filled + '░' * (bar_length - filled)

    message = f"{icon} <b>{text}</b>\n\n"

    if doc_name:
        message += f"📄 {doc_name}\n\n"

    if progress > 0 and progress < 100:
        message += f"[{bar}] {progress}%\n\n"

    if step:
        message += f"<i>{step}</i>\n"

    if status == 'done':
        message += "\n✨ <i>Document ready to use!</i>"
    elif status == 'error':
        message += "\n⚠️ <i>Try uploading document again</i>"

    return message


def format_quick_help(context: str = 'general') -> str:
    """
    Formats contextual hint.

    Args:
        context: Context ('general', 'document', 'question', 'settings')

    Returns:
        Hint for user
    """
    helps = {
        'general': """
💡 <b>Quick Tips</b>

<b>Quick Commands:</b>
/start - Main menu
/stats - Your statistics
/mydocs - Document list
/help - Full help

<b>Or simply:</b>
📤 Send file for analysis
💬 Ask question about active document
🔗 Send URL for parsing
""",

        'document': """
💡 <b>Working with Document</b>

<b>You can:</b>
💬 Ask question - just write in chat
📊 Visualize - create charts (for Excel)
📥 Export - get PDF report
📋 Get summary
🔍 Extract keywords

<b>Example questions:</b>
"What are the main conclusions?"
"How many total records in table?"
"List key risks"
""",

        'question': """
💡 <b>How to Ask Questions</b>

<b>Tips for best results:</b>
✅ Be specific in questions
✅ You can ask to clarify answer
✅ Ask about specific sections
✅ Request examples

<b>Bad:</b> "What's here?"
<b>Good:</b> "What's the Q3 sales trend?"
""",

        'settings': """
💡 <b>AI Settings</b>

<b>Role</b> - determines approach to responses
(analyst, consultant, teacher)

<b>Style</b> - determines response format
(brief, detailed, list)

<b>Mode</b> - affects speed and quality
(fast, standard, advanced)

💡 Experiment with settings!
"""
    }

    return helps.get(context, helps['general'])


def format_document_card(doc: Dict[str, Any], is_active: bool = False) -> str:
    """
    Formats document card for list.

    Args:
        doc: Document data
        is_active: Is document active

    Returns:
        Formatted card
    """
    type_icons = {
        'pdf': '📄',
        'excel': '📊',
        'word': '📝',
        'url': '🌐',
        'audio': '🎤'
    }

    icon = type_icons.get(doc.get('type_raw', ''), '📎')
    active_mark = " ✅ <b>ACTIVE</b>" if is_active else ""

    name = doc.get('name', 'Untitled')
    if len(name) > 35:
        name = name[:32] + "..."

    size = doc.get('size', 'N/A')
    date = doc.get('created_at', 'N/A')
    words = doc.get('word_count', 0)

    card = f"{icon} <code>{name}</code>{active_mark}\n"
    card += f"    📏 {size} · 📝 {words:,} words · 📅 {date}\n"

    return card


def format_error_message(error_type: str, details: str = None) -> str:
    """
    Formats error message with helpful tips.

    Args:
        error_type: Error type
        details: Error details

    Returns:
        Beautifully formatted error message
    """
    error_messages = {
        'file_too_large': {
            'icon': '📦',
            'title': 'File too large',
            'message': 'Telegram limits file size to 20 MB.',
            'solution': '💡 Try compressing file or splitting into parts'
        },
        'unsupported_format': {
            'icon': '📎',
            'title': 'Unsupported format',
            'message': 'This file format is not yet supported.',
            'solution': '💡 Supported: PDF, Excel, Word, Audio'
        },
        'processing_failed': {
            'icon': '⚠️',
            'title': 'Processing error',
            'message': 'Failed to process document.',
            'solution': '💡 Try uploading file again'
        },
        'no_active_document': {
            'icon': '📄',
            'title': 'No active document',
            'message': 'To ask question, first upload document.',
            'solution': '💡 Send file or select from list'
        },
        'api_error': {
            'icon': '🔌',
            'title': 'API Error',
            'message': 'Problem connecting to AI service.',
            'solution': '💡 Try again in few seconds'
        },
    }

    error_info = error_messages.get(error_type, {
        'icon': '❌',
        'title': 'An error occurred',
        'message': details or 'Unknown error',
        'solution': '💡 Contact support if problem persists'
    })

    message = f"{error_info['icon']} <b>{error_info['title']}</b>\n\n"
    message += f"{error_info['message']}\n\n"
    message += f"{error_info['solution']}"

    if details:
        message += f"\n\n<i>Details: {details[:100]}</i>"

    return message


def format_success_message(action: str, details: str = None) -> str:
    """
    Formats success message.

    Args:
        action: Action type
        details: Additional information

    Returns:
        Beautifully formatted message
    """
    success_messages = {
        'document_uploaded': {
            'icon': '✅',
            'title': 'Document uploaded successfully!',
            'next': 'Ask questions or use document menu'
        },
        'settings_saved': {
            'icon': '💾',
            'title': 'Settings saved!',
            'next': 'New settings will apply to next responses'
        },
        'export_ready': {
            'icon': '📥',
            'title': 'Export ready!',
            'next': 'Check file above in chat'
        },
        'document_deleted': {
            'icon': '🗑️',
            'title': 'Document deleted',
            'next': 'You can upload new document'
        },
    }

    success_info = success_messages.get(action, {
        'icon': '✅',
        'title': 'Done!',
        'next': details or ''
    })

    message = f"{success_info['icon']} <b>{success_info['title']}</b>\n\n"

    if success_info['next']:
        message += f"➡️ {success_info['next']}"

    if details and action not in success_messages:
        message += f"\n\n{details}"

    return message
