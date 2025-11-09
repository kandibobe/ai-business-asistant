"""
Pydantic validators for API request/response validation.
"""
from typing import Optional, List
from pydantic import BaseModel, Field, validator, EmailStr
from datetime import datetime


# === Authentication Models ===

class UserRegister(BaseModel):
    """Схема регистрации пользователя."""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8, max_length=100)
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)

    @validator('username')
    def username_alphanumeric(cls, v):
        if not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError('Username must be alphanumeric (with _ and - allowed)')
        return v

    @validator('password')
    def password_strength(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v


class UserLogin(BaseModel):
    """Схема логина пользователя."""
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8, max_length=100)


class Token(BaseModel):
    """Схема JWT токена."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenRefresh(BaseModel):
    """Схема обновления токена."""
    refresh_token: str


class UserResponse(BaseModel):
    """Схема ответа с данными пользователя."""
    id: int
    user_id: int
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    language: str = "ru"
    mode: str = "standard"
    ai_role: str = "assistant"
    response_style: str = "standard"
    created_at: datetime

    class Config:
        from_attributes = True


# === Document Models ===

class DocumentUpload(BaseModel):
    """Метаданные при загрузке документа."""
    document_type: str = Field(..., regex="^(pdf|excel|word|audio|url)$")


class DocumentResponse(BaseModel):
    """Схема ответа с данными документа."""
    id: int
    file_name: str
    document_type: Optional[str]
    file_size: Optional[int]
    word_count: Optional[int]
    char_count: Optional[int]
    uploaded_at: datetime
    processed_at: Optional[datetime]

    class Config:
        from_attributes = True


class DocumentList(BaseModel):
    """Список документов."""
    documents: List[DocumentResponse]
    total: int
    active_document_id: Optional[int]


class DocumentContent(BaseModel):
    """Содержимое документа."""
    id: int
    file_name: str
    content: str
    summary: Optional[str]
    keywords: Optional[str]


# === Chat Models ===

class ChatMessage(BaseModel):
    """Сообщение в чате."""
    message: str = Field(..., min_length=1, max_length=10000)
    document_id: Optional[int] = None

    @validator('message')
    def sanitize_message(cls, v):
        # Базовая санитизация - удаляем потенциально опасные символы
        import re
        # Удаляем нулевые байты
        v = v.replace('\x00', '')
        # Ограничиваем множественные пробелы
        v = re.sub(r'\s+', ' ', v)
        return v.strip()


class ChatResponse(BaseModel):
    """Ответ от AI."""
    message: str
    response_time_ms: Optional[int]
    cached: bool = False
    tokens_used: Optional[int]


class ChatHistory(BaseModel):
    """История чата."""
    document_id: int
    messages: List[dict]
    total_messages: int


# === Settings Models ===

class UserSettings(BaseModel):
    """Настройки пользователя."""
    language: str = Field("ru", regex="^(ru|en|de|uk)$")
    mode: str = Field("standard", regex="^(fast|standard|advanced)$")
    ai_role: str = Field("assistant", regex="^(assistant|analyst|consultant|advisor|teacher|researcher|creative|developer|business_expert|data_scientist|financial_advisor)$")
    response_style: str = Field("standard", regex="^(brief|standard|detailed|creative|formal|casual|technical)$")
    notifications_enabled: bool = True
    auto_analysis_enabled: bool = False


class SettingsUpdate(BaseModel):
    """Обновление настроек."""
    language: Optional[str] = Field(None, regex="^(ru|en|de|uk)$")
    mode: Optional[str] = Field(None, regex="^(fast|standard|advanced)$")
    ai_role: Optional[str] = None
    response_style: Optional[str] = None
    notifications_enabled: Optional[bool] = None
    auto_analysis_enabled: Optional[bool] = None


# === Analytics Models ===

class UserStats(BaseModel):
    """Статистика пользователя."""
    total_documents: int
    total_questions: int
    avg_response_time_ms: Optional[float]
    total_sessions: int
    documents_by_type: dict
    recent_activity: List[dict]


class DocumentStats(BaseModel):
    """Статистика по документу."""
    document_id: int
    total_questions: int
    avg_response_time_ms: Optional[float]
    question_history: List[dict]


# === Developer Tools Models ===

class JsonValidateRequest(BaseModel):
    """Запрос валидации JSON."""
    json_string: str = Field(..., max_length=100000)


class Base64EncodeRequest(BaseModel):
    """Запрос кодирования в Base64."""
    text: str = Field(..., max_length=100000)


class HashGenerateRequest(BaseModel):
    """Запрос генерации хэша."""
    text: str = Field(..., max_length=100000)
    algorithm: str = Field("sha256", regex="^(md5|sha1|sha256|sha512)$")


class QRCodeRequest(BaseModel):
    """Запрос генерации QR кода."""
    text: str = Field(..., max_length=2000)
    size: int = Field(300, ge=100, le=1000)


# === Error Response ===

class ErrorResponse(BaseModel):
    """Стандартный ответ с ошибкой."""
    detail: str
    error_type: Optional[str]
    field: Optional[str]


# === Success Response ===

class SuccessResponse(BaseModel):
    """Стандартный успешный ответ."""
    success: bool = True
    message: str


# === Pagination ===

class PaginationParams(BaseModel):
    """Параметры пагинации."""
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)


class PaginatedResponse(BaseModel):
    """Пагинированный ответ."""
    items: List[dict]
    total: int
    page: int
    page_size: int
    total_pages: int


# Пример использования
if __name__ == "__main__":
    # Тест валидации
    print("Testing Pydantic validators...")

    # Тест регистрации
    try:
        user = UserRegister(
            email="test@example.com",
            username="test_user",
            password="StrongPass123",
            first_name="Test",
            last_name="User"
        )
        print(f"✅ Valid user registration: {user.username}")
    except Exception as e:
        print(f"❌ Validation error: {e}")

    # Тест слабого пароля
    try:
        weak_user = UserRegister(
            email="test@example.com",
            username="test",
            password="weak",
        )
        print(f"❌ Should have failed: {weak_user.password}")
    except Exception as e:
        print(f"✅ Correctly rejected weak password: {e}")

    # Тест настроек
    try:
        settings = UserSettings(
            language="ru",
            mode="advanced",
            ai_role="analyst"
        )
        print(f"✅ Valid settings: {settings.dict()}")
    except Exception as e:
        print(f"❌ Settings validation error: {e}")
