"""
Settings routes.
Get/update user settings.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.dependencies import get_db, get_current_user
from utils.validators import UserSettings, SettingsUpdate
from database.models import User

router = APIRouter()


@router.get("/", response_model=UserSettings)
async def get_settings(
    current_user: User = Depends(get_current_user)
):
    """Get current user settings."""
    return {
        "language": current_user.language or "ru",
        "mode": current_user.mode or "standard",
        "ai_role": current_user.ai_role or "assistant",
        "response_style": current_user.response_style or "standard",
        "notifications_enabled": current_user.notifications_enabled == "true",
        "auto_analysis_enabled": current_user.auto_analysis_enabled == "true"
    }


@router.put("/", response_model=UserSettings)
async def update_settings(
    settings: SettingsUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user settings."""
    # Update only provided fields
    if settings.language is not None:
        current_user.language = settings.language

    if settings.mode is not None:
        current_user.mode = settings.mode

    if settings.ai_role is not None:
        current_user.ai_role = settings.ai_role

    if settings.response_style is not None:
        current_user.response_style = settings.response_style

    if settings.notifications_enabled is not None:
        current_user.notifications_enabled = "true" if settings.notifications_enabled else "false"

    if settings.auto_analysis_enabled is not None:
        current_user.auto_analysis_enabled = "true" if settings.auto_analysis_enabled else "false"

    db.commit()
    db.refresh(current_user)

    # Return updated settings
    return {
        "language": current_user.language,
        "mode": current_user.mode,
        "ai_role": current_user.ai_role,
        "response_style": current_user.response_style,
        "notifications_enabled": current_user.notifications_enabled == "true",
        "auto_analysis_enabled": current_user.auto_analysis_enabled == "true"
    }
