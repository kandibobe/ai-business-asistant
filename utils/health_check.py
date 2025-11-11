"""
Health check module for monitoring bot and service status.
"""
import logging
from typing import Dict, Any, Optional
from datetime import datetime
import time
from sqlalchemy import text

logger = logging.getLogger(__name__)


class HealthCheck:
    """Monitor health of all bot services."""

    def __init__(self):
        """Initialize health check."""
        self.start_time = time.time()
        self.last_check = None
        self.status_history = []

    def check_database(self) -> Dict[str, Any]:
        """
        Check database connection health.

        Returns:
            Dict with status and details
        """
        try:
            from database.database import engine

            with engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                result.fetchone()

            return {
                "status": "healthy",
                "message": "Database connection OK",
                "response_time_ms": self._measure_db_latency()
            }
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return {
                "status": "unhealthy",
                "message": f"Database error: {str(e)}",
                "response_time_ms": None
            }

    def check_redis(self) -> Dict[str, Any]:
        """
        Check Redis connection health.

        Returns:
            Dict with status and details
        """
        try:
            from utils.cache import redis_client

            if not redis_client:
                return {
                    "status": "disabled",
                    "message": "Redis client not initialized",
                    "response_time_ms": None
                }

            start = time.time()
            redis_client.ping()
            latency = (time.time() - start) * 1000

            return {
                "status": "healthy",
                "message": "Redis connection OK",
                "response_time_ms": round(latency, 2)
            }
        except Exception as e:
            logger.error(f"Redis health check failed: {e}")
            return {
                "status": "unhealthy",
                "message": f"Redis error: {str(e)}",
                "response_time_ms": None
            }

    def check_ai_service(self) -> Dict[str, Any]:
        """
        Check AI service availability.

        Returns:
            Dict with status and details
        """
        try:
            import google.generativeai as genai
            from config import GEMINI_MODEL_NAME
            import os

            gemini_api_key = os.getenv('GEMINI_API_KEY')
            if not gemini_api_key:
                return {
                    "status": "misconfigured",
                    "message": "GEMINI_API_KEY not set",
                    "response_time_ms": None
                }

            # Just check configuration, don't make actual API call
            # (to avoid costs on health checks)
            return {
                "status": "configured",
                "message": f"AI model configured: {GEMINI_MODEL_NAME}",
                "response_time_ms": None
            }
        except Exception as e:
            logger.error(f"AI service health check failed: {e}")
            return {
                "status": "error",
                "message": f"AI configuration error: {str(e)}",
                "response_time_ms": None
            }

    def _measure_db_latency(self) -> Optional[float]:
        """
        Measure database query latency.

        Returns:
            Latency in milliseconds or None if error
        """
        try:
            from database.database import engine

            start = time.time()
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            latency = (time.time() - start) * 1000
            return round(latency, 2)
        except Exception:
            return None

    def get_system_info(self) -> Dict[str, Any]:
        """
        Get system information.

        Returns:
            Dict with system stats
        """
        import psutil
        import sys

        uptime_seconds = int(time.time() - self.start_time)

        return {
            "uptime_seconds": uptime_seconds,
            "uptime_human": self._format_uptime(uptime_seconds),
            "python_version": sys.version.split()[0],
            "cpu_percent": psutil.cpu_percent(interval=0.1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage('/').percent,
        }

    def get_full_status(self) -> Dict[str, Any]:
        """
        Get complete health status of all services.

        Returns:
            Dict with full health status
        """
        self.last_check = datetime.utcnow()

        db_health = self.check_database()
        redis_health = self.check_redis()
        ai_health = self.check_ai_service()

        # Overall status
        all_healthy = (
            db_health["status"] == "healthy" and
            redis_health["status"] in ["healthy", "disabled"] and
            ai_health["status"] in ["configured", "healthy"]
        )

        status = {
            "timestamp": self.last_check.isoformat(),
            "status": "healthy" if all_healthy else "degraded",
            "services": {
                "database": db_health,
                "redis": redis_health,
                "ai_service": ai_health,
            },
            "system": self.get_system_info(),
        }

        # Store in history (keep last 10)
        self.status_history.append(status)
        if len(self.status_history) > 10:
            self.status_history.pop(0)

        return status

    def _format_uptime(self, seconds: int) -> str:
        """
        Format uptime in human-readable format.

        Args:
            seconds: Uptime in seconds

        Returns:
            Formatted string like "2d 3h 45m"
        """
        days = seconds // 86400
        hours = (seconds % 86400) // 3600
        minutes = (seconds % 3600) // 60

        parts = []
        if days > 0:
            parts.append(f"{days}d")
        if hours > 0:
            parts.append(f"{hours}h")
        if minutes > 0 or not parts:
            parts.append(f"{minutes}m")

        return " ".join(parts)

    def is_healthy(self) -> bool:
        """
        Quick health check.

        Returns:
            True if all critical services are healthy
        """
        status = self.get_full_status()
        return status["status"] == "healthy"


# Global health check instance
health_checker = HealthCheck()


def get_health_status() -> Dict[str, Any]:
    """
    Get current health status.

    Returns:
        Health status dict
    """
    return health_checker.get_full_status()


def is_system_healthy() -> bool:
    """
    Quick health check.

    Returns:
        True if system is healthy
    """
    return health_checker.is_healthy()


if __name__ == "__main__":
    # Test health check
    import json

    print("Running health check...")
    status = get_health_status()
    print(json.dumps(status, indent=2))

    print(f"\nSystem healthy: {is_system_healthy()}")
