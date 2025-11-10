"""
Pydantic models for Chat API
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class MessageRequest(BaseModel):
    """Request model for sending a chat message"""
    message: str = Field(..., min_length=1, max_length=10000)
    document_id: Optional[int] = None


class MessageResponse(BaseModel):
    """Response model for chat message"""
    answer: str
    response_time: float
    timestamp: datetime
    question_id: Optional[int] = None


class ChatHistoryItem(BaseModel):
    """Single item in chat history"""
    id: int
    question: str
    answer: str
    timestamp: datetime
    response_time: Optional[float]
    document_id: Optional[int]

    class Config:
        from_attributes = True


class ChatHistoryResponse(BaseModel):
    """Response model for chat history"""
    history: list[ChatHistoryItem]
    total: int
