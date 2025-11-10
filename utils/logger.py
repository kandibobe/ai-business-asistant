"""
Structured logging configuration.
"""
import logging
import sys
from datetime import datetime
from typing import Optional

# ANSI color codes for console output
COLORS = {
    'DEBUG': '\033[36m',      # Cyan
    'INFO': '\033[32m',       # Green
    'WARNING': '\033[33m',    # Yellow
    'ERROR': '\033[31m',      # Red
    'CRITICAL': '\033[35m',   # Magenta
    'RESET': '\033[0m',       # Reset
}


class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors for console output."""

    def format(self, record: logging.LogRecord) -> str:
        # Add timestamp
        record.timestamp = datetime.utcnow().isoformat()

        # Add color to level name for console
        levelname = record.levelname
        if sys.stderr.isatty():  # Only add colors if outputting to terminal
            color = COLORS.get(levelname, COLORS['RESET'])
            record.levelname = f"{color}{levelname}{COLORS['RESET']}"

        # Format the message
        formatted = super().format(record)

        # Reset levelname for next use
        record.levelname = levelname

        return formatted


def setup_logging(
    level: str = "INFO",
    log_file: Optional[str] = None,
    json_logs: bool = False
) -> None:
    """
    Configure application-wide logging.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path for file logging
        json_logs: If True, use JSON format for logs (good for production)
    """
    # Convert string level to logging constant
    numeric_level = getattr(logging, level.upper(), logging.INFO)

    # Create root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)

    # Remove existing handlers
    root_logger.handlers.clear()

    # Console handler with colored output
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(numeric_level)

    if json_logs:
        # JSON format for production
        console_format = (
            '{"timestamp":"%(timestamp)s","level":"%(levelname)s",'
            '"name":"%(name)s","message":"%(message)s",'
            '"module":"%(module)s","function":"%(funcName)s"}'
        )
        console_formatter = logging.Formatter(console_format)
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

        # Always use structured format for files
        file_format = (
            '%(timestamp)s | %(levelname)-8s | %(name)-30s | '
            '%(message)s | %(filename)s:%(lineno)d'
        )
        file_formatter = logging.Formatter(file_format)
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)

    # Suppress noisy loggers
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('telegram').setLevel(logging.WARNING)
    logging.getLogger('httpx').setLevel(logging.WARNING)
    logging.getLogger('httpcore').setLevel(logging.WARNING)

    root_logger.info(f"Logging configured: level={level}, file={log_file}")


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance.

    Args:
        name: Logger name (usually __name__)

    Returns:
        Logger instance
    """
    return logging.getLogger(name)


# Context manager for temporary log level changes
class LogLevel:
    """Context manager to temporarily change log level."""

    def __init__(self, logger: logging.Logger, level: str):
        self.logger = logger
        self.new_level = getattr(logging, level.upper())
        self.old_level = logger.level

    def __enter__(self):
        self.logger.setLevel(self.new_level)
        return self.logger

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logger.setLevel(self.old_level)


# Usage examples:
if __name__ == "__main__":
    # Setup logging
    setup_logging(level="DEBUG")

    # Get logger
    logger = get_logger(__name__)

    # Test all log levels
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")

    # Test context manager
    with LogLevel(logger, "ERROR"):
        logger.info("This won't show")
        logger.error("This will show")

    logger.info("Back to INFO level")
