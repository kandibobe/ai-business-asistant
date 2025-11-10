"""
Settings API routes
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.dependencies import get_db, get_current_user
from api.models.settings import (
    SettingsResponse,
    SettingsUpdateRequest,
    SettingsUpdateResponse
)
from database import models
from database.crud import update_user_settings

router = APIRouter()


@router.get("", response_model=SettingsResponse)
async def get_settings(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current user settings
    """
    return SettingsResponse(
        language=current_user.language or "en",
        ai_role=getattr(current_user, 'ai_role', None),
        ai_style=getattr(current_user, 'ai_style', None),
        mode=getattr(current_user, 'mode', None),
        notifications_enabled=True
    )


@router.put("", response_model=SettingsUpdateResponse)
async def update_settings(
    settings: SettingsUpdateRequest,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update user settings

    - **language**: User interface language (en, ru, de)
    - **ai_role**: AI assistant role
    - **ai_style**: AI response style
    - **mode**: User mode
    - **notifications_enabled**: Enable/disable notifications
    """
    # Build update dictionary
    updates = {}
    if settings.language is not None:
        updates['language'] = settings.language
    if settings.ai_role is not None:
        updates['ai_role'] = settings.ai_role
    if settings.ai_style is not None:
        updates['ai_style'] = settings.ai_style
    if settings.mode is not None:
        updates['mode'] = settings.mode

    # Update user settings
    if updates:
        updated_user = update_user_settings(db, current_user.user_id, **updates)
        current_user = updated_user

    return SettingsUpdateResponse(
        success=True,
        message="Settings updated successfully",
        settings=SettingsResponse(
            language=current_user.language or "en",
            ai_role=getattr(current_user, 'ai_role', None),
            ai_style=getattr(current_user, 'ai_style', None),
            mode=getattr(current_user, 'mode', None),
            notifications_enabled=True
        )
    )


@router.post("/language")
async def change_language(
    language: str,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Quick endpoint to change language
    """
    if language not in ['en', 'ru', 'de']:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid language. Supported: en, ru, de"
        )

    current_user.language = language
    db.commit()

    return {
        "success": True,
        "language": language,
        "message": f"Language changed to {language}"
    }
