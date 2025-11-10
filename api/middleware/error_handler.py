"""
Global error handler middleware for FastAPI
"""
from fastapi import Request, status
from fastapi.responses import JSONResponse
import logging
import traceback

logger = logging.getLogger(__name__)


async def error_handler_middleware(request: Request, call_next):
    """
    Global error handler middleware
    Catches all unhandled exceptions and returns proper JSON response
    """
    try:
        response = await call_next(request)
        return response
    except Exception as exc:
        # Log the error with full traceback
        logger.error(f"Unhandled error in {request.method} {request.url.path}")
        logger.error(f"Error: {exc}")
        logger.error(traceback.format_exc())

        # Return user-friendly error response
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": "Internal server error",
                "type": type(exc).__name__,
                "path": str(request.url.path)
            }
        )
