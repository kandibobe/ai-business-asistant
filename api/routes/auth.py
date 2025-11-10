"""
Authentication API routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import bcrypt

from api.dependencies import (
    get_db,
    verify_token,
    get_current_user,
    create_access_token,
    create_refresh_token,
    user_to_dict
)
from api.models.auth import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
    UserResponse,
    AuthResponse
)
from database import models

router = APIRouter()


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register(data: RegisterRequest, db: Session = Depends(get_db)):
    """
    Register a new user

    - **username**: Unique username (3-50 characters)
    - **password**: Password (minimum 6 characters)
    - **email**: Optional email address
    - **first_name**: Optional first name
    - **last_name**: Optional last name
    """
    # Check if username already exists
    existing_user = db.query(models.User).filter(
        models.User.username == data.username
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )

    # Hash password
    hashed_password = bcrypt.hashpw(
        data.password.encode('utf-8'),
        bcrypt.gensalt()
    )

    # Generate unique user_id (Telegram-style ID)
    # Get the highest user_id and increment
    max_user = db.query(models.User).order_by(models.User.user_id.desc()).first()
    new_user_id = (max_user.user_id + 1) if max_user else 1000000

    # Create new user
    new_user = models.User(
        user_id=new_user_id,
        username=data.username,
        password_hash=hashed_password.decode('utf-8'),
        email=data.email,
        first_name=data.first_name,
        last_name=data.last_name,
        language="en",
        is_premium=False
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Generate tokens
    access_token = create_access_token(new_user.id)
    refresh_token = create_refresh_token(new_user.id)

    return AuthResponse(
        user=UserResponse(**user_to_dict(new_user)),
        tokens=TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token
        )
    )


@router.post("/login", response_model=AuthResponse)
async def login(data: LoginRequest, db: Session = Depends(get_db)):
    """
    Login user and return JWT tokens

    - **username**: Username
    - **password**: Password
    """
    # Find user by username
    user = db.query(models.User).filter(
        models.User.username == data.username
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # Verify password
    if not user.password_hash:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Password not set for this user"
        )

    password_valid = bcrypt.checkpw(
        data.password.encode('utf-8'),
        user.password_hash.encode('utf-8')
    )

    if not password_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # Generate tokens
    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    return AuthResponse(
        user=UserResponse(**user_to_dict(user)),
        tokens=TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token
        )
    )


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: models.User = Depends(get_current_user)):
    """
    Get current authenticated user information

    Requires valid JWT token in Authorization header
    """
    return UserResponse(**user_to_dict(current_user))


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(user_id: int = Depends(verify_token)):
    """
    Refresh access token using refresh token

    Requires valid refresh token in Authorization header
    """
    # Generate new tokens
    access_token = create_access_token(user_id)
    refresh_token = create_refresh_token(user_id)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token
    )
