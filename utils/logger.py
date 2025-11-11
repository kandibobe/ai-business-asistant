"""
Enhanced structured logging configuration with better context and formatting.

Provides:
- Structured JSON logging for production
- Colored console logging for development
- Request ID tracking
- User context tracking
- Performance metrics
"""
import logging
import sys
import json
from datetime import datetime
from typing import Optional, Dict, Any
from contextvars import ContextVar

# Context variables for request tracking
request_id_var: ContextVar[Optional[str]] = ContextVar('request_id', default=None)
user_id_var: ContextVar[Optional[int]] = ContextVar('user_id', default=None)

# ANSI color codes for console output
COLORS = {
    'DEBUG': '\033[36m',      # Cyan
    'INFO': '\033[32m',       # Green
    'WARNING': '\033[33m',    # Yellow
    'ERROR': '\033[31m',      # Red
    'CRITICAL': '\033[35m',   # Magenta
    'RESET': '\033[0m',       # Reset
}


class ContextualLogRecord(logging.LogRecord):
    """Enhanced LogRecord with contextual information."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add context variables
        self.request_id = request_id_var.get()
        self.user_id = user_id_var.get()
        self.timestamp = datetime.utcnow().isoformat()


class JSONFormatter(logging.Formatter):
    """
    JSON formatter for structured logging.

    Outputs logs in JSON format suitable for log aggregation systems
    like ELK, Grafana Loki, or Datadog.
    """

    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add context if available
        if hasattr(record, 'request_id') and record.request_id:
            log_data["request_id"] = record.request_id

        if hasattr(record, 'user_id') and record.user_id:
            log_data["user_id"] = record.user_id

        # Add extra fields
        if hasattr(record, '__dict__'):
            for key, value in record.__dict__.items():
                if key not in log_data and not key.startswith('_'):
                    try:
                        # Only add JSON-serializable values
                        json.dumps(value)
                        log_data[key] = value
                    except (TypeError, ValueError):
                        log_data[key] = str(value)

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data, ensure_ascii=False)


class ColoredFormatter(logging.Formatter):
    """
    Custom formatter with colors for console output.

    Provides human-readable colored output for development.
    """

    def format(self, record: logging.LogRecord) -> str:
        # Add timestamp
        if not hasattr(record, 'timestamp'):
            record.timestamp = datetime.utcnow().isoformat()

        # Build context string
        context_parts = []

        if hasattr(record, 'request_id') and record.request_id:
            context_parts.append(f"req:{record.request_id[:8]}")

        if hasattr(record, 'user_id') and record.user_id:
            context_parts.append(f"user:{record.user_id}")

        context_str = f" [{', '.join(context_parts)}]" if context_parts else ""

        # Add color to level name for console
        levelname = record.levelname
        if sys.stderr.isatty():  # Only add colors if outputting to terminal
            color = COLORS.get(levelname, COLORS['RESET'])
            record.levelname = f"{color}{levelname}{COLORS['RESET']}"

        # Add context to message
        original_msg = record.getMessage()
        record.msg = f"{original_msg}{context_str}"

        # Format the message
        formatted = super().format(record)

        # Reset for next use
        record.levelname = levelname
        record.msg = original_msg

        return formatted


def setup_logging(
    level: str = "INFO",
    log_file: Optional[str] = None,
    json_logs: bool = False
) -> None:
    """
    Configure application-wide logging with enhanced features.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path for file logging
        json_logs: If True, use JSON format for logs (good for production)
    """
    # Convert string level to logging constant
    numeric_level = getattr(logging, level.upper(), logging.INFO)

    # Set custom LogRecord factory for contextual logging
    logging.setLogRecordFactory(ContextualLogRecord)

    # Create root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)

    # Remove existing handlers
    root_logger.handlers.clear()

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(numeric_level)

    if json_logs:
        # JSON format for production
        console_formatter = JSONFormatter()
    else:
        # Human-readable format for development
        console_format = (
            '%(levelname)-8s [%(name)s] %(message)s '
            '(%(filename)s:%(lineno)d)'
        )
        console_formatter = ColoredFormatter(console_format)

    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)

    # File handler (if specified)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(numeric_level)

        # Always use JSON format for file logs
        file_formatter = JSONFormatter()
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)

    # Suppress noisy loggers
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('telegram').setLevel(logging.WARNING)
    logging.getLogger('httpx').setLevel(logging.WARNING)
    logging.getLogger('httpcore').setLevel(logging.WARNING)

    root_logger.info(f"Logging configured: level={level}, file={log_file}, json={json_logs}")


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance.

    Args:
        name: Logger name (usually __name__)

    Returns:
        Logger instance
    """
    return logging.getLogger(name)


# ==================== Context Management ====================

class LogContext:
    """
    Context manager for adding contextual information to logs.

    Usage:
        with LogContext(request_id="abc123", user_id=456):
            logger.info("User action")  # Will include request_id and user_id
    """

    def __init__(self, request_id: Optional[str] = None, user_id: Optional[int] = None):
        self.request_id = request_id
        self.user_id = user_id
        self.old_request_id = None
        self.old_user_id = None

    def __enter__(self):
        # Save old values
        self.old_request_id = request_id_var.get()
        self.old_user_id = user_id_var.get()

        # Set new values
        if self.request_id:
            request_id_var.set(self.request_id)
        if self.user_id:
            user_id_var.set(self.user_id)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Restore old values
        request_id_var.set(self.old_request_id)
        user_id_var.set(self.old_user_id)


class LogLevel:
    """
    Context manager to temporarily change log level.

    Usage:
        with LogLevel(logger, "DEBUG"):
            logger.debug("This will show")
    """

    def __init__(self, logger: logging.Logger, level: str):
        self.logger = logger
        self.new_level = getattr(logging, level.upper())
        self.old_level = logger.level

    def __enter__(self):
        self.logger.setLevel(self.new_level)
        return self.logger

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logger.setLevel(self.old_level)


# ==================== Helper Functions ====================

def set_request_context(request_id: str, user_id: Optional[int] = None) -> None:
    """
    Set request context for all subsequent logs.

    Args:
        request_id: Unique request identifier
        user_id: Optional user ID
    """
    request_id_var.set(request_id)
    if user_id:
        user_id_var.set(user_id)


def clear_request_context() -> None:
    """Clear request context."""
    request_id_var.set(None)
    user_id_var.set(None)


def log_function_call(logger: logging.Logger):
    """
    Decorator to log function calls with arguments.

    Usage:
        @log_function_call(logger)
        def my_function(arg1, arg2):
            ...
    """
    def decorator(func):
        from functools import wraps
        import asyncio

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            logger.debug(
                f"Calling {func.__name__}",
                extra={"args": str(args)[:100], "kwargs": str(kwargs)[:100]}
            )
            try:
                result = await func(*args, **kwargs)
                logger.debug(f"{func.__name__} completed successfully")
                return result
            except Exception as e:
                logger.error(
                    f"{func.__name__} failed: {e}",
                    exc_info=True
                )
                raise

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            logger.debug(
                f"Calling {func.__name__}",
                extra={"args": str(args)[:100], "kwargs": str(kwargs)[:100]}
            )
            try:
                result = func(*args, **kwargs)
                logger.debug(f"{func.__name__} completed successfully")
                return result
            except Exception as e:
                logger.error(
                    f"{func.__name__} failed: {e}",
                    exc_info=True
                )
                raise

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator


# ==================== Usage Examples ====================

if __name__ == "__main__":
    """
    Test enhanced logging.

    Run: python -m utils.logger
    """
    print("=" * 60)
    print("📝 Testing Enhanced Logging")
    print("=" * 60)

    # Test 1: Basic logging
    print("\n[1/4] Testing basic logging...")
    setup_logging(level="DEBUG", json_logs=False)
    logger = get_logger(__name__)

    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")

    # Test 2: Context logging
    print("\n[2/4] Testing context logging...")
    with LogContext(request_id="req-12345", user_id=42):
        logger.info("User performed action")
        logger.info("Another action with context")

    logger.info("Without context")

    # Test 3: JSON logging
    print("\n[3/4] Testing JSON logging...")
    setup_logging(level="INFO", json_logs=True)
    logger = get_logger(__name__)

    logger.info("JSON formatted message")
    logger.error("Error with context", extra={"error_code": "E001"})

    # Test 4: Log level context
    print("\n[4/4] Testing log level context...")
    setup_logging(level="INFO", json_logs=False)
    logger = get_logger(__name__)

    logger.info("This will show")
    logger.debug("This won't show")

    with LogLevel(logger, "DEBUG"):
        logger.debug("This will show inside context")

    logger.debug("This won't show again")

    print("\n" + "=" * 60)
    print("✅ All logging tests completed!")
    print("=" * 60)
