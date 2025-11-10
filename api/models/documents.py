"""
Pydantic models for Documents API
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DocumentResponse(BaseModel):
    """Response model for document data"""
    id: int
    file_name: str
    document_type: str
    file_size: int
    status: str
    is_active: bool
    uploaded_at: Optional[datetime]
    processed_at: Optional[datetime]
    summary: Optional[str]
    page_count: Optional[int]
    word_count: Optional[int]

    class Config:
        from_attributes = True


class DocumentListResponse(BaseModel):
    """Response model for document list"""
    documents: list[DocumentResponse]
    total: int
    page: int
    page_size: int


class UploadResponse(BaseModel):
    """Response model for document upload"""
    id: int
    file_name: str
    document_type: str
    file_size: int
    status: str
    message: str


class DeleteResponse(BaseModel):
    """Response model for document deletion"""
    success: bool
    message: str


class ActivateResponse(BaseModel):
    """Response model for document activation"""
    success: bool
    document_id: int
    message: str
