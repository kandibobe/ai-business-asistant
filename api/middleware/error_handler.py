"""
Error handling middleware.
"""
import logging
from fastapi import Request

logger = logging.getLogger(__name__)


def log_exception(exc: Exception, request: Request = None):
    """Log exception with request details."""
    if request:
        logger.error(
            f"Exception occurred: {type(exc).__name__}: {str(exc)}",
            extra={
                "path": request.url.path,
                "method": request.method,
                "client": request.client.host if request.client else None
            },
            exc_info=True
        )
    else:
        logger.error(
            f"Exception occurred: {type(exc).__name__}: {str(exc)}",
            exc_info=True
        )
