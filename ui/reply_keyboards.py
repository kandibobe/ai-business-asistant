"""
Постоянные клавиатуры (ReplyKeyboard) для быстрого доступа.
Отображаются внизу экрана Telegram.
"""
from telegram import ReplyKeyboardMarkup, KeyboardButton
from config.i18n import get_text

def get_main_reply_keyboard(lang: str = 'ru') -> ReplyKeyboardMarkup:
    """
    Главная постоянная клавиатура с быстрым доступом.

    Args:
        lang: Код языка (ru, en, de)

    Returns:
        ReplyKeyboardMarkup с кнопками быстрого доступа
    """
    keyboard = [
        [
            KeyboardButton(get_text('quick_upload', lang)),
            KeyboardButton(get_text('quick_docs', lang)),
        ],
        [
            KeyboardButton(get_text('quick_chat', lang)),
            KeyboardButton(get_text('quick_tools', lang)),
        ],
        [
            KeyboardButton(get_text('btn_settings', lang)),
            KeyboardButton(get_text('btn_help', lang)),
        ],
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,  # Адаптивный размер кнопок
        one_time_keyboard=False,  # Клавиатура остается после нажатия
        input_field_placeholder=get_text('quick_placeholder', lang) if get_text('quick_placeholder', lang) != '[quick_placeholder]' else None
    )

def get_minimal_reply_keyboard(lang: str = 'ru') -> ReplyKeyboardMarkup:
    """
    Минимальная клавиатура с основными действиями.

    Args:
        lang: Код языка

    Returns:
        ReplyKeyboardMarkup с минимальным набором кнопок
    """
    keyboard = [
        [
            KeyboardButton(get_text('quick_docs', lang)),
            KeyboardButton(get_text('quick_chat', lang)),
        ],
        [
            KeyboardButton(get_text('btn_main_menu', lang)),
        ],
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )

def remove_reply_keyboard():
    """Удаляет постоянную клавиатуру"""
    from telegram import ReplyKeyboardRemove
    return ReplyKeyboardRemove()
