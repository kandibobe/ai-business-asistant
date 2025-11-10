"""
Dependencies for FastAPI routes (auth, database, etc.)
"""
from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import jwt
from datetime import datetime, timedelta
import os

from database.database import SessionLocal
from database import models

# Security
security = HTTPBearer()

# JWT Configuration
JWT_SECRET = os.getenv("JWT_SECRET", "your-secret-key-change-in-production")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 1 hour
REFRESH_TOKEN_EXPIRE_DAYS = 7  # 7 days


def get_db() -> Generator[Session, None, None]:
    """
    Database dependency - provides database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_access_token(user_id: int) -> str:
    """
    Create JWT access token
    """
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        "user_id": user_id,
        "exp": expire,
        "type": "access"
    }
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def create_refresh_token(user_id: int) -> str:
    """
    Create JWT refresh token
    """
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode = {
        "user_id": user_id,
        "exp": expire,
        "type": "refresh"
    }
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt


async def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> int:
    """
    Verify JWT token and return user_id
    """
    token = credentials.credentials

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id: int = payload.get("user_id")
        token_type: str = payload.get("type")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if token_type != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user_id

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(
    user_id: int = Depends(verify_token),
    db: Session = Depends(get_db)
) -> models.User:
    """
    Get current authenticated user from database
    """
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


def user_to_dict(user: models.User) -> dict:
    """
    Convert User model to dictionary for API response
    """
    return {
        "id": user.id,
        "user_id": user.user_id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "language": user.language,
        "is_premium": user.is_premium or False,
        "created_at": user.created_at.isoformat() if user.created_at else None
    }


def document_to_dict(doc: models.Document) -> dict:
    """
    Convert Document model to dictionary for API response
    """
    return {
        "id": doc.id,
        "file_name": doc.file_name,
        "document_type": doc.document_type,
        "file_size": doc.file_size,
        "status": doc.status,
        "is_active": doc.is_active,
        "uploaded_at": doc.uploaded_at.isoformat() if doc.uploaded_at else None,
        "processed_at": doc.processed_at.isoformat() if doc.processed_at else None,
        "summary": doc.summary,
        "page_count": getattr(doc, 'page_count', None),
        "word_count": getattr(doc, 'word_count', None)
    }
