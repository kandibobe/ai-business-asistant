"""
Chat API routes (REST + WebSocket)
"""
from fastapi import APIRouter, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from typing import Optional
import time
from datetime import datetime
import os

from api.dependencies import get_db, get_current_user
from api.models.chat import (
    MessageRequest,
    MessageResponse,
    ChatHistoryItem,
    ChatHistoryResponse
)
from database import models
from analytics.stats import track_question

# Import AI model
import google.generativeai as genai
from config.settings import GEMINI_API_KEY

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

router = APIRouter()


async def generate_ai_response(question: str, context: Optional[str] = None) -> str:
    """
    Generate AI response using Gemini
    """
    try:
        model = genai.GenerativeModel('gemini-pro')

        # Build prompt with context if available
        if context:
            prompt = f"""You are an AI business intelligence assistant. Answer the following question based on the provided document context.

Document Context:
{context[:4000]}

Question: {question}

Provide a helpful, accurate answer based on the document content."""
        else:
            prompt = f"""You are an AI business intelligence assistant. Answer the following question:

Question: {question}

Provide a helpful and professional answer."""

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI generation failed: {str(e)}"
        )


@router.post("/message", response_model=MessageResponse)
async def send_message(
    data: MessageRequest,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Send a message and get AI response

    - **message**: User's question/message
    - **document_id**: Optional document ID for context
    """
    # Get document context if provided
    context = None
    document = None

    if data.document_id:
        document = db.query(models.Document).filter(
            models.Document.id == data.document_id,
            models.Document.user_id == current_user.id
        ).first()

        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found"
            )

        context = document.extracted_text

    # Generate AI response
    start_time = time.time()
    answer = await generate_ai_response(data.message, context)
    response_time = time.time() - start_time

    # Track question in database
    question_record = track_question(
        db=db,
        user_id=current_user.user_id,
        doc_id=data.document_id,
        question=data.message,
        answer=answer,
        response_time=response_time
    )

    return MessageResponse(
        answer=answer,
        response_time=round(response_time, 2),
        timestamp=datetime.now(),
        question_id=question_record.id if question_record else None
    )


@router.get("/history", response_model=ChatHistoryResponse)
async def get_chat_history(
    document_id: Optional[int] = None,
    limit: int = 50,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get chat history for the user (optionally filtered by document)

    - **document_id**: Optional document ID to filter history
    - **limit**: Maximum number of messages to return (default: 50)
    """
    query = db.query(models.Question).filter(
        models.Question.user_id == current_user.id
    )

    if document_id:
        query = query.filter(models.Question.document_id == document_id)

    total = query.count()
    questions = query.order_by(
        models.Question.created_at.desc()
    ).limit(limit).all()

    history = [
        ChatHistoryItem(
            id=q.id,
            question=q.question_text,
            answer=q.answer_text or "",
            timestamp=q.created_at,
            response_time=q.response_time,
            document_id=q.document_id
        )
        for q in questions
    ]

    return ChatHistoryResponse(
        history=history,
        total=total
    )


@router.delete("/history", status_code=status.HTTP_204_NO_CONTENT)
async def clear_chat_history(
    document_id: Optional[int] = None,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Clear chat history (optionally for specific document)

    - **document_id**: Optional document ID to clear history for
    """
    query = db.query(models.Question).filter(
        models.Question.user_id == current_user.id
    )

    if document_id:
        query = query.filter(models.Question.document_id == document_id)

    query.delete()
    db.commit()

    return None


@router.websocket("/ws")
async def websocket_chat(websocket: WebSocket, db: Session = Depends(get_db)):
    """
    WebSocket endpoint for real-time chat

    Send JSON: {"message": "your question", "document_id": 123 (optional)}
    Receive JSON: {"answer": "AI response", "response_time": 1.23, "timestamp": "..."}
    """
    await websocket.accept()

    try:
        while True:
            # Receive message from client
            data = await websocket.receive_json()

            message = data.get("message")
            document_id = data.get("document_id")
            user_id = data.get("user_id")  # Should be sent by client after auth

            if not message:
                await websocket.send_json({
                    "error": "Message is required"
                })
                continue

            # Get document context if provided
            context = None
            if document_id:
                document = db.query(models.Document).filter(
                    models.Document.id == document_id
                ).first()
                if document:
                    context = document.extracted_text

            # Generate AI response
            start_time = time.time()
            try:
                answer = await generate_ai_response(message, context)
                response_time = time.time() - start_time

                # Track question if user_id provided
                if user_id:
                    track_question(
                        db=db,
                        user_id=user_id,
                        doc_id=document_id,
                        question=message,
                        answer=answer,
                        response_time=response_time
                    )

                # Send response
                await websocket.send_json({
                    "answer": answer,
                    "response_time": round(response_time, 2),
                    "timestamp": datetime.now().isoformat()
                })

            except Exception as e:
                await websocket.send_json({
                    "error": f"Failed to generate response: {str(e)}"
                })

    except WebSocketDisconnect:
        print("WebSocket client disconnected")
    except Exception as e:
        print(f"WebSocket error: {e}")
        await websocket.close()
