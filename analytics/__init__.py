"""
Analytics модуль для статистики и аналитики.
"""
from .stats import (
    get_user_stats,
    get_document_stats,
    get_global_stats,
    get_top_users,
    track_question,
    generate_usage_report,
    calculate_streak,
)

__all__ = [
    'get_user_stats',
    'get_document_stats',
    'get_global_stats',
    'get_top_users',
    'track_question',
    'generate_usage_report',
    'calculate_streak',
]
