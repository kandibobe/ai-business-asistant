"""
Centralized constants for AI Business Assistant.

This module contains all magic numbers, hardcoded values, and configuration constants
used throughout the application. Centralizing constants improves maintainability
and makes it easier to adjust behavior without changing code logic.

Design Principles:
- All constants are UPPERCASE_WITH_UNDERSCORES
- Related constants are grouped together
- Each constant has a descriptive comment
- No logic in this file - only constant definitions
"""

from typing import Dict, List, Set

# ==============================================================================
# FILE PROCESSING LIMITS
# ==============================================================================

# Maximum file sizes (in bytes)
MAX_FILE_SIZE_PDF = 50 * 1024 * 1024  # 50 MB
MAX_FILE_SIZE_EXCEL = 20 * 1024 * 1024  # 20 MB
MAX_FILE_SIZE_WORD = 20 * 1024 * 1024  # 20 MB
MAX_FILE_SIZE_AUDIO = 100 * 1024 * 1024  # 100 MB
MAX_FILE_SIZE_IMAGE = 10 * 1024 * 1024  # 10 MB

# Document processing limits
MAX_DOCUMENT_PAGES = 500  # Maximum pages in PDF
MAX_EXCEL_ROWS = 100000  # Maximum rows in Excel
MAX_EXCEL_SHEETS = 50  # Maximum sheets in Excel workbook
MAX_TEXT_LENGTH = 1000000  # Maximum text length (characters)

# Content length limits
MAX_USER_QUERY_LENGTH = 5000  # Maximum user query length
MAX_AI_RESPONSE_LENGTH = 10000  # Maximum AI response length
MAX_DOCUMENT_TITLE_LENGTH = 200  # Maximum document title length
MAX_FILENAME_LENGTH = 255  # Maximum filename length

# ==============================================================================
# RATE LIMITING
# ==============================================================================

# Rate limits (requests per time period)
RATE_LIMIT_FREE_PER_MINUTE = 10  # Free tier: 10 requests/minute
RATE_LIMIT_FREE_PER_HOUR = 100  # Free tier: 100 requests/hour
RATE_LIMIT_FREE_PER_DAY = 500  # Free tier: 500 requests/day

RATE_LIMIT_PREMIUM_PER_MINUTE = 30  # Premium: 30 requests/minute
RATE_LIMIT_PREMIUM_PER_HOUR = 500  # Premium: 500 requests/hour
RATE_LIMIT_PREMIUM_PER_DAY = 5000  # Premium: 5000 requests/day

# Document limits by tier
MAX_DOCUMENTS_FREE = 10  # Free tier: 10 documents
MAX_DOCUMENTS_PREMIUM = 100  # Premium: 100 documents
MAX_DOCUMENTS_ENTERPRISE = -1  # Enterprise: unlimited (-1)

# ==============================================================================
# CACHE SETTINGS
# ==============================================================================

# Cache TTL (Time To Live) in seconds
CACHE_TTL_AI_RESPONSE = 3600  # 1 hour for AI responses
CACHE_TTL_DOCUMENT_EMBEDDING = 604800  # 7 days for embeddings
CACHE_TTL_USER_SESSION = 86400  # 24 hours for user sessions
CACHE_TTL_HEALTH_CHECK = 60  # 1 minute for health checks
CACHE_TTL_METRICS = 300  # 5 minutes for metrics

# Cache key prefixes
CACHE_KEY_AI_RESPONSE = "ai:response:"
CACHE_KEY_DOCUMENT = "doc:"
CACHE_KEY_USER = "user:"
CACHE_KEY_RATE_LIMIT = "ratelimit:"
CACHE_KEY_SESSION = "session:"

# ==============================================================================
# AI MODEL SETTINGS
# ==============================================================================

# Gemini model names
GEMINI_MODEL_PRO = "gemini-1.5-pro-002"
GEMINI_MODEL_FLASH = "gemini-1.5-flash-002"
GEMINI_MODEL_PRO_VISION = "gemini-1.5-pro-vision-002"

# AI processing parameters
AI_MAX_TOKENS = 8192  # Maximum tokens in response
AI_TEMPERATURE = 0.7  # Temperature for AI responses (0.0-1.0)
AI_TOP_P = 0.95  # Top-p sampling parameter
AI_TOP_K = 40  # Top-k sampling parameter
AI_MAX_CONTEXT_LENGTH = 100000  # Maximum context length

# AI retry settings
AI_MAX_RETRIES = 3  # Maximum API call retries
AI_RETRY_DELAY = 2  # Seconds to wait between retries
AI_RETRY_BACKOFF = 2  # Exponential backoff multiplier

# ==============================================================================
# CELERY TASK SETTINGS
# ==============================================================================

# Task timeouts (seconds)
TASK_TIMEOUT_PDF = 300  # 5 minutes for PDF processing
TASK_TIMEOUT_EXCEL = 300  # 5 minutes for Excel processing
TASK_TIMEOUT_AUDIO = 600  # 10 minutes for audio transcription
TASK_TIMEOUT_WEB = 120  # 2 minutes for web scraping
TASK_TIMEOUT_AI = 120  # 2 minutes for AI processing

# Task retry settings
TASK_MAX_RETRIES = 3  # Maximum task retries
TASK_RETRY_DELAY = 60  # Seconds between retries

# ==============================================================================
# SECURITY SETTINGS
# ==============================================================================

# Allowed file extensions
ALLOWED_EXTENSIONS_DOCUMENT: Set[str] = {'.pdf', '.doc', '.docx', '.txt'}
ALLOWED_EXTENSIONS_SPREADSHEET: Set[str] = {'.xls', '.xlsx', '.csv'}
ALLOWED_EXTENSIONS_AUDIO: Set[str] = {'.mp3', '.wav', '.m4a', '.ogg', '.flac'}
ALLOWED_EXTENSIONS_IMAGE: Set[str] = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
ALLOWED_EXTENSIONS_ALL: Set[str] = (
    ALLOWED_EXTENSIONS_DOCUMENT
    | ALLOWED_EXTENSIONS_SPREADSHEET
    | ALLOWED_EXTENSIONS_AUDIO
    | ALLOWED_EXTENSIONS_IMAGE
)

# MIME types mapping
ALLOWED_MIME_TYPES: Dict[str, List[str]] = {
    'pdf': ['application/pdf'],
    'excel': [
        'application/vnd.ms-excel',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    ],
    'word': [
        'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    ],
    'audio': ['audio/mpeg', 'audio/wav', 'audio/mp4', 'audio/ogg', 'audio/flac'],
    'image': ['image/jpeg', 'image/png', 'image/gif', 'image/webp'],
}

# Security patterns to detect
DANGEROUS_PATTERNS = [
    r"<script[^>]*>.*?</script>",  # XSS
    r"javascript:",  # JavaScript injection
    r"on\w+\s*=",  # Event handlers
    r"';?\s*(DROP|DELETE|INSERT|UPDATE)\s+",  # SQL injection
    r"\$\(['\"].*['\"]\)",  # Command injection
    r"__import__",  # Python import injection
    r"eval\s*\(",  # Eval injection
    r"exec\s*\(",  # Exec injection
]

# Password requirements
PASSWORD_MIN_LENGTH = 8
PASSWORD_MAX_LENGTH = 128
PASSWORD_REQUIRE_UPPERCASE = True
PASSWORD_REQUIRE_LOWERCASE = True
PASSWORD_REQUIRE_DIGIT = True
PASSWORD_REQUIRE_SPECIAL = True

# JWT settings
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 30
JWT_REFRESH_TOKEN_EXPIRE_DAYS = 7
JWT_ALGORITHM = "HS256"

# ==============================================================================
# DATABASE SETTINGS
# ==============================================================================

# Connection pool settings
DB_POOL_SIZE = 10  # Connection pool size
DB_MAX_OVERFLOW = 20  # Max connections beyond pool_size
DB_POOL_TIMEOUT = 30  # Seconds to wait for connection
DB_POOL_RECYCLE = 3600  # Recycle connections after 1 hour

# Query settings
DB_QUERY_TIMEOUT = 30  # Query timeout in seconds
DB_MAX_RESULTS = 1000  # Maximum results per query

# ==============================================================================
# API SETTINGS
# ==============================================================================

# API pagination
API_DEFAULT_PAGE_SIZE = 20  # Default items per page
API_MAX_PAGE_SIZE = 100  # Maximum items per page
API_DEFAULT_PAGE = 1  # Default page number

# API timeouts
API_REQUEST_TIMEOUT = 30  # Request timeout in seconds
API_RESPONSE_TIMEOUT = 60  # Response timeout in seconds

# ==============================================================================
# TELEGRAM BOT SETTINGS
# ==============================================================================

# Message limits
TELEGRAM_MAX_MESSAGE_LENGTH = 4096  # Telegram's limit
TELEGRAM_MAX_CAPTION_LENGTH = 1024  # Telegram's caption limit
TELEGRAM_MESSAGE_CHUNK_SIZE = 3000  # Safe chunk size for long messages

# Keyboard settings
TELEGRAM_MAX_INLINE_BUTTONS = 100  # Max inline keyboard buttons
TELEGRAM_MAX_BUTTON_TEXT_LENGTH = 64  # Max button text length

# File download settings
TELEGRAM_DOWNLOAD_TIMEOUT = 300  # 5 minutes for file download
TELEGRAM_MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB (Telegram bot limit)

# ==============================================================================
# MONITORING & METRICS
# ==============================================================================

# Prometheus metrics labels
METRIC_LABEL_ENDPOINT = "endpoint"
METRIC_LABEL_METHOD = "method"
METRIC_LABEL_STATUS = "status"
METRIC_LABEL_USER_TIER = "user_tier"

# Health check thresholds
HEALTH_CHECK_TIMEOUT = 5  # Seconds for health check
HEALTH_DB_TIMEOUT = 3  # Seconds for database health check
HEALTH_REDIS_TIMEOUT = 2  # Seconds for Redis health check

# Log retention
LOG_RETENTION_DAYS = 30  # Keep logs for 30 days
LOG_MAX_SIZE_MB = 100  # Rotate log file at 100 MB

# ==============================================================================
# WEB SCRAPING
# ==============================================================================

# Web scraping limits
WEB_SCRAPING_TIMEOUT = 30  # Request timeout in seconds
WEB_SCRAPING_MAX_RETRIES = 3  # Maximum retries
WEB_SCRAPING_MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB max content

# User agent
WEB_SCRAPING_USER_AGENT = (
    "Mozilla/5.0 (compatible; AIBusinessBot/1.0; +https://github.com/yourusername/ai-bot)"
)

# Blocked domains (to prevent abuse)
WEB_SCRAPING_BLOCKED_DOMAINS: Set[str] = {
    'localhost',
    '127.0.0.1',
    '0.0.0.0',
    'internal',
}

# ==============================================================================
# AUDIO TRANSCRIPTION
# ==============================================================================

# Whisper API settings
WHISPER_MODEL = "whisper-1"
WHISPER_LANGUAGE = "ru"  # Default language
WHISPER_TEMPERATURE = 0.0  # Temperature for transcription
WHISPER_MAX_FILE_SIZE = 25 * 1024 * 1024  # 25 MB (OpenAI limit)

# ==============================================================================
# EXPORT SETTINGS
# ==============================================================================

# PDF export settings
PDF_PAGE_SIZE = "A4"
PDF_MARGIN_MM = 20  # Margin in millimeters
PDF_FONT_SIZE = 12
PDF_LINE_HEIGHT = 1.5

# Image export settings
IMAGE_DPI = 300  # DPI for image export
IMAGE_QUALITY = 95  # JPEG quality (1-100)

# ==============================================================================
# ERROR MESSAGES (INTERNATIONALIZATION KEYS)
# ==============================================================================

# Error codes
ERROR_CODE_VALIDATION = "VALIDATION_ERROR"
ERROR_CODE_AUTH = "AUTH_ERROR"
ERROR_CODE_NOT_FOUND = "NOT_FOUND"
ERROR_CODE_RATE_LIMIT = "RATE_LIMIT_EXCEEDED"
ERROR_CODE_FILE_TOO_LARGE = "FILE_TOO_LARGE"
ERROR_CODE_INVALID_FILE_TYPE = "INVALID_FILE_TYPE"
ERROR_CODE_AI_ERROR = "AI_SERVICE_ERROR"
ERROR_CODE_DATABASE = "DATABASE_ERROR"
ERROR_CODE_INTERNAL = "INTERNAL_ERROR"

# ==============================================================================
# STATUS CODES
# ==============================================================================

# Document processing status
STATUS_PENDING = "pending"
STATUS_PROCESSING = "processing"
STATUS_COMPLETED = "completed"
STATUS_FAILED = "failed"
STATUS_DELETED = "deleted"

# User status
USER_STATUS_ACTIVE = "active"
USER_STATUS_INACTIVE = "inactive"
USER_STATUS_BANNED = "banned"

# Subscription tiers
TIER_FREE = "free"
TIER_PREMIUM = "premium"
TIER_ENTERPRISE = "enterprise"

# ==============================================================================
# REGEX PATTERNS
# ==============================================================================

# Common regex patterns
PATTERN_EMAIL = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
PATTERN_URL = r'^https?://[^\s/$.?#].[^\s]*$'
PATTERN_PHONE = r'^\+?1?\d{9,15}$'
PATTERN_USERNAME = r'^[a-zA-Z0-9_-]{3,32}$'

# ==============================================================================
# FEATURE FLAGS (can be overridden by settings)
# ==============================================================================

# Default feature flags (can be overridden in settings.py)
FEATURE_AUDIO_TRANSCRIPTION = True
FEATURE_WEB_SCRAPING = True
FEATURE_AI_CACHING = True
FEATURE_METRICS = True
FEATURE_RATE_LIMITING = True
FEATURE_PREMIUM_FEATURES = True

# ==============================================================================
# DEVELOPMENT & DEBUG
# ==============================================================================

# Debug settings
DEBUG_SQL_QUERIES = False  # Log SQL queries
DEBUG_SLOW_QUERY_THRESHOLD = 1.0  # Seconds
DEBUG_LOG_REQUESTS = False  # Log all requests

# ==============================================================================
# USAGE EXAMPLES
# ==============================================================================

if __name__ == "__main__":
    """
    Test constants module.

    Run: python -m config.constants
    """
    print("=" * 80)
    print("📋 AI Business Assistant - Constants Configuration")
    print("=" * 80)

    print("\n📁 File Processing Limits:")
    print(f"   PDF: {MAX_FILE_SIZE_PDF / 1024 / 1024:.0f} MB")
    print(f"   Excel: {MAX_FILE_SIZE_EXCEL / 1024 / 1024:.0f} MB")
    print(f"   Audio: {MAX_FILE_SIZE_AUDIO / 1024 / 1024:.0f} MB")

    print("\n⏱️  Rate Limits (Free Tier):")
    print(f"   Per Minute: {RATE_LIMIT_FREE_PER_MINUTE}")
    print(f"   Per Hour: {RATE_LIMIT_FREE_PER_HOUR}")
    print(f"   Per Day: {RATE_LIMIT_FREE_PER_DAY}")

    print("\n🤖 AI Models:")
    print(f"   Pro: {GEMINI_MODEL_PRO}")
    print(f"   Flash: {GEMINI_MODEL_FLASH}")

    print("\n💾 Cache TTL:")
    print(f"   AI Response: {CACHE_TTL_AI_RESPONSE / 3600:.1f} hours")
    print(f"   Embeddings: {CACHE_TTL_DOCUMENT_EMBEDDING / 86400:.0f} days")

    print("\n📊 Allowed File Types:")
    print(f"   Documents: {', '.join(sorted(ALLOWED_EXTENSIONS_DOCUMENT))}")
    print(f"   Spreadsheets: {', '.join(sorted(ALLOWED_EXTENSIONS_SPREADSHEET))}")
    print(f"   Audio: {', '.join(sorted(ALLOWED_EXTENSIONS_AUDIO))}")

    print("\n" + "=" * 80)
    print("✅ All constants loaded successfully!")
    print("=" * 80)
