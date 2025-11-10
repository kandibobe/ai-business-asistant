"""
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
        """
        Increment a counter metric.

        Args:
            metric_name: Name of the metric
            value: Amount to increment (default 1)
            tags: Optional tags for the metric
        """
        with self.lock:
            key = self._make_key(metric_name, tags)
            self.counters[key] += value

    def timing(self, metric_name: str, duration_ms: float, tags: Optional[Dict[str, str]] = None):
        """
        Record a timing metric.

        Args:
            metric_name: Name of the metric
            duration_ms: Duration in milliseconds
            tags: Optional tags for the metric
        """
        with self.lock:
            key = self._make_key(metric_name, tags)
            self.timers[key].append(duration_ms)

            # Keep only last 1000 measurements to prevent memory issues
            if len(self.timers[key]) > 1000:
                self.timers[key] = self.timers[key][-1000:]

    def gauge(self, metric_name: str, value: float, tags: Optional[Dict[str, str]] = None):
        """
        Set a gauge metric (current value).

        Args:
            metric_name: Name of the metric
            value: Current value
            tags: Optional tags for the metric
        """
        with self.lock:
            key = self._make_key(metric_name, tags)
            self.gauges[key] = value

    def get_counter(self, metric_name: str, tags: Optional[Dict[str, str]] = None) -> int:
        """Get counter value."""
        key = self._make_key(metric_name, tags)
        return self.counters.get(key, 0)

    def get_timer_stats(self, metric_name: str, tags: Optional[Dict[str, str]] = None) -> Dict[str, float]:
        """
        Get timer statistics.

        Returns:
            Dict with min, max, avg, p95, p99
        """
        key = self._make_key(metric_name, tags)
        timings = self.timers.get(key, [])

        if not timings:
            return {
                "count": 0,
                "min": 0,
                "max": 0,
                "avg": 0,
                "p50": 0,
                "p95": 0,
                "p99": 0,
            }

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

    def get_gauge(self, metric_name: str, tags: Optional[Dict[str, str]] = None) -> Optional[float]:
        """Get gauge value."""
        key = self._make_key(metric_name, tags)
        return self.gauges.get(key)

    def get_all_metrics(self) -> Dict[str, Any]:
        """
        Get all collected metrics.

        Returns:
            Dict with all metrics and their values
        """
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
            logger.info("All metrics reset")

    @staticmethod
    def _make_key(metric_name: str, tags: Optional[Dict[str, str]] = None) -> str:
        """Create unique key from metric name and tags."""
        if not tags:
            return metric_name

        tag_str = ",".join(f"{k}={v}" for k, v in sorted(tags.items()))
        return f"{metric_name}:{tag_str}"


class Timer:
    """Context manager for timing code blocks."""

    def __init__(self, metric_name: str, collector: MetricsCollector, tags: Optional[Dict[str, str]] = None):
        """
        Initialize timer.

        Args:
            metric_name: Name of the metric
            collector: MetricsCollector instance
            tags: Optional tags
        """
        self.metric_name = metric_name
        self.collector = collector
        self.tags = tags
        self.start_time = None

    def __enter__(self):
        """Start timer."""
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Stop timer and record metric."""
        if self.start_time:
            duration_ms = (time.time() - self.start_time) * 1000
            self.collector.timing(self.metric_name, duration_ms, self.tags)


# Global metrics collector
metrics = MetricsCollector()


def track_message_handled(user_id: int, message_type: str):
    """Track message handled."""
    metrics.increment("messages.handled", tags={"type": message_type})
    metrics.increment(f"users.{user_id}.messages")


def track_ai_request(user_id: int, duration_ms: float, cached: bool):
    """Track AI request."""
    metrics.increment("ai.requests", tags={"cached": str(cached)})
    metrics.timing("ai.response_time", duration_ms, tags={"cached": str(cached)})
    metrics.increment(f"users.{user_id}.ai_requests")


def track_document_processed(user_id: int, doc_type: str, success: bool):
    """Track document processing."""
    metrics.increment("documents.processed", tags={"type": doc_type, "success": str(success)})
    if success:
        metrics.increment(f"users.{user_id}.documents")


def track_error(error_type: str, handler: str):
    """Track error occurrence."""
    metrics.increment("errors", tags={"type": error_type, "handler": handler})


def track_cache_operation(operation: str, hit: bool):
    """Track cache operation."""
    metrics.increment(f"cache.{operation}", tags={"hit": str(hit)})


def get_metrics_summary() -> Dict[str, Any]:
    """
    Get summary of all metrics.

    Returns:
        Dict with metrics summary
    """
    return metrics.get_all_metrics()


def track_startup_time(duration_ms: float):
    """Track bot startup time."""
    metrics.timing("bot.startup_time", duration_ms)
    logger.info(f"Bot startup completed in {duration_ms:.2f}ms")


if __name__ == "__main__":
    # Test metrics
    import json

    # Track some test metrics
    metrics.increment("test.counter")
    metrics.increment("test.counter")
    metrics.increment("test.counter")

    metrics.gauge("test.gauge", 42.5)

    with Timer("test.timer", metrics):
        time.sleep(0.1)

    with Timer("test.timer", metrics):
        time.sleep(0.05)

    # Print metrics
    print(json.dumps(get_metrics_summary(), indent=2))
