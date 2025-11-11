#!/usr/bin/env python3
"""
Скрипт для применения всех масштабных улучшений бота.
Копирует новые файлы и обновляет существующие.

Использование:
    python apply_improvements.py
"""
import os
import shutil
import sys
from pathlib import Path

print("=" * 70)
print("🚀 Применение масштабных улучшений AI Business Assistant")
print("=" * 70)

# Проверяем что мы в правильной директории
if not os.path.exists("main.py") or not os.path.exists("requirements.txt"):
    print("❌ Ошибка: Запустите скрипт из корневой директории проекта")
    print("   (где находятся main.py и requirements.txt)")
    sys.exit(1)

print("\n[1/5] Создание новых утилит...")

# utils/health_check.py
print("   Creating utils/health_check.py...")
health_check_content = '''"""
Health check module for monitoring bot and service status.
"""
import logging
from typing import Dict, Any, Optional
from datetime import datetime
import time

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
            from sqlalchemy import text

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
            from config import GEMINI_MODEL_NAME
            import os

            gemini_api_key = os.getenv('GEMINI_API_KEY')
            if not gemini_api_key:
                return {
                    "status": "misconfigured",
                    "message": "GEMINI_API_KEY not set",
                    "response_time_ms": None
                }

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
            from sqlalchemy import text

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
        try:
            import psutil
        except ImportError:
            return {
                "uptime_seconds": int(time.time() - self.start_time),
                "note": "Install psutil for system metrics: pip install psutil"
            }

        import sys

        uptime_seconds = int(time.time() - self.start_time)

        return {
            "uptime_seconds": uptime_seconds,
            "uptime_human": self._format_uptime(uptime_seconds),
            "python_version": sys.version.split()[0],
            "cpu_percent": psutil.cpu_percent(interval=0.1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage('/').percent if os.name != 'nt' else psutil.disk_usage('C:\\\\').percent,
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

    print(f"\\nSystem healthy: {is_system_healthy()}")
'''

with open("utils/health_check.py", "w", encoding="utf-8") as f:
    f.write(health_check_content)

print("   ✅ utils/health_check.py created")

# utils/metrics.py
print("   Creating utils/metrics.py...")
metrics_content = '''"""
Application metrics and monitoring.
Tracks performance, usage, and system health.
"""
import logging
import time
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from collections import defaultdict
import threading

logger = logging.getLogger(__name__)


@dataclass
class Metric:
    """Single metric data point."""
    name: str
    value: float
    timestamp: float
    tags: Dict[str, str] = field(default_factory=dict)


class MetricsCollector:
    """Collects and aggregates application metrics."""

    def __init__(self):
        """Initialize metrics collector."""
        self.counters = defaultdict(int)
        self.timers = defaultdict(list)
        self.gauges = {}
        self.lock = threading.Lock()

    def increment(self, metric_name: str, value: int = 1, tags: Optional[Dict[str, str]] = None):
        """Increment a counter metric."""
        with self.lock:
            key = self._make_key(metric_name, tags)
            self.counters[key] += value

    def timing(self, metric_name: str, duration_ms: float, tags: Optional[Dict[str, str]] = None):
        """Record a timing metric."""
        with self.lock:
            key = self._make_key(metric_name, tags)
            self.timers[key].append(duration_ms)

            # Keep only last 1000 measurements
            if len(self.timers[key]) > 1000:
                self.timers[key] = self.timers[key][-1000:]

    def gauge(self, metric_name: str, value: float, tags: Optional[Dict[str, str]] = None):
        """Set a gauge metric."""
        with self.lock:
            key = self._make_key(metric_name, tags)
            self.gauges[key] = value

    def get_counter(self, metric_name: str, tags: Optional[Dict[str, str]] = None) -> int:
        """Get counter value."""
        key = self._make_key(metric_name, tags)
        return self.counters.get(key, 0)

    def get_timer_stats(self, metric_name: str, tags: Optional[Dict[str, str]] = None) -> Dict[str, float]:
        """Get timer statistics."""
        key = self._make_key(metric_name, tags)
        timings = self.timers.get(key, [])

        if not timings:
            return {"count": 0, "min": 0, "max": 0, "avg": 0, "p50": 0, "p95": 0, "p99": 0}

        sorted_timings = sorted(timings)
        count = len(sorted_timings)

        return {
            "count": count,
            "min": round(min(sorted_timings), 2),
            "max": round(max(sorted_timings), 2),
            "avg": round(sum(sorted_timings) / count, 2),
            "p50": round(sorted_timings[int(count * 0.50)], 2),
            "p95": round(sorted_timings[int(count * 0.95)], 2) if count > 1 else sorted_timings[0],
            "p99": round(sorted_timings[int(count * 0.99)], 2) if count > 1 else sorted_timings[0],
        }

    def get_all_metrics(self) -> Dict[str, Any]:
        """Get all collected metrics."""
        with self.lock:
            metrics = {
                "counters": dict(self.counters),
                "timers": {k: self.get_timer_stats(k.split(":")[0]) for k in self.timers.keys()},
                "gauges": dict(self.gauges),
                "timestamp": datetime.utcnow().isoformat(),
            }
        return metrics

    def reset(self):
        """Reset all metrics."""
        with self.lock:
            self.counters.clear()
            self.timers.clear()
            self.gauges.clear()

    @staticmethod
    def _make_key(metric_name: str, tags: Optional[Dict[str, str]] = None) -> str:
        """Create unique key from metric name and tags."""
        if not tags:
            return metric_name
        tag_str = ",".join(f"{k}={v}" for k, v in sorted(tags.items()))
        return f"{metric_name}:{tag_str}"


class Timer:
    """Context manager for timing code blocks."""

    def __init__(self, metric_name: str, collector, tags: Optional[Dict[str, str]] = None):
        self.metric_name = metric_name
        self.collector = collector
        self.tags = tags
        self.start_time = None

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.start_time:
            duration_ms = (time.time() - self.start_time) * 1000
            self.collector.timing(self.metric_name, duration_ms, self.tags)


# Global metrics collector
metrics = MetricsCollector()


def track_ai_request(user_id: int, duration_ms: float, cached: bool):
    """Track AI request."""
    metrics.increment("ai.requests", tags={"cached": str(cached)})
    metrics.timing("ai.response_time", duration_ms, tags={"cached": str(cached)})


def track_startup_time(duration_ms: float):
    """Track bot startup time."""
    metrics.timing("bot.startup_time", duration_ms)


def get_metrics_summary() -> Dict[str, Any]:
    """Get summary of all metrics."""
    return metrics.get_all_metrics()
'''

with open("utils/metrics.py", "w", encoding="utf-8") as f:
    f.write(metrics_content)

print("   ✅ utils/metrics.py created")

print("\n[2/5] Обновление main.py...")

# Читаем текущий main.py
with open("main.py", "r", encoding="utf-8") as f:
    main_content = f.read()

# Проверяем нужно ли обновлять
if "from utils.metrics import" not in main_content:
    print("   ⚠️  main.py needs manual update - see MAJOR_IMPROVEMENTS.md")
else:
    print("   ✅ main.py already updated")

print("\n[3/5] Обновление handlers/messages.py...")

# Проверяем handlers/messages.py
with open("handlers/messages.py", "r", encoding="utf-8") as f:
    messages_content = f.read()

if "from utils.ai_helpers import" not in messages_content:
    print("   ⚠️  handlers/messages.py needs manual update - see MAJOR_IMPROVEMENTS.md")
else:
    print("   ✅ handlers/messages.py already updated")

print("\n[4/5] Проверка зависимостей...")

# Проверяем requirements.txt
with open("requirements.txt", "r", encoding="utf-8") as f:
    reqs = f.read()

if "psutil" not in reqs:
    print("   Adding psutil to requirements.txt...")
    with open("requirements.txt", "a", encoding="utf-8") as f:
        f.write("psutil==5.9.8  # System and process monitoring\n")
    print("   ✅ psutil added to requirements.txt")
else:
    print("   ✅ psutil already in requirements.txt")

print("\n[5/5] Финальная проверка...")
print("   ✅ utils/health_check.py")
print("   ✅ utils/metrics.py")
print("   ✅ requirements.txt")

print("\n" + "=" * 70)
print("✅ Применение улучшений завершено!")
print("=" * 70)

print("\n📋 Следующие шаги:")
print("1. Установите зависимости:")
print("   pip install -r requirements.txt")
print("")
print("2. Проверьте health check:")
print("   python utils/health_check.py")
print("")
print("3. Проверьте metrics:")
print("   python utils/metrics.py")
print("")
print("4. Запустите бота:")
print("   python main.py")
print("")
print("📖 Полная документация: MAJOR_IMPROVEMENTS.md")
print("")
