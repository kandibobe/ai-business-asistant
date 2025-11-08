"""
UI модуль для красивого интерфейса Telegram бота.
"""
from .keyboards import (
    get_main_menu_keyboard,
    get_post_analysis_keyboard,
    get_document_actions_keyboard,
    get_export_format_keyboard,
    get_stats_actions_keyboard,
    get_language_keyboard,
    get_settings_keyboard,
    get_ai_mode_keyboard,
    get_premium_keyboard,
    get_confirm_keyboard,
    get_quick_actions_reply_keyboard,
    get_pagination_keyboard,
)
from .messages import (
    format_welcome_message,
    format_stats_message,
    format_document_info,
    format_document_list,
    format_help_message,
    format_processing_message,
    format_success_message,
    format_error_message,
    format_premium_promo,
    format_comparison_table,
)

__all__ = [
    # Keyboards
    'get_main_menu_keyboard',
    'get_post_analysis_keyboard',
    'get_document_actions_keyboard',
    'get_export_format_keyboard',
    'get_stats_actions_keyboard',
    'get_language_keyboard',
    'get_settings_keyboard',
    'get_ai_mode_keyboard',
    'get_premium_keyboard',
    'get_confirm_keyboard',
    'get_quick_actions_reply_keyboard',
    'get_pagination_keyboard',
    # Messages
    'format_welcome_message',
    'format_stats_message',
    'format_document_info',
    'format_document_list',
    'format_help_message',
    'format_processing_message',
    'format_success_message',
    'format_error_message',
    'format_premium_promo',
    'format_comparison_table',
]
