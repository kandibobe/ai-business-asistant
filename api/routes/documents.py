"""
Documents routes.
Upload, list, view, delete documents.
"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import os

from api.dependencies import get_db, get_current_user
from utils.validators import DocumentResponse, DocumentList, DocumentContent
from utils.security import validate_file, get_safe_file_path, FileValidationError
from database import crud
from database.models import User
from tasks import process_pdf_task, process_excel_task, process_word_task

router = APIRouter()

UPLOAD_DIR = "downloads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.get("/", response_model=DocumentList)
async def list_documents(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get list of all user documents.

    Returns list with active document ID.
    """
    documents = crud.get_user_documents(db, current_user)
    active_doc = crud.get_active_document_for_user(db, current_user)

    return {
        "documents": documents,
        "total": len(documents),
        "active_document_id": active_doc.id if active_doc else None
    }


@router.post("/upload", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload a document for processing.

    Supports: PDF, Excel, Word files.
    """
    # Determine file type
    file_ext = os.path.splitext(file.filename)[1].lower()

    file_type_map = {
        '.pdf': ('pdf', process_pdf_task),
        '.xlsx': ('excel', process_excel_task),
        '.xls': ('excel', process_excel_task),
        '.docx': ('word', process_word_task),
        '.doc': ('word', process_word_task),
    }

    if file_ext not in file_type_map:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type: {file_ext}. Supported: PDF, Excel, Word"
        )

    file_type, task_func = file_type_map[file_ext]

    # Save file (use internal database ID for consistent paths)
    safe_path = get_safe_file_path(UPLOAD_DIR, current_user.id, file.filename)

    try:
        contents = await file.read()
        with open(safe_path, 'wb') as f:
            f.write(contents)

        # Validate file
        is_valid, error_msg = validate_file(safe_path, file.filename, file_type)
        if not is_valid:
            os.remove(safe_path)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_msg
            )

        # Create document record (will be updated by Celery task)
        document = crud.create_user_document(
            db,
            current_user,
            filename=file.filename,
            file_path=safe_path,
            extracted_text="Processing...",
            document_type=file_type,
            file_size=len(contents)
        )

        # Queue processing task (use telegram user_id for Celery compatibility)
        # Note: For web users, user_id is negative; for Telegram users, it's their chat_id
        task_func.delay(
            chat_id=None,  # Not from Telegram
            user_id=current_user.user_id if hasattr(current_user, 'user_id') else current_user.id,
            username=current_user.username,
            first_name=current_user.first_name,
            last_name=current_user.last_name,
            file_path=safe_path,
            file_name=file.filename
        )

        return document

    except FileValidationError as e:
        if os.path.exists(safe_path):
            os.remove(safe_path)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        if os.path.exists(safe_path):
            os.remove(safe_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Upload failed: {str(e)}"
        )


@router.get("/{document_id}", response_model=DocumentContent)
async def get_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get document by ID with full content."""
    document = crud.get_document_by_id(db, document_id)

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )

    # Check ownership
    if document.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    return {
        "id": document.id,
        "file_name": document.file_name,
        "content": document.content or "",
        "summary": document.summary,
        "keywords": document.keywords
    }


@router.delete("/{document_id}")
async def delete_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a document."""
    document = crud.get_document_by_id(db, document_id)

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )

    # Check ownership
    if document.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    # Delete file from disk
    if document.file_path and os.path.exists(document.file_path):
        try:
            os.remove(document.file_path)
        except:
            pass

    # Delete from database
    crud.delete_document(db, document_id)

    return {"message": "Document deleted successfully"}


@router.put("/{document_id}/activate")
async def activate_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Set document as active for chat."""
    document = crud.get_document_by_id(db, document_id)

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )

    # Check ownership
    if document.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    crud.set_active_document(db, current_user, document_id)

    return {"message": "Document activated", "document_id": document_id}
