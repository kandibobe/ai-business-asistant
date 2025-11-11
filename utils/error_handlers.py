"""
Enhanced error handlers with retry logic and user-friendly messages.

Provides:
- Global exception handlers for FastAPI
- Bot error handlers with graceful degradation
- Retry logic with exponential backoff
- Contextual error messages
- Error tracking and logging
"""
import logging
import traceback
import sys
from typing import Optional, Callable, Any
from functools import wraps

from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from telegram import Update
from telegram.ext import ContextTypes

from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log,
)

logger = logging.getLogger(__name__)


# ==================== Error Types ====================

class AppError(Exception):
    """Base application error."""
    def __init__(self, message: str, error_code: str = "APP_ERROR", status_code: int = 500):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        super().__init__(self.message)


class DatabaseError(AppError):
    """Database operation failed."""
    def __init__(self, message: str):
        super().__init__(message, "DATABASE_ERROR", 500)


class ValidationError(AppError):
    """Input validation failed."""
    def __init__(self, message: str):
        super().__init__(message, "VALIDATION_ERROR", 400)


class AuthenticationError(AppError):
    """Authentication failed."""
    def __init__(self, message: str):
        super().__init__(message, "AUTH_ERROR", 401)


class AuthorizationError(AppError):
    """Authorization failed (insufficient permissions)."""
    def __init__(self, message: str):
        super().__init__(message, "AUTHORIZATION_ERROR", 403)


class NotFoundError(AppError):
    """Resource not found."""
    def __init__(self, message: str):
        super().__init__(message, "NOT_FOUND", 404)


class RateLimitError(AppError):
    """Rate limit exceeded."""
    def __init__(self, message: str):
        super().__init__(message, "RATE_LIMIT", 429)


class ExternalServiceError(AppError):
    """External service (AI, etc.) failed."""
    def __init__(self, message: str):
        super().__init__(message, "EXTERNAL_SERVICE_ERROR", 503)


# ==================== FastAPI Error Handlers ====================

async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    """
    Handle custom application errors.

    Returns user-friendly JSON response with error details.
    """
    logger.error(
        f"Application error: {exc.error_code}",
        extra={
            "error_code": exc.error_code,
            "message": exc.message,
            "path": request.url.path,
            "method": request.method,
        },
        exc_info=True
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.error_code,
                "message": exc.message,
                "type": exc.__class__.__name__,
            }
        }
    )


async def validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """
    Handle Pydantic validation errors.

    Returns detailed validation error information.
    """
    logger.warning(
        "Validation error",
        extra={
            "path": request.url.path,
            "errors": exc.errors(),
        }
    )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Input validation failed",
                "details": exc.errors()
            }
        }
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    """
    Handle HTTP exceptions (404, 405, etc.).
    """
    logger.warning(
        f"HTTP {exc.status_code}: {exc.detail}",
        extra={
            "status_code": exc.status_code,
            "path": request.url.path,
        }
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": f"HTTP_{exc.status_code}",
                "message": exc.detail,
            }
        }
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handle all unhandled exceptions.

    Logs full traceback and returns generic error to user.
    """
    logger.error(
        "Unhandled exception",
        extra={
            "path": request.url.path,
            "method": request.method,
            "exception_type": type(exc).__name__,
        },
        exc_info=True
    )

    # In production, don't expose internal details
    from config import is_production

    if is_production():
        message = "An internal error occurred. Please try again later."
        details = None
    else:
        message = f"{type(exc).__name__}: {str(exc)}"
        details = traceback.format_exc()

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": "INTERNAL_ERROR",
                "message": message,
                "details": details,
            }
        }
    )


def register_fastapi_error_handlers(app) -> None:
    """
    Register all error handlers with FastAPI app.

    Usage:
        from fastapi import FastAPI
        app = FastAPI()
        register_fastapi_error_handlers(app)
    """
    app.add_exception_handler(AppError, app_error_handler)
    app.add_exception_handler(RequestValidationError, validation_error_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)

    logger.info("✅ FastAPI error handlers registered")


# ==================== Telegram Bot Error Handler ====================

async def telegram_error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Global error handler for Telegram bot.

    Provides user-friendly error messages and logs full details.
    """
    logger.error(
        "❌ Telegram bot error",
        exc_info=context.error
    )

    # Try to send user-friendly message
    try:
        if isinstance(update, Update) and update.effective_message:
            error = context.error
            error_type = type(error).__name__

            # Determine user-friendly message based on error type
            if "Database" in error_type or "SQL" in error_type:
                user_message = (
                    "⚠️ Проблема с базой данных.\n\n"
                    "💡 Возможно требуется миграция: python migrate_db.py"
                )

            elif "Connection" in error_type or "Network" in error_type:
                user_message = (
                    "⚠️ Проблема с подключением.\n\n"
                    "💡 Проверьте Redis и PostgreSQL."
                )

            elif "RateLimit" in error_type or "TooManyRequests" in error_type:
                user_message = (
                    "⚠️ Превышен лимит запросов.\n\n"
                    "Пожалуйста, подождите немного и попробуйте снова."
                )

            elif "Authentication" in error_type or "Unauthorized" in error_type:
                user_message = (
                    "⚠️ Ошибка аутентификации.\n\n"
                    "Возможно, истек срок действия токена. "
                    "Попробуйте заново: /start"
                )

            elif "File" in error_type or "Document" in error_type:
                user_message = (
                    "⚠️ Не удалось обработать файл.\n\n"
                    "Проверьте:\n"
                    "- Файл не поврежден\n"
                    "- Размер файла допустимый\n"
                    "- Формат файла поддерживается"
                )

            elif "Gemini" in error_type or "AI" in error_type:
                user_message = (
                    "⚠️ Проблема с AI сервисом.\n\n"
                    "Попробуйте еще раз через несколько секунд."
                )

            else:
                user_message = (
                    "⚠️ Произошла ошибка при обработке запроса.\n\n"
                    "Пожалуйста, попробуйте снова или обратитесь к администратору."
                )

            # Add help commands
            user_message += "\n\n🆘 Доступные команды:\n/start - Начать заново\n/help - Помощь"

            await update.effective_message.reply_text(user_message)

    except Exception as e:
        logger.error(f"❌ Failed to send error message to user: {e}")


# ==================== Retry Decorators ====================

def retry_on_error(
    max_attempts: int = 3,
    wait_min: int = 2,
    wait_max: int = 10,
    exceptions=(Exception,)
):
    """
    Decorator to retry function on error with exponential backoff.

    Args:
        max_attempts: Maximum number of retry attempts
        wait_min: Minimum wait time in seconds
        wait_max: Maximum wait time in seconds
        exceptions: Tuple of exceptions to retry on

    Usage:
        @retry_on_error(max_attempts=3)
        async def my_function():
            ...
    """
    return retry(
        stop=stop_after_attempt(max_attempts),
        wait=wait_exponential(multiplier=1, min=wait_min, max=wait_max),
        retry=retry_if_exception_type(exceptions),
        before_sleep=before_sleep_log(logger, logging.WARNING),
        reraise=True
    )


def safe_execute(default_return: Any = None, log_error: bool = True):
    """
    Decorator to safely execute function and return default on error.

    Args:
        default_return: Value to return if function raises exception
        log_error: Whether to log the error

    Usage:
        @safe_execute(default_return=[])
        def get_user_documents(user_id):
            ...
    """
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                if log_error:
                    logger.error(
                        f"Error in {func.__name__}: {e}",
                        exc_info=True
                    )
                return default_return

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if log_error:
                    logger.error(
                        f"Error in {func.__name__}: {e}",
                        exc_info=True
                    )
                return default_return

        # Return appropriate wrapper based on function type
        import asyncio
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator


# ==================== Context Manager for Error Handling ====================

class ErrorContext:
    """
    Context manager for error handling with custom messages.

    Usage:
        with ErrorContext("uploading document", user_message="Failed to upload"):
            upload_document()
    """

    def __init__(
        self,
        operation: str,
        user_message: Optional[str] = None,
        raise_error: bool = True
    ):
        self.operation = operation
        self.user_message = user_message
        self.raise_error = raise_error

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            logger.error(
                f"Error during {self.operation}: {exc_val}",
                exc_info=(exc_type, exc_val, exc_tb)
            )

            if not self.raise_error:
                return True  # Suppress exception

        return False  # Propagate exception


# ==================== Graceful Degradation ====================

async def with_fallback(
    primary_func: Callable,
    fallback_func: Optional[Callable] = None,
    fallback_value: Any = None,
    *args,
    **kwargs
) -> Any:
    """
    Execute function with fallback on failure.

    Args:
        primary_func: Main function to execute
        fallback_func: Fallback function to execute on error
        fallback_value: Value to return if both fail
        *args, **kwargs: Arguments for functions

    Returns:
        Result from primary_func, or fallback, or fallback_value

    Example:
        result = await with_fallback(
            get_from_cache,
            fallback_func=get_from_database,
            fallback_value={},
            user_id=123
        )
    """
    try:
        if asyncio.iscoroutinefunction(primary_func):
            return await primary_func(*args, **kwargs)
        else:
            return primary_func(*args, **kwargs)

    except Exception as e:
        logger.warning(f"Primary function failed: {e}, trying fallback")

        if fallback_func:
            try:
                if asyncio.iscoroutinefunction(fallback_func):
                    return await fallback_func(*args, **kwargs)
                else:
                    return fallback_func(*args, **kwargs)

            except Exception as e2:
                logger.error(f"Fallback function also failed: {e2}")

        return fallback_value


# Make asyncio available for type checking
import asyncio


# ==================== Usage Examples ====================

if __name__ == "__main__":
    """
    Test error handlers.

    Run: python -m utils.error_handlers
    """
    import asyncio

    print("=" * 60)
    print("🔧 Testing Error Handlers")
    print("=" * 60)

    # Test retry decorator
    print("\n[1/3] Testing retry decorator...")

    attempt_count = 0

    @retry_on_error(max_attempts=3, wait_min=1, wait_max=2)
    async def flaky_function():
        global attempt_count
        attempt_count += 1
        print(f"   Attempt {attempt_count}")

        if attempt_count < 3:
            raise ConnectionError("Simulated connection error")

        return "Success!"

    async def test_retry():
        global attempt_count
        attempt_count = 0
        result = await flaky_function()
        print(f"   ✅ Result: {result}")

    asyncio.run(test_retry())

    # Test safe execute
    print("\n[2/3] Testing safe_execute decorator...")

    @safe_execute(default_return="Default value")
    async def unsafe_function():
        raise ValueError("Something went wrong")

    async def test_safe():
        result = await unsafe_function()
        print(f"   ✅ Returned: {result}")

    asyncio.run(test_safe())

    # Test error context
    print("\n[3/3] Testing error context...")

    with ErrorContext("test operation", raise_error=False):
        print("   Executing operation that will fail...")
        raise RuntimeError("Test error")

    print("   ✅ Error handled gracefully")

    print("\n" + "=" * 60)
    print("✅ All tests completed!")
    print("=" * 60)
