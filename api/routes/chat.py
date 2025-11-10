"""
Chat routes.
Send messages to AI, get chat history.
"""
from fastapi import APIRouter, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
import google.generativeai as genai
import os
from dotenv import load_dotenv
import time
import logging

load_dotenv()

from api.dependencies import get_db, get_current_user
from utils.validators import ChatMessage, ChatResponse
from utils.ai_helpers import (
    generate_ai_response,
    safe_get_text,
    truncate_context,
    AIServiceError,
    AIRateLimitError,
    AIQuotaError,
)
from database import crud
from database.models import User
from config import GEMINI_MODEL_NAME

logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize Gemini
gemini_api_key = os.getenv('GEMINI_API_KEY')
if gemini_api_key:
    genai.configure(api_key=gemini_api_key)
    gemini_model = genai.GenerativeModel(GEMINI_MODEL_NAME)
else:
    gemini_model = None


@router.post("/message", response_model=ChatResponse)
async def send_message(
    message: ChatMessage,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Send a message to AI.

    If document_id provided, uses that document as context.
    Otherwise, uses active document.
    """
    if not gemini_model:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI service not configured"
        )

    # Get document for context
    document = None
    if message.document_id:
        document = crud.get_document_by_id(db, message.document_id)
        if not document or document.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found"
            )
    else:
        document = crud.get_active_document_for_user(db, current_user)

    if not document:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No active document. Please upload and activate a document first."
        )

    # Truncate context if too long to avoid token limits
    document_content = truncate_context(document.content or "", max_tokens=30000)

    # Build prompt
    prompt = f"""
    You are a business analytics expert. Analyze the document text provided below and answer the user's question.
    Your answer should be clear, concise and based EXCLUSIVELY on the information from the document.
    Do not make up anything that is not in the text.

    --- DOCUMENT TEXT ---
    {document_content}
    --- END OF DOCUMENT TEXT ---

    USER'S QUESTION:
    "{message.message}"
    """

    # Call AI with retry logic
    start_time = time.time()
    try:
        logger.info(f"Sending message to AI for user {current_user.user_id}")
        response = generate_ai_response(gemini_model, prompt)
        response_time_ms = int((time.time() - start_time) * 1000)

        # Safely extract text
        response_text = safe_get_text(response)
        if not response_text:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="AI did not generate a valid response"
            )

        logger.info(f"AI response generated in {response_time_ms}ms")

        return {
            "message": response_text,
            "response_time_ms": response_time_ms,
            "cached": False,
            "tokens_used": None
        }

    except AIRateLimitError as e:
        logger.error(f"AI rate limit exceeded: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="AI service rate limit exceeded. Please try again in a few moments."
        )

    except AIQuotaError as e:
        logger.error(f"AI quota exceeded: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI service quota exceeded. Please contact support."
        )

    except AIServiceError as e:
        logger.error(f"AI service error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI service error: {str(e)}"
        )

    except (ConnectionError, TimeoutError) as e:
        logger.error(f"Network error after retries: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI service temporarily unavailable. Please try again."
        )

    except Exception as e:
        logger.exception(f"Unexpected error in AI chat: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )


@router.get("/history/{document_id}")
async def get_chat_history(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get chat history for a document.

    TODO: Implement chat history storage.
    """
    document = crud.get_document_by_id(db, document_id)

    if not document or document.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )

    # TODO: Implement chat history storage
    return {
        "document_id": document_id,
        "messages": [],
        "total_messages": 0
    }


# WebSocket endpoint for real-time chat
@router.websocket("/ws")
async def websocket_chat(websocket: WebSocket):
    """
    WebSocket endpoint for real-time chat.

    Client should send: {"token": "jwt_token", "message": "question", "document_id": 123}
    """
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_json()

            # TODO: Implement proper WebSocket authentication and chat
            await websocket.send_json({
                "message": "WebSocket chat not yet implemented",
                "status": "info"
            })

    except WebSocketDisconnect:
        pass
