"""
AI response caching using Redis.
Reduces AI API costs and improves response times.
"""
import hashlib
import json
import logging
from typing import Optional, Dict, Any
import redis
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# Redis connection with optimized pooling
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
try:
    # Create connection pool for better performance
    redis_pool = redis.ConnectionPool.from_url(
        REDIS_URL,
        decode_responses=True,
        max_connections=50,  # Max concurrent connections
        socket_keepalive=True,  # Keep connections alive
        socket_connect_timeout=5,  # 5 second connection timeout
        socket_timeout=5,  # 5 second operation timeout
        retry_on_timeout=True,  # Retry on timeout
        health_check_interval=30,  # Check connection health every 30s
    )

    redis_client = redis.Redis(connection_pool=redis_pool)
    redis_client.ping()  # Test connection
    logger.info(f"✅ Connected to Redis at {REDIS_URL} with connection pool (max: 50)")
except Exception as e:
    logger.warning(f"⚠️ Redis connection failed: {e}. Caching will be disabled.")
    redis_client = None
    redis_pool = None


class AIResponseCache:
    """Cache for AI responses to reduce costs and improve performance."""

    def __init__(
        self,
        ttl: int = 3600,  # 1 hour default TTL
        namespace: str = "ai_chat"
    ):
        """
        Initialize AI response cache.

        Args:
            ttl: Time-to-live in seconds (default 1 hour)
            namespace: Cache key namespace
        """
        self.ttl = ttl
        self.namespace = namespace
        self.client = redis_client

    def _generate_cache_key(self, prompt: str, model: str = "gemini") -> str:
        """
        Generate a unique cache key for a prompt.

        Uses SHA-256 hash of prompt + model to create consistent keys.

        Args:
            prompt: The AI prompt
            model: Model name

        Returns:
            Cache key string
        """
        # Normalize prompt (strip whitespace, lowercase)
        normalized = prompt.strip().lower()

        # Create hash
        hash_input = f"{model}:{normalized}".encode('utf-8')
        hash_digest = hashlib.sha256(hash_input).hexdigest()

        # Return namespaced key
        return f"{self.namespace}:{hash_digest}"

    def get(self, prompt: str, model: str = "gemini") -> Optional[Dict[str, Any]]:
        """
        Get cached AI response for a prompt.

        Args:
            prompt: The AI prompt
            model: Model name

        Returns:
            Cached response dict or None if not found
        """
        if not self.client:
            return None

        try:
            key = self._generate_cache_key(prompt, model)
            cached_data = self.client.get(key)

            if cached_data:
                logger.info(f"Cache HIT for prompt hash: {key}")
                data = json.loads(cached_data)
                return data
            else:
                logger.debug(f"Cache MISS for prompt hash: {key}")
                return None

        except Exception as e:
            logger.error(f"Cache get error: {e}")
            return None

    def set(
        self,
        prompt: str,
        response: Dict[str, Any],
        model: str = "gemini",
        ttl: Optional[int] = None
    ) -> bool:
        """
        Cache an AI response.

        Args:
            prompt: The AI prompt
            response: Response data to cache
            model: Model name
            ttl: Optional custom TTL (uses default if not provided)

        Returns:
            True if cached successfully, False otherwise
        """
        if not self.client:
            return False

        try:
            key = self._generate_cache_key(prompt, model)
            ttl = ttl or self.ttl

            # Add metadata
            cache_data = {
                **response,
                "_cached_at": self._get_timestamp(),
                "_ttl": ttl,
            }

            # Store in Redis with TTL
            self.client.setex(
                key,
                ttl,
                json.dumps(cache_data)
            )

            logger.info(f"Cached response for {key} (TTL: {ttl}s)")
            return True

        except Exception as e:
            logger.error(f"Cache set error: {e}")
            return False

    def delete(self, prompt: str, model: str = "gemini") -> bool:
        """
        Delete a cached response.

        Args:
            prompt: The AI prompt
            model: Model name

        Returns:
            True if deleted, False otherwise
        """
        if not self.client:
            return False

        try:
            key = self._generate_cache_key(prompt, model)
            deleted = self.client.delete(key)
            logger.info(f"Deleted cache key: {key}")
            return bool(deleted)

        except Exception as e:
            logger.error(f"Cache delete error: {e}")
            return False

    def clear_all(self) -> int:
        """
        Clear all cached responses in this namespace.

        Returns:
            Number of keys deleted
        """
        if not self.client:
            return 0

        try:
            pattern = f"{self.namespace}:*"
            keys = self.client.keys(pattern)

            if keys:
                deleted = self.client.delete(*keys)
                logger.info(f"Cleared {deleted} cache keys")
                return deleted

            return 0

        except Exception as e:
            logger.error(f"Cache clear error: {e}")
            return 0

    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.

        Returns:
            Dict with cache statistics
        """
        if not self.client:
            return {"enabled": False}

        try:
            pattern = f"{self.namespace}:*"
            keys = self.client.keys(pattern)

            total_size = 0
            for key in keys:
                value = self.client.get(key)
                if value:
                    total_size += len(value.encode('utf-8'))

            return {
                "enabled": True,
                "total_keys": len(keys),
                "total_size_bytes": total_size,
                "total_size_kb": round(total_size / 1024, 2),
                "namespace": self.namespace,
            }

        except Exception as e:
            logger.error(f"Cache stats error: {e}")
            return {"enabled": True, "error": str(e)}

    @staticmethod
    def _get_timestamp() -> str:
        """Get current UTC timestamp in ISO format."""
        from datetime import datetime
        return datetime.utcnow().isoformat()


# Global cache instance for AI chat
ai_chat_cache = AIResponseCache(
    ttl=int(os.getenv('AI_CACHE_TTL', 3600)),  # 1 hour default
    namespace="ai_chat"
)


# Decorator for caching function results
def cached_ai_call(ttl: Optional[int] = None):
    """
    Decorator to cache AI function calls.

    Usage:
        @cached_ai_call(ttl=7200)
        def my_ai_function(prompt: str) -> dict:
            return gemini_model.generate_content(prompt)
    """
    def decorator(func):
        def wrapper(prompt: str, *args, **kwargs):
            # Try to get from cache
            cached = ai_chat_cache.get(prompt)
            if cached:
                return cached

            # Call function
            result = func(prompt, *args, **kwargs)

            # Cache result
            ai_chat_cache.set(prompt, result, ttl=ttl)

            return result

        return wrapper
    return decorator


if __name__ == "__main__":
    # Test cache
    cache = AIResponseCache()

    # Test set/get
    test_prompt = "What is the capital of France?"
    test_response = {"message": "Paris", "response_time_ms": 1200}

    print(f"Setting cache: {cache.set(test_prompt, test_response)}")
    print(f"Getting cache: {cache.get(test_prompt)}")

    # Test stats
    print(f"Cache stats: {cache.get_stats()}")

    # Test clear
    print(f"Cleared: {cache.clear_all()} keys")
