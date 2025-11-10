"""
Configuration package for AI Business Intelligence Agent.
"""

# Gemini model configuration
# Upgraded to Gemini 1.5 Pro for:
# - 1 million token context window (vs 32K in old gemini-pro)
# - Native multimodality (images, video)
# - Better performance and accuracy
# - More cost-effective with gemini-1.5-flash option
GEMINI_MODEL_NAME = 'gemini-1.5-pro-002'  # Latest Gemini 1.5 Pro
GEMINI_FLASH_MODEL = 'gemini-1.5-flash-002'  # Faster, cheaper alternative

# Model selection based on use case
# Use GEMINI_MODEL_NAME for complex analysis
# Use GEMINI_FLASH_MODEL for simple/fast responses
DEFAULT_MODEL = GEMINI_MODEL_NAME

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
    'GEMINI_FLASH_MODEL',
    'DEFAULT_MODEL',
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
