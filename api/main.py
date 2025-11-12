"""
FastAPI application for AI Business Assistant.
REST API для веб-приложения.
"""
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import logging
import os
from dotenv import load_dotenv

load_dotenv()

# Try relative imports first, fall back to absolute
try:
    from .routes import auth, documents, chat, analytics, settings, tools
    from .middleware.error_handler import log_exception
except ImportError:
    from api.routes import auth, documents, chat, analytics, settings, tools
    from api.middleware.error_handler import log_exception

from utils.logger import setup_logging

# Setup structured logging
setup_logging(
    level=os.getenv("LOG_LEVEL", "INFO"),
    log_file=os.getenv("LOG_FILE"),
    json_logs=os.getenv("JSON_LOGS", "false").lower() == "true"
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="AI Business Assistant API",
    description="REST API for AI-powered business document analysis",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# CORS middleware
# SECURITY FIX: Restrict allowed headers and methods
ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', 'http://localhost:5173,http://localhost:3000').split(',')

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Removed PATCH
    allow_headers=["Content-Type", "Authorization", "Accept"],  # Whitelist
    expose_headers=["Content-Type"],  # Minimal exposure
    max_age=600  # Cache preflight requests for 10 minutes
)


# Security headers middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    """Add comprehensive security headers to all responses."""
    response = await call_next(request)

    # Prevent MIME type sniffing
    response.headers["X-Content-Type-Options"] = "nosniff"

    # Prevent clickjacking attacks
    response.headers["X-Frame-Options"] = "DENY"

    # Enable XSS protection (legacy browsers)
    response.headers["X-XSS-Protection"] = "1; mode=block"

    # Force HTTPS (only if in production)
    is_production = os.getenv("ENVIRONMENT", "development").lower() == "production"
    if is_production:
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"

    # Content Security Policy - strict policy for API
    csp_directives = [
        "default-src 'self'",
        "script-src 'self'",
        "style-src 'self' 'unsafe-inline'",  # Allow inline styles for Swagger UI
        "img-src 'self' data: https:",
        "font-src 'self'",
        "connect-src 'self'",
        "frame-ancestors 'none'",
        "base-uri 'self'",
        "form-action 'self'",
        "upgrade-insecure-requests" if is_production else ""
    ]
    response.headers["Content-Security-Policy"] = "; ".join(filter(None, csp_directives))

    # Referrer Policy
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

    # Permissions Policy (formerly Feature Policy)
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=(), payment=()"

    # Remove server information
    response.headers.pop("Server", None)

    return response


# Global exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors."""
    log_exception(exc, request)
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Validation error",
            "errors": exc.errors()
        }
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle all unhandled exceptions."""
    log_exception(exc, request)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error",
            "type": type(exc).__name__
        }
    )


# Health check endpoint
@app.get("/api/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "AI Business Assistant API",
        "version": "1.0.0"
    }


# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(documents.router, prefix="/api/documents", tags=["Documents"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])
app.include_router(settings.router, prefix="/api/settings", tags=["Settings"])
app.include_router(tools.router, prefix="/api/tools", tags=["Developer Tools"])


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information."""
    return {
        "message": "AI Business Assistant API",
        "version": "1.0.0",
        "docs": "/api/docs",
        "health": "/api/health"
    }


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv('API_PORT', 8000))

    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )
