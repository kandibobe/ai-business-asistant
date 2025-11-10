"""
Pydantic models for Authentication API
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class RegisterRequest(BaseModel):
    """Request model for user registration"""
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    email: Optional[EmailStr] = None
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)


class LoginRequest(BaseModel):
    """Request model for user login"""
    username: str
    password: str


class TokenResponse(BaseModel):
    """Response model for token endpoints"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    """Response model for user data"""
    id: int
    user_id: int
    username: str
    first_name: Optional[str]
    last_name: Optional[str]
    language: str
    is_premium: bool
    created_at: Optional[datetime]

    class Config:
        from_attributes = True


class AuthResponse(BaseModel):
    """Complete authentication response with user and tokens"""
    user: UserResponse
    tokens: TokenResponse
