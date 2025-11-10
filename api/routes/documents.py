"""
Documents API routes
"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import Optional
import os
import shutil
from datetime import datetime

from api.dependencies import get_db, get_current_user, document_to_dict
from api.models.documents import (
    DocumentResponse,
    DocumentListResponse,
    UploadResponse,
    DeleteResponse,
    ActivateResponse
)
from database import models
from utils.file_validators import validate_file_upload

router = APIRouter()


@router.get("", response_model=DocumentListResponse)
async def get_documents(
    page: int = 1,
    page_size: int = 20,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get list of user's documents with pagination

    - **page**: Page number (default: 1)
    - **page_size**: Number of items per page (default: 20, max: 100)
    """
    # Validate pagination
    if page < 1:
        page = 1
    if page_size < 1 or page_size > 100:
        page_size = 20

    skip = (page - 1) * page_size

    # Get total count
    total = db.query(models.Document).filter(
        models.Document.user_id == current_user.id
    ).count()

    # Get documents
    documents = db.query(models.Document).filter(
        models.Document.user_id == current_user.id
    ).order_by(
        models.Document.uploaded_at.desc()
    ).offset(skip).limit(page_size).all()

    return DocumentListResponse(
        documents=[DocumentResponse(**document_to_dict(doc)) for doc in documents],
        total=total,
        page=page,
        page_size=page_size
    )


@router.post("/upload", response_model=UploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload a new document for processing

    Supported formats: PDF, Excel, Word, Audio (MP3, WAV), Text
    Max file size: 50MB
    """
    # Validate file
    validation_result = validate_file_upload(file)
    if not validation_result["valid"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=validation_result["error"]
        )

    # Create uploads directory if not exists
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)

    # Generate unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{current_user.user_id}_{timestamp}{file_extension}"
    file_path = os.path.join(upload_dir, unique_filename)

    # Save file
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save file: {str(e)}"
        )

    # Get file size
    file_size = os.path.getsize(file_path)

    # Create document record
    new_document = models.Document(
        user_id=current_user.id,
        file_name=file.filename,
        file_path=file_path,
        document_type=validation_result["file_type"],
        file_size=file_size,
        status="pending",
        is_active=False
    )

    db.add(new_document)
    db.commit()
    db.refresh(new_document)

    # TODO: Trigger async processing with Celery
    # process_document_task.delay(new_document.id, file_path)

    return UploadResponse(
        id=new_document.id,
        file_name=new_document.file_name,
        document_type=new_document.document_type,
        file_size=new_document.file_size,
        status=new_document.status,
        message="Document uploaded successfully. Processing will start shortly."
    )


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get details of a specific document
    """
    document = db.query(models.Document).filter(
        models.Document.id == document_id,
        models.Document.user_id == current_user.id
    ).first()

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )

    return DocumentResponse(**document_to_dict(document))


@router.delete("/{document_id}", response_model=DeleteResponse)
async def delete_document(
    document_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a document
    """
    document = db.query(models.Document).filter(
        models.Document.id == document_id,
        models.Document.user_id == current_user.id
    ).first()

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )

    # Delete file from disk
    if document.file_path and os.path.exists(document.file_path):
        try:
            os.remove(document.file_path)
        except Exception as e:
            print(f"Failed to delete file: {e}")

    # Delete from database
    db.delete(document)
    db.commit()

    return DeleteResponse(
        success=True,
        message="Document deleted successfully"
    )


@router.put("/{document_id}/activate", response_model=ActivateResponse)
async def activate_document(
    document_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Set a document as active for chat context
    """
    document = db.query(models.Document).filter(
        models.Document.id == document_id,
        models.Document.user_id == current_user.id
    ).first()

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )

    # Deactivate all other documents
    db.query(models.Document).filter(
        models.Document.user_id == current_user.id,
        models.Document.id != document_id
    ).update({"is_active": False})

    # Activate this document
    document.is_active = True
    db.commit()

    return ActivateResponse(
        success=True,
        document_id=document.id,
        message=f"Document '{document.file_name}' activated successfully"
    )
