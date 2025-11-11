"""
Pydantic Settings for environment configuration with validation.

This module provides type-safe configuration loading with automatic validation
at startup. If any required environment variables are missing or invalid,
the application will fail fast with clear error messages.
"""
import os
from typing import Optional, List
from pydantic import Field, field_validator, ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Pydantic will automatically:
    - Load values from .env file
    - Validate types and constraints
    - Fail fast if required variables are missing
    - Provide clear error messages
    """

    # ==================== Telegram Configuration ====================
    telegram_bot_token: str = Field(
        ...,
        description="Telegram Bot Token from @BotFather",
        min_length=40
    )

    # ==================== AI Configuration ====================
    gemini_api_key: str = Field(
        ...,
        description="Google Gemini API Key",
        min_length=20
    )

    openai_api_key: Optional[str] = Field(
        None,
        description="OpenAI API Key for Whisper transcription (optional)",
        min_length=20
    )

    gemini_model_name: str = Field(
        default="gemini-1.5-pro-002",
        description="Gemini model to use for AI responses"
    )

    gemini_flash_model: str = Field(
        default="gemini-1.5-flash-002",
        description="Fast Gemini model for simple queries"
    )

    # ==================== Database Configuration ====================
    db_host: str = Field(
        default="localhost",
        description="PostgreSQL host"
    )

    db_port: int = Field(
        default=5432,
        ge=1,
        le=65535,
        description="PostgreSQL port"
    )

    db_user: str = Field(
        ...,
        min_length=1,
        description="PostgreSQL username"
    )

    db_pass: str = Field(
        ...,
        min_length=1,
        description="PostgreSQL password"
    )

    db_name: str = Field(
        ...,
        min_length=1,
        description="PostgreSQL database name"
    )

    @property
    def database_url(self) -> str:
        """Construct PostgreSQL connection URL."""
        return f"postgresql://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"

    @property
    def async_database_url(self) -> str:
        """Construct async PostgreSQL connection URL."""
        return f"postgresql+asyncpg://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"

    # ==================== Redis Configuration ====================
    redis_url: str = Field(
        default="redis://localhost:6379/0",
        description="Redis connection URL"
    )

    ai_cache_ttl: int = Field(
        default=3600,
        ge=0,
        description="AI response cache TTL in seconds"
    )

    # ==================== Logging Configuration ====================
    log_level: str = Field(
        default="INFO",
        description="Logging level"
    )

    log_file: Optional[str] = Field(
        None,
        description="Optional log file path"
    )

    json_logs: bool = Field(
        default=False,
        description="Use JSON format for logs (production)"
    )

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level."""
        allowed = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        v_upper = v.upper()
        if v_upper not in allowed:
            raise ValueError(f"Log level must be one of: {', '.join(allowed)}")
        return v_upper

    # ==================== API Configuration ====================
    api_port: int = Field(
        default=8000,
        ge=1024,
        le=65535,
        description="FastAPI server port"
    )

    jwt_secret_key: str = Field(
        ...,
        min_length=32,
        description="JWT secret key for authentication"
    )

    jwt_algorithm: str = Field(
        default="HS256",
        description="JWT signing algorithm"
    )

    jwt_access_token_expire_minutes: int = Field(
        default=30,
        ge=1,
        description="JWT access token expiration in minutes"
    )

    jwt_refresh_token_expire_days: int = Field(
        default=7,
        ge=1,
        description="JWT refresh token expiration in days"
    )

    allowed_origins: str = Field(
        default="http://localhost:5173,http://localhost:3000",
        description="Comma-separated list of allowed CORS origins"
    )

    @property
    def cors_origins(self) -> List[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.allowed_origins.split(",") if origin.strip()]

    # ==================== Security Configuration ====================
    max_file_size_mb: int = Field(
        default=50,
        ge=1,
        le=500,
        description="Maximum file upload size in MB"
    )

    rate_limit_per_minute: int = Field(
        default=30,
        ge=1,
        description="API rate limit per minute for free users"
    )

    rate_limit_per_minute_premium: int = Field(
        default=100,
        ge=1,
        description="API rate limit per minute for premium users"
    )

    # ==================== Feature Flags ====================
    enable_audio_transcription: bool = Field(
        default=True,
        description="Enable audio transcription feature"
    )

    enable_web_scraping: bool = Field(
        default=True,
        description="Enable web page scraping feature"
    )

    enable_ai_caching: bool = Field(
        default=True,
        description="Enable AI response caching"
    )

    enable_metrics: bool = Field(
        default=True,
        description="Enable Prometheus metrics"
    )

    # ==================== Monitoring ====================
    sentry_dsn: Optional[str] = Field(
        None,
        description="Sentry DSN for error tracking (optional)"
    )

    environment: str = Field(
        default="development",
        description="Environment name (development, staging, production)"
    )

    @field_validator("environment")
    @classmethod
    def validate_environment(cls, v: str) -> str:
        """Validate environment."""
        allowed = ["development", "staging", "production"]
        v_lower = v.lower()
        if v_lower not in allowed:
            raise ValueError(f"Environment must be one of: {', '.join(allowed)}")
        return v_lower

    # ==================== Performance Tuning ====================
    celery_worker_concurrency: int = Field(
        default=4,
        ge=1,
        description="Number of Celery worker processes"
    )

    celery_task_time_limit: int = Field(
        default=300,
        ge=30,
        description="Celery task time limit in seconds"
    )

    max_context_length: int = Field(
        default=100000,
        ge=1000,
        description="Maximum context length for AI processing"
    )

    # Pydantic v2 configuration
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"  # Ignore extra fields in .env
    )


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """
    Get the global settings instance (singleton pattern).

    This will load and validate settings on first call.
    Subsequent calls return the cached instance.

    Returns:
        Settings: Validated settings instance

    Raises:
        ValidationError: If environment variables are invalid or missing
    """
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


def reload_settings() -> Settings:
    """
    Force reload settings from environment.

    Useful for testing or dynamic configuration updates.

    Returns:
        Settings: New validated settings instance
    """
    global _settings
    _settings = Settings()
    return _settings


# Convenience function for checking if in production
def is_production() -> bool:
    """Check if running in production environment."""
    return get_settings().environment == "production"


def is_development() -> bool:
    """Check if running in development environment."""
    return get_settings().environment == "development"


# Example usage and validation
if __name__ == "__main__":
    """
    Test settings validation.

    Run this to check if your .env file is correctly configured:
        python -m config.settings
    """
    print("=" * 60)
    print("🔧 Testing Configuration Validation")
    print("=" * 60)

    try:
        settings = get_settings()

        print("\n✅ Configuration loaded successfully!\n")
        print("📊 Configuration Summary:")
        print(f"   Environment: {settings.environment}")
        print(f"   Log Level: {settings.log_level}")
        print(f"   Database: {settings.db_host}:{settings.db_port}/{settings.db_name}")
        print(f"   Redis: {settings.redis_url}")
        print(f"   API Port: {settings.api_port}")
        print(f"   Gemini Model: {settings.gemini_model_name}")
        print(f"   OpenAI Configured: {'Yes' if settings.openai_api_key else 'No'}")
        print(f"   JSON Logs: {'Enabled' if settings.json_logs else 'Disabled'}")
        print(f"   CORS Origins: {settings.cors_origins}")
        print(f"   Sentry: {'Enabled' if settings.sentry_dsn else 'Disabled'}")

        print("\n🔒 Security Settings:")
        print(f"   Max File Size: {settings.max_file_size_mb} MB")
        print(f"   Rate Limit (Free): {settings.rate_limit_per_minute}/min")
        print(f"   Rate Limit (Premium): {settings.rate_limit_per_minute_premium}/min")

        print("\n🎛️  Feature Flags:")
        print(f"   Audio Transcription: {'✓' if settings.enable_audio_transcription else '✗'}")
        print(f"   Web Scraping: {'✓' if settings.enable_web_scraping else '✗'}")
        print(f"   AI Caching: {'✓' if settings.enable_ai_caching else '✗'}")
        print(f"   Metrics: {'✓' if settings.enable_metrics else '✗'}")

        print("\n" + "=" * 60)
        print("✅ All settings validated successfully!")
        print("=" * 60)

    except Exception as e:
        print("\n" + "=" * 60)
        print("❌ Configuration Validation Failed!")
        print("=" * 60)
        print(f"\nError: {e}")
        print("\n💡 Tips:")
        print("   1. Make sure .env file exists (copy from .env.example)")
        print("   2. Check that all required variables are set")
        print("   3. Verify variable types and formats")
        print("   4. See .env.example for reference")
        print("=" * 60)
        exit(1)
