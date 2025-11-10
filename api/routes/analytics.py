"""
Analytics routes.
User statistics, document analytics.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.dependencies import get_db, get_current_user
from utils.validators import UserStats, DocumentStats
from database import crud
from database.models import User

router = APIRouter()


@router.get("/stats", response_model=UserStats)
async def get_user_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user statistics.

    Returns total documents, questions, response time, etc.
    """
    documents = crud.get_user_documents(db, current_user)

    # Calculate stats
    total_documents = len(documents)
    documents_by_type = {}

    for doc in documents:
        doc_type = doc.document_type or 'unknown'
        documents_by_type[doc_type] = documents_by_type.get(doc_type, 0) + 1

    return {
        "total_documents": total_documents,
        "total_questions": 0,  # TODO: Implement question tracking
        "avg_response_time_ms": None,  # TODO: Implement response time tracking
        "total_sessions": 0,  # TODO: Implement session tracking
        "documents_by_type": documents_by_type,
        "recent_activity": []  # TODO: Implement activity tracking
    }


@router.get("/documents/{document_id}", response_model=DocumentStats)
async def get_document_stats(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get statistics for a specific document.

    Returns questions asked, response times, etc.
    """
    document = crud.get_document_by_id(db, document_id)

    if not document or document.user_id != current_user.id:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )

    return {
        "document_id": document_id,
        "total_questions": 0,  # TODO: Implement question tracking
        "avg_response_time_ms": None,
        "question_history": []
    }
