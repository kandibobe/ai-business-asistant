"""
Analytics API routes
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta

from api.dependencies import get_db, get_current_user
from database import models

router = APIRouter()


@router.get("/stats")
async def get_user_stats(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get comprehensive user statistics
    """
    # Total documents
    total_documents = db.query(models.Document).filter(
        models.Document.user_id == current_user.id
    ).count()

    # Total questions
    total_questions = db.query(models.Question).filter(
        models.Question.user_id == current_user.id
    ).count()

    # Average response time
    avg_response_time = db.query(
        func.avg(models.Question.response_time)
    ).filter(
        models.Question.user_id == current_user.id,
        models.Question.response_time.isnot(None)
    ).scalar() or 0

    # Documents by type
    docs_by_type = db.query(
        models.Document.document_type,
        func.count(models.Document.id)
    ).filter(
        models.Document.user_id == current_user.id
    ).group_by(
        models.Document.document_type
    ).all()

    documents_by_type = {doc_type: count for doc_type, count in docs_by_type}

    # Active document
    active_document = db.query(models.Document).filter(
        models.Document.user_id == current_user.id,
        models.Document.is_active == True
    ).first()

    return {
        "total_documents": total_documents,
        "total_questions": total_questions,
        "average_response_time": round(avg_response_time, 2) if avg_response_time else 0,
        "documents_by_type": documents_by_type,
        "active_document": {
            "id": active_document.id,
            "file_name": active_document.file_name,
            "document_type": active_document.document_type
        } if active_document else None,
        "user_since": current_user.created_at.isoformat() if current_user.created_at else None
    }


@router.get("/dashboard")
async def get_dashboard_stats(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get dashboard statistics (today's activity)
    """
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    # Today's documents
    documents_today = db.query(models.Document).filter(
        models.Document.user_id == current_user.id,
        models.Document.uploaded_at >= today_start
    ).count()

    # Today's questions
    questions_today = db.query(models.Question).filter(
        models.Question.user_id == current_user.id,
        models.Question.created_at >= today_start
    ).count()

    # Total documents
    total_documents = db.query(models.Document).filter(
        models.Document.user_id == current_user.id
    ).count()

    # Total questions
    total_questions = db.query(models.Question).filter(
        models.Question.user_id == current_user.id
    ).count()

    # Recent questions (last 7 days by day)
    week_ago = datetime.now() - timedelta(days=7)
    questions_by_day = db.query(
        func.date(models.Question.created_at).label('date'),
        func.count(models.Question.id).label('count')
    ).filter(
        models.Question.user_id == current_user.id,
        models.Question.created_at >= week_ago
    ).group_by(
        func.date(models.Question.created_at)
    ).all()

    activity_chart = [
        {
            "date": date.isoformat(),
            "questions": count
        }
        for date, count in questions_by_day
    ]

    # Recent documents
    recent_documents = db.query(models.Document).filter(
        models.Document.user_id == current_user.id
    ).order_by(
        models.Document.uploaded_at.desc()
    ).limit(5).all()

    return {
        "documents_today": documents_today,
        "questions_today": questions_today,
        "total_documents": total_documents,
        "total_questions": total_questions,
        "activity_chart": activity_chart,
        "recent_documents": [
            {
                "id": doc.id,
                "file_name": doc.file_name,
                "document_type": doc.document_type,
                "uploaded_at": doc.uploaded_at.isoformat() if doc.uploaded_at else None,
                "is_active": doc.is_active
            }
            for doc in recent_documents
        ],
        "is_premium": current_user.is_premium or False
    }


@router.get("/documents/{document_id}/stats")
async def get_document_stats(
    document_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get statistics for a specific document
    """
    # Get document
    document = db.query(models.Document).filter(
        models.Document.id == document_id,
        models.Document.user_id == current_user.id
    ).first()

    if not document:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )

    # Questions about this document
    total_questions = db.query(models.Question).filter(
        models.Question.document_id == document_id,
        models.Question.user_id == current_user.id
    ).count()

    # Average response time for this document
    avg_response_time = db.query(
        func.avg(models.Question.response_time)
    ).filter(
        models.Question.document_id == document_id,
        models.Question.user_id == current_user.id,
        models.Question.response_time.isnot(None)
    ).scalar() or 0

    # Recent questions
    recent_questions = db.query(models.Question).filter(
        models.Question.document_id == document_id,
        models.Question.user_id == current_user.id
    ).order_by(
        models.Question.created_at.desc()
    ).limit(10).all()

    return {
        "document": {
            "id": document.id,
            "file_name": document.file_name,
            "document_type": document.document_type,
            "file_size": document.file_size,
            "uploaded_at": document.uploaded_at.isoformat() if document.uploaded_at else None,
            "processed_at": document.processed_at.isoformat() if document.processed_at else None,
            "status": document.status
        },
        "total_questions": total_questions,
        "average_response_time": round(avg_response_time, 2) if avg_response_time else 0,
        "recent_questions": [
            {
                "question": q.question_text,
                "answer": q.answer_text[:200] + "..." if q.answer_text and len(q.answer_text) > 200 else q.answer_text,
                "created_at": q.created_at.isoformat() if q.created_at else None,
                "response_time": q.response_time
            }
            for q in recent_questions
        ]
    }
