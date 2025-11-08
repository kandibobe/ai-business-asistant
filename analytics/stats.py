"""
Модуль статистики и аналитики для AI Business Intelligence Agent.
Tracking пользовательской активности для демонстрации на Fiverr.
"""
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timedelta
from typing import Dict, Any, List
from database import models

def get_user_stats(db: Session, user_id: int) -> Dict[str, Any]:
    """
    Получить статистику пользователя.

    Args:
        db: SQLAlchemy session
        user_id: ID пользователя

    Returns:
        Словарь со статистикой
    """
    user = db.query(models.User).filter(models.User.user_id == user_id).first()

    if not user:
        return {}

    # Подсчет документов по типам (теперь используем document_type поле!)
    documents = db.query(models.Document).filter(models.Document.user_id == user.id).all()

    # Общая статистика
    total_docs = len(documents)

    # Подсчет по типам - используем поле document_type
    pdf_count = sum(1 for doc in documents if doc.document_type == 'pdf')
    excel_count = sum(1 for doc in documents if doc.document_type == 'excel')
    word_count = sum(1 for doc in documents if doc.document_type == 'word')
    url_count = sum(1 for doc in documents if doc.document_type == 'url')
    audio_count = sum(1 for doc in documents if doc.document_type == 'audio')

    # Дополнительная статистика
    total_words = sum(doc.word_count or 0 for doc in documents)
    total_chars = sum(doc.char_count or 0 for doc in documents)
    total_size = sum(doc.file_size or 0 for doc in documents)

    # Документы за текущий месяц
    month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    docs_this_month = sum(1 for doc in documents if doc.created_at >= month_start)

    # Активный документ
    active_doc = None
    if user.active_document_id:
        active_doc_obj = db.query(models.Document).filter(
            models.Document.id == user.active_document_id
        ).first()
        active_doc = active_doc_obj.file_name if active_doc_obj else None

    # Расчет streak (дней подряд с активностью)
    # Упрощенная версия - можно улучшить с отдельной таблицей activity
    streak_days = calculate_streak(user.created_at)

    # Форматируем размер
    size_mb = total_size / (1024 * 1024) if total_size > 0 else 0

    return {
        'total_docs': total_docs,
        'active_doc': active_doc or 'Нет',
        'docs_this_month': docs_this_month,
        'questions_asked': 0,  # TODO: добавить tracking вопросов
        'avg_response_time': 'N/A',  # TODO: добавить tracking времени ответа
        'accuracy': 95,  # Демо значение
        'pdf_count': pdf_count,
        'excel_count': excel_count,
        'word_count': word_count,
        'url_count': url_count,
        'audio_count': audio_count,
        'first_visit': user.created_at.strftime('%d.%m.%Y'),
        'last_activity': datetime.now().strftime('%d.%m.%Y %H:%M'),
        'streak_days': streak_days,
        'is_premium': False,  # TODO: добавить premium tracking
        # Новая статистика
        'total_words': total_words,
        'total_chars': total_chars,
        'total_size_mb': round(size_mb, 2),
        'avg_doc_words': round(total_words / total_docs, 0) if total_docs > 0 else 0,
    }

def calculate_streak(created_at: datetime) -> int:
    """
    Рассчитать количество дней активности подряд.
    Упрощенная версия для демо.
    """
    days_since_registration = (datetime.now() - created_at).days
    # Для демо возвращаем случайное значение от 1 до дней с регистрации
    return min(days_since_registration, 30)  # Макс 30 для демо

def get_document_stats(db: Session, doc_id: int) -> Dict[str, Any]:
    """
    Получить статистику по конкретному документу.

    Args:
        db: SQLAlchemy session
        doc_id: ID документа

    Returns:
        Словарь со статистикой документа
    """
    doc = db.query(models.Document).filter(models.Document.id == doc_id).first()

    if not doc:
        return {}

    # Маппинг типов документов для отображения
    type_display = {
        'pdf': '📄 PDF',
        'excel': '📊 Excel',
        'word': '📝 Word',
        'url': '🌐 URL',
        'audio': '🎤 Audio',
        'unknown': '📎 Unknown'
    }

    doc_type_display = type_display.get(doc.document_type, '📎 Unknown')

    # Форматируем размер файла
    size_display = 'N/A'
    if doc.file_size:
        if doc.file_size < 1024:
            size_display = f"{doc.file_size} B"
        elif doc.file_size < 1024 * 1024:
            size_display = f"{doc.file_size / 1024:.1f} KB"
        else:
            size_display = f"{doc.file_size / (1024 * 1024):.1f} MB"

    return {
        'id': doc.id,
        'name': doc.file_name,
        'type': doc_type_display,
        'type_raw': doc.document_type,
        'size': size_display,
        'file_size_bytes': doc.file_size or 0,
        'word_count': doc.word_count or 0,
        'char_count': doc.char_count or (len(doc.content) if doc.content else 0),
        'created_at': doc.created_at.strftime('%d.%m.%Y %H:%M'),
        'uploaded_at': doc.uploaded_at.strftime('%d.%m.%Y %H:%M') if doc.uploaded_at else 'N/A',
        'processed_at': doc.processed_at.strftime('%d.%m.%Y %H:%M') if doc.processed_at else 'Не обработан',
        'processed': doc.processed_at is not None,
        'language': doc.language_detected or 'Не определен',
        'summary': doc.summary or 'Нет краткого содержания',
        'keywords': doc.keywords or 'Не извлечены',
        'source_url': doc.source_url,
        'questions_count': 0,  # TODO: добавить tracking вопросов
        'rating': 0,  # TODO: добавить рейтинговую систему
    }

def get_global_stats(db: Session) -> Dict[str, Any]:
    """
    Получить глобальную статистику (для админа или демо).

    Args:
        db: SQLAlchemy session

    Returns:
        Глобальная статистика платформы
    """
    total_users = db.query(func.count(models.User.id)).scalar()
    total_documents = db.query(func.count(models.Document.id)).scalar()

    # Пользователи за последние 7 дней
    week_ago = datetime.now() - timedelta(days=7)
    active_users_week = db.query(func.count(models.User.id)).filter(
        models.User.created_at >= week_ago
    ).scalar()

    # Документы за последние 24 часа
    day_ago = datetime.now() - timedelta(days=1)
    docs_today = db.query(func.count(models.Document.id)).filter(
        models.Document.created_at >= day_ago
    ).scalar()

    return {
        'total_users': total_users,
        'total_documents': total_documents,
        'active_users_week': active_users_week,
        'docs_today': docs_today,
        'avg_docs_per_user': round(total_documents / total_users, 2) if total_users > 0 else 0,
    }

def get_top_users(db: Session, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Получить топ пользователей по количеству документов.

    Args:
        db: SQLAlchemy session
        limit: Количество пользователей

    Returns:
        Список топ пользователей
    """
    top_users = db.query(
        models.User,
        func.count(models.Document.id).label('doc_count')
    ).join(
        models.Document, models.User.id == models.Document.user_id
    ).group_by(
        models.User.id
    ).order_by(
        desc('doc_count')
    ).limit(limit).all()

    return [
        {
            'user_id': user.user_id,
            'username': user.username or 'Anonymous',
            'first_name': user.first_name,
            'doc_count': doc_count,
        }
        for user, doc_count in top_users
    ]

def track_question(db: Session, user_id: int, doc_id: int, question: str, answer: str, response_time: float):
    """
    Трекинг вопросов пользователя (для будущей реализации).

    Args:
        db: SQLAlchemy session
        user_id: ID пользователя
        doc_id: ID документа
        question: Текст вопроса
        answer: Текст ответа
        response_time: Время ответа в секундах
    """
    # TODO: Создать таблицу Question в моделях и реализовать сохранение
    pass

def generate_usage_report(db: Session, user_id: int, period_days: int = 30) -> str:
    """
    Генерировать отчет об использовании за период.

    Args:
        db: SQLAlchemy session
        user_id: ID пользователя
        period_days: Период в днях

    Returns:
        Форматированный текстовый отчет
    """
    user = db.query(models.User).filter(models.User.user_id == user_id).first()

    if not user:
        return "Пользователь не найден"

    start_date = datetime.now() - timedelta(days=period_days)

    documents = db.query(models.Document).filter(
        models.Document.user_id == user.id,
        models.Document.created_at >= start_date
    ).all()

    report = f"""
📊 ОТЧЕТ ОБ ИСПОЛЬЗОВАНИИ
За период: {period_days} дней

👤 Пользователь: {user.first_name or 'N/A'} ({user.username or 'N/A'})

📄 Документы:
   • Всего загружено: {len(documents)}
   • Средняя длина: {sum(len(d.content or '') for d in documents) // len(documents) if documents else 0} символов

📈 Активность:
   • Дней с документами: {len(set(d.created_at.date() for d in documents))}
   • Средне в день: {len(documents) / period_days:.2f}

💡 Рекомендации:
   {'✅ Отличная активность! Продолжайте в том же духе!' if len(documents) > 10 else '📈 Загружайте больше документов для лучшего анализа!'}
"""

    return report
