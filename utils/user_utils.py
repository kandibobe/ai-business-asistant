"""
Utility functions for user operations.
Optimized for performance with caching and efficient database access.
"""
from telegram import Update
from telegram.ext import ContextTypes
from sqlalchemy.orm import Session

from database.database import SessionLocal
from database import crud


def get_user_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """
    Get user's preferred language with caching for performance.

    Uses context.user_data cache to avoid repeated database queries.

    Args:
        update: Telegram Update object
        context: Bot context

    Returns:
        Language code (ru, en, de)
    """
    # Check cache first
    if 'user_language' in context.user_data:
        return context.user_data['user_language']

    # Get from database
    user = update.effective_user
    if not user:
        return 'ru'

    db: Session = SessionLocal()
    try:
        db_user = crud.get_or_create_user(
            db, user.id, user.username, user.first_name, user.last_name
        )
        lang = db_user.language or 'ru'

        # Cache for subsequent calls
        context.user_data['user_language'] = lang

        return lang
    finally:
        db.close()


def invalidate_user_cache(context: ContextTypes.DEFAULT_TYPE):
    """
    Invalidate cached user data (call this after language change).

    Args:
        context: Bot context
    """
    context.user_data.pop('user_language', None)


def get_user_with_db(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Get user and database session together for efficient operations.

    Usage:
        with get_user_with_db(update, context) as (db, db_user, lang):
            # Use db, db_user, and lang here
            pass

    Args:
        update: Telegram Update object
        context: Bot context

    Yields:
        Tuple of (db, db_user, language_code)
    """
    from contextlib import contextmanager

    @contextmanager
    def _get_user():
        user = update.effective_user
        db: Session = SessionLocal()
        try:
            db_user = crud.get_or_create_user(
                db, user.id, user.username, user.first_name, user.last_name
            )

            # Get cached language or from db_user
            lang = context.user_data.get('user_language')
            if not lang:
                lang = db_user.language or 'ru'
                context.user_data['user_language'] = lang

            yield db, db_user, lang
        finally:
            db.close()

    return _get_user()
