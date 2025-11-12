"""
Performance monitoring and debugging utilities.

Provides decorators and context managers for:
- Execution time tracking
- Memory usage monitoring
- Query counting
- Cache hit rate tracking
- Performance profiling
"""
import time
import functools
import logging
from contextlib import contextmanager
from typing import Callable, Any
import psutil
import os

logger = logging.getLogger(__name__)


# ==============================================================================
# Performance Decorators
# ==============================================================================

def timeit(func: Callable) -> Callable:
    """
    Decorator to measure function execution time.

    Usage:
        @timeit
        def slow_function():
            time.sleep(1)
    """
    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            result = await func(*args, **kwargs)
            return result
        finally:
            elapsed = time.perf_counter() - start
            logger.info(
                f"⏱️  {func.__name__} took {elapsed:.3f}s",
                extra={
                    "function": func.__name__,
                    "duration_seconds": elapsed,
                    "performance": True
                }
            )

    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            elapsed = time.perf_counter() - start
            logger.info(
                f"⏱️  {func.__name__} took {elapsed:.3f}s",
                extra={
                    "function": func.__name__,
                    "duration_seconds": elapsed,
                    "performance": True
                }
            )

    # Return appropriate wrapper based on function type
    import inspect
    if inspect.iscoroutinefunction(func):
        return async_wrapper
    return sync_wrapper


def track_memory(func: Callable) -> Callable:
    """
    Decorator to track memory usage of a function.

    Usage:
        @track_memory
        def memory_intensive():
            big_list = [0] * 10000000
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        process = psutil.Process(os.getpid())
        mem_before = process.memory_info().rss / 1024 / 1024  # MB

        result = func(*args, **kwargs)

        mem_after = process.memory_info().rss / 1024 / 1024  # MB
        mem_diff = mem_after - mem_before

        logger.info(
            f"💾 {func.__name__} memory: {mem_before:.1f}MB → {mem_after:.1f}MB (Δ{mem_diff:+.1f}MB)",
            extra={
                "function": func.__name__,
                "memory_before_mb": mem_before,
                "memory_after_mb": mem_after,
                "memory_delta_mb": mem_diff,
                "performance": True
            }
        )

        return result

    return wrapper


def log_performance(threshold_seconds: float = 1.0):
    """
    Decorator that logs warning if function takes longer than threshold.

    Usage:
        @log_performance(threshold_seconds=0.5)
        def should_be_fast():
            time.sleep(1)  # Will log warning
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - start

            if elapsed > threshold_seconds:
                logger.warning(
                    f"⚠️  SLOW: {func.__name__} took {elapsed:.3f}s (threshold: {threshold_seconds}s)",
                    extra={
                        "function": func.__name__,
                        "duration_seconds": elapsed,
                        "threshold_seconds": threshold_seconds,
                        "slow_query": True
                    }
                )

            return result

        return wrapper

    return decorator


# ==============================================================================
# Context Managers
# ==============================================================================

@contextmanager
def timer(operation_name: str):
    """
    Context manager for timing code blocks.

    Usage:
        with timer("database query"):
            results = db.query(User).all()
    """
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        logger.debug(
            f"⏱️  {operation_name}: {elapsed:.3f}s",
            extra={
                "operation": operation_name,
                "duration_seconds": elapsed,
                "performance": True
            }
        )


@contextmanager
def memory_tracker(operation_name: str):
    """
    Context manager for tracking memory usage.

    Usage:
        with memory_tracker("large file processing"):
            data = open("big_file.txt").read()
    """
    process = psutil.Process(os.getpid())
    mem_before = process.memory_info().rss / 1024 / 1024

    try:
        yield
    finally:
        mem_after = process.memory_info().rss / 1024 / 1024
        mem_diff = mem_after - mem_before

        logger.debug(
            f"💾 {operation_name}: {mem_before:.1f}MB → {mem_after:.1f}MB (Δ{mem_diff:+.1f}MB)",
            extra={
                "operation": operation_name,
                "memory_before_mb": mem_before,
                "memory_after_mb": mem_after,
                "memory_delta_mb": mem_diff,
                "performance": True
            }
        )


# ==============================================================================
# Query Counter (for detecting N+1 queries)
# ==============================================================================

class QueryCounter:
    """
    Context manager to count database queries.
    Useful for detecting N+1 query problems.

    Usage:
        with QueryCounter() as counter:
            users = db.query(User).all()
            for user in users:
                print(user.documents)  # N+1 if not eager loaded!

        print(f"Executed {counter.count} queries")
    """

    def __init__(self, warn_threshold: int = 10):
        self.count = 0
        self.warn_threshold = warn_threshold
        self.queries = []

    def __enter__(self):
        # Hook into SQLAlchemy event system
        from sqlalchemy import event
        from sqlalchemy.engine import Engine

        @event.listens_for(Engine, "before_cursor_execute")
        def receive_before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
            self.count += 1
            self.queries.append({
                "statement": statement,
                "parameters": parameters
            })

        self._listener = receive_before_cursor_execute
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        from sqlalchemy import event
        from sqlalchemy.engine import Engine

        # Remove listener
        event.remove(Engine, "before_cursor_execute", self._listener)

        if self.count > self.warn_threshold:
            logger.warning(
                f"⚠️  N+1 QUERY DETECTED: {self.count} queries (threshold: {self.warn_threshold})",
                extra={
                    "query_count": self.count,
                    "threshold": self.warn_threshold,
                    "queries": self.queries[:5]  # Log first 5 queries
                }
            )


# ==============================================================================
# Cache Statistics
# ==============================================================================

class CacheStats:
    """Track cache hit/miss rates."""

    def __init__(self):
        self.hits = 0
        self.misses = 0

    def hit(self):
        self.hits += 1

    def miss(self):
        self.misses += 1

    @property
    def hit_rate(self) -> float:
        total = self.hits + self.misses
        if total == 0:
            return 0.0
        return self.hits / total * 100

    def report(self):
        total = self.hits + self.misses
        logger.info(
            f"📊 Cache Stats: {self.hits} hits, {self.misses} misses ({self.hit_rate:.1f}% hit rate)",
            extra={
                "cache_hits": self.hits,
                "cache_misses": self.misses,
                "cache_hit_rate": self.hit_rate,
                "total_requests": total
            }
        )


# Global cache stats instance
cache_stats = CacheStats()


# ==============================================================================
# Performance Profiler
# ==============================================================================

def profile(output_file: str = "profile.stats"):
    """
    Decorator for CPU profiling.

    Usage:
        @profile(output_file="my_function.stats")
        def expensive_function():
            # code here

    View results:
        python -m pstats my_function.stats
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            import cProfile
            import pstats

            profiler = cProfile.Profile()
            profiler.enable()

            try:
                result = func(*args, **kwargs)
                return result
            finally:
                profiler.disable()

                # Save stats
                profiler.dump_stats(output_file)

                # Print summary
                stats = pstats.Stats(output_file)
                stats.strip_dirs()
                stats.sort_stats('cumulative')

                logger.info(f"📈 Profile saved to {output_file}")
                logger.info("Top 10 functions by cumulative time:")
                stats.print_stats(10)

        return wrapper

    return decorator


# ==============================================================================
# System Resource Monitoring
# ==============================================================================

def get_system_metrics() -> dict:
    """
    Get current system resource usage.

    Returns:
        dict: System metrics including CPU, memory, disk usage
    """
    process = psutil.Process(os.getpid())

    return {
        "cpu_percent": process.cpu_percent(interval=0.1),
        "memory_mb": process.memory_info().rss / 1024 / 1024,
        "memory_percent": process.memory_percent(),
        "num_threads": process.num_threads(),
        "num_fds": process.num_fds() if hasattr(process, 'num_fds') else None,
        "system_cpu_percent": psutil.cpu_percent(interval=0.1),
        "system_memory_percent": psutil.virtual_memory().percent,
        "system_disk_percent": psutil.disk_usage('/').percent
    }


def log_system_metrics():
    """Log current system metrics."""
    metrics = get_system_metrics()
    logger.info(
        f"💻 System: CPU {metrics['cpu_percent']:.1f}%, "
        f"Memory {metrics['memory_mb']:.1f}MB ({metrics['memory_percent']:.1f}%), "
        f"Threads {metrics['num_threads']}",
        extra=metrics
    )


# ==============================================================================
# Example Usage
# ==============================================================================

if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(level=logging.DEBUG)

    # Example 1: Time a function
    @timeit
    def slow_function():
        time.sleep(0.5)
        return "done"

    slow_function()

    # Example 2: Track memory
    @track_memory
    def memory_intensive():
        big_list = [0] * 1000000
        return len(big_list)

    memory_intensive()

    # Example 3: Context manager
    with timer("custom operation"):
        time.sleep(0.1)

    # Example 4: Log system metrics
    log_system_metrics()
