"""
Configuration package for AI Business Intelligence Agent.
"""

# Gemini model configuration
GEMINI_MODEL_NAME = 'gemini-pro-latest'

# Import from this package
from .i18n import get_text, get_language_name, get_available_languages, LANGUAGES, TRANSLATIONS
from .ai_personas import (
    AI_ROLES,
    RESPONSE_STYLES,
    AI_MODES,
    build_ai_prompt,
    get_role_display_name,
    get_style_display_name,
    get_mode_display_name,
)

__all__ = [
    'GEMINI_MODEL_NAME',
    'get_text',
    'get_language_name',
    'get_available_languages',
    'LANGUAGES',
    'TRANSLATIONS',
    'AI_ROLES',
    'RESPONSE_STYLES',
    'AI_MODES',
    'build_ai_prompt',
    'get_role_display_name',
    'get_style_display_name',
    'get_mode_display_name',
]
