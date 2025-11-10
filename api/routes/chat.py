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

load_dotenv()

from api.dependencies import get_db, get_current_user
from utils.validators import ChatMessage, ChatResponse
from database import crud
from database.models import User
from config import GEMINI_MODEL_NAME

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

    # Build prompt
    prompt = f"""
    You are a business analytics expert. Analyze the document text provided below and answer the user's question.
    Your answer should be clear, concise and based EXCLUSIVELY on the information from the document.
    Do not make up anything that is not in the text.

    --- DOCUMENT TEXT ---
    {document.content}
    --- END OF DOCUMENT TEXT ---

    USER'S QUESTION:
    "{message.message}"
    """

    # Call AI
    start_time = time.time()
    try:
        response = gemini_model.generate_content(prompt)
        response_time_ms = int((time.time() - start_time) * 1000)

        return {
            "message": response.text,
            "response_time_ms": response_time_ms,
            "cached": False,
            "tokens_used": None
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI error: {str(e)}"
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
