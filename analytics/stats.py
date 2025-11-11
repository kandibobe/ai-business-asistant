"""
Statistics and analytics module for AI Business Intelligence Agent.
User activity tracking for Fiverr demonstration.
"""
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timedelta
from typing import Dict, Any, List
from database import models

def get_user_stats(db: Session, user_id: int) -> Dict[str, Any]:
    """
    Get user statistics.

    Args:
        db: SQLAlchemy session
        user_id: User ID

    Returns:
        Dictionary with statistics
    """
    user = db.query(models.User).filter(models.User.user_id == user_id).first()

    if not user:
        return {}

    # Count documents by type (now using document_type field!)
    documents = db.query(models.Document).filter(models.Document.user_id == user.id).all()

    # General statistics
    total_docs = len(documents)

    # Count by type - using document_type field
    pdf_count = sum(1 for doc in documents if doc.document_type == 'pdf')
    excel_count = sum(1 for doc in documents if doc.document_type == 'excel')
    word_count = sum(1 for doc in documents if doc.document_type == 'word')
    url_count = sum(1 for doc in documents if doc.document_type == 'url')
    audio_count = sum(1 for doc in documents if doc.document_type == 'audio')

    # Additional statistics
    total_words = sum(doc.word_count or 0 for doc in documents)
    total_chars = sum(doc.char_count or 0 for doc in documents)
    total_size = sum(doc.file_size or 0 for doc in documents)

    # Documents this month
    month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    docs_this_month = sum(
        1 for doc in documents
        if (hasattr(doc, 'created_at') and doc.created_at and doc.created_at >= month_start) or
           (hasattr(doc, 'uploaded_at') and doc.uploaded_at and doc.uploaded_at >= month_start)
    )

    # Active document
    active_doc = None
    if user.active_document_id:
        active_doc_obj = db.query(models.Document).filter(
            models.Document.id == user.active_document_id
        ).first()
        active_doc = active_doc_obj.file_name if active_doc_obj else None

    # Calculate streak (consecutive days with activity)
    # Simplified version - can be improved with separate activity table
    streak_days = calculate_streak(user.created_at)

    # Format size
    size_mb = total_size / (1024 * 1024) if total_size > 0 else 0

    return {
        'total_docs': total_docs,
        'active_doc': active_doc or 'None',
        'docs_this_month': docs_this_month,
        'questions_asked': 0,  # TODO: add question tracking
        'avg_response_time': 'N/A',  # TODO: add response time tracking
        'accuracy': 95,  # Demo value
        'pdf_count': pdf_count,
        'excel_count': excel_count,
        'word_count': word_count,
        'url_count': url_count,
        'audio_count': audio_count,
        'first_visit': user.created_at.strftime('%d.%m.%Y'),
        'last_activity': datetime.now().strftime('%d.%m.%Y %H:%M'),
        'streak_days': streak_days,
        'is_premium': False,  # TODO: add premium tracking
        # New statistics
        'total_words': total_words,
        'total_chars': total_chars,
        'total_size_mb': round(size_mb, 2),
        'avg_doc_words': round(total_words / total_docs, 0) if total_docs > 0 else 0,
    }

def calculate_streak(created_at: datetime) -> int:
    """
    Calculate consecutive days of activity.
    Simplified version for demo.
    """
    days_since_registration = (datetime.now() - created_at).days
    # For demo return a value from 1 to days since registration
    return min(days_since_registration, 30)  # Max 30 for demo

def get_document_stats(db: Session, doc_id: int) -> Dict[str, Any]:
    """
    Get statistics for specific document.

    Args:
        db: SQLAlchemy session
        doc_id: Document ID

    Returns:
        Dictionary with document statistics
    """
    doc = db.query(models.Document).filter(models.Document.id == doc_id).first()

    if not doc:
        return {}

    # Document type display mapping
    type_display = {
        'pdf': '📄 PDF',
        'excel': '📊 Excel',
        'word': '📝 Word',
        'url': '🌐 URL',
        'audio': '🎤 Audio',
        'unknown': '📎 Unknown'
    }

    doc_type_display = type_display.get(doc.document_type, '📎 Unknown')

    # Format file size
    size_display = 'N/A'
    if doc.file_size:
        if doc.file_size < 1024:
            size_display = f"{doc.file_size} B"
        elif doc.file_size < 1024 * 1024:
            size_display = f"{doc.file_size / 1024:.1f} KB"
        else:
            size_display = f"{doc.file_size / (1024 * 1024):.1f} MB"

    # Safely format created_at
    created_at_str = 'N/A'
    if hasattr(doc, 'created_at') and doc.created_at:
        created_at_str = doc.created_at.strftime('%d.%m.%Y %H:%M')
    elif hasattr(doc, 'uploaded_at') and doc.uploaded_at:
        created_at_str = doc.uploaded_at.strftime('%d.%m.%Y %H:%M')

    return {
        'id': doc.id,
        'name': doc.file_name,
        'type': doc_type_display,
        'type_raw': doc.document_type,
        'size': size_display,
        'file_size_bytes': doc.file_size or 0,
        'word_count': doc.word_count or 0,
        'char_count': doc.char_count or (len(doc.content) if doc.content else 0),
        'created_at': created_at_str,
        'uploaded_at': doc.uploaded_at.strftime('%d.%m.%Y %H:%M') if doc.uploaded_at else 'N/A',
        'processed_at': doc.processed_at.strftime('%d.%m.%Y %H:%M') if doc.processed_at else 'Not processed',
        'processed': doc.processed_at is not None,
        'language': doc.language_detected or 'Not detected',
        'summary': doc.summary or 'No summary available',
        'keywords': doc.keywords or 'Not extracted',
        'source_url': doc.source_url,
        'questions_count': 0,  # TODO: add question tracking
        'rating': 0,  # TODO: add rating system
    }

def get_global_stats(db: Session) -> Dict[str, Any]:
    """
    Get global statistics (for admin or demo).

    Args:
        db: SQLAlchemy session

    Returns:
        Global platform statistics
    """
    total_users = db.query(func.count(models.User.id)).scalar()
    total_documents = db.query(func.count(models.Document.id)).scalar()

    # Users in last 7 days
    week_ago = datetime.now() - timedelta(days=7)
    active_users_week = db.query(func.count(models.User.id)).filter(
        models.User.created_at >= week_ago
    ).scalar()

    # Documents in last 24 hours
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
    Get top users by document count.

    Args:
        db: SQLAlchemy session
        limit: Number of users

    Returns:
        List of top users
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
    Track user questions (for future implementation).

    Args:
        db: SQLAlchemy session
        user_id: User ID
        doc_id: Document ID
        question: Question text
        answer: Answer text
        response_time: Response time in seconds
    """
    # TODO: Create Question table in models and implement saving
    pass

def generate_usage_report(db: Session, user_id: int, period_days: int = 30) -> str:
    """
    Generate usage report for period.

    Args:
        db: SQLAlchemy session
        user_id: User ID
        period_days: Period in days

    Returns:
        Formatted text report
    """
    user = db.query(models.User).filter(models.User.user_id == user_id).first()

    if not user:
        return "User not found"

    start_date = datetime.now() - timedelta(days=period_days)

    documents = db.query(models.Document).filter(
        models.Document.user_id == user.id,
        models.Document.created_at >= start_date
    ).all()

    report = f"""
📊 USAGE REPORT
Period: {period_days} days

👤 User: {user.first_name or 'N/A'} ({user.username or 'N/A'})

📄 Documents:
   • Total uploaded: {len(documents)}
   • Average length: {sum(len(d.content or '') for d in documents) // len(documents) if documents else 0} characters

📈 Activity:
   • Days with documents: {len(set(d.created_at.date() for d in documents))}
   • Average per day: {len(documents) / period_days:.2f}

💡 Recommendations:
   {'✅ Excellent activity! Keep it up!' if len(documents) > 10 else '📈 Upload more documents for better analysis!'}
"""

    return report
