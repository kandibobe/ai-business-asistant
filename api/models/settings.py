"""
Pydantic models for Settings API
"""
from pydantic import BaseModel
from typing import Optional


class SettingsResponse(BaseModel):
    """Response model for user settings"""
    language: str
    ai_role: Optional[str]
    ai_style: Optional[str]
    mode: Optional[str]
    notifications_enabled: bool = True

    class Config:
        from_attributes = True


class SettingsUpdateRequest(BaseModel):
    """Request model for updating settings"""
    language: Optional[str] = None
    ai_role: Optional[str] = None
    ai_style: Optional[str] = None
    mode: Optional[str] = None
    notifications_enabled: Optional[bool] = None


class SettingsUpdateResponse(BaseModel):
    """Response model for settings update"""
    success: bool
    message: str
    settings: SettingsResponse
