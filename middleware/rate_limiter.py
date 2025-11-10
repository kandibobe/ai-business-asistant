"""
Rate limiting middleware using Redis.
Защита от спама и злоупотреблений.
"""
import os
import redis
import time
from typing import Optional, Callable
from functools import wraps
from dotenv import load_dotenv

load_dotenv()

# Подключение к Redis
redis_client = redis.from_url(os.getenv('REDIS_URL', 'redis://localhost:6379/0'))


class RateLimitExceeded(Exception):
    """Исключение при превышении rate limit."""
    def __init__(self, limit: int, window: int, retry_after: int):
        self.limit = limit
        self.window = window
        self.retry_after = retry_after
        message = (
            f"Rate limit exceeded: {limit} requests per {window} seconds. "
            f"Try again in {retry_after} seconds."
        )
        super().__init__(message)


# Квоты для разных типов пользователей
RATE_LIMITS = {
    'free': {
        'ai_requests': (5, 60),        # 5 AI запросов в минуту
        'document_upload': (3, 300),   # 3 загрузки в 5 минут
        'api_calls': (30, 60),         # 30 API вызовов в минуту
    },
    'premium': {
        'ai_requests': (20, 60),       # 20 AI запросов в минуту
        'document_upload': (10, 300),  # 10 загрузок в 5 минут
        'api_calls': (100, 60),        # 100 API вызовов в минуту
    },
    'admin': {
        'ai_requests': (100, 60),      # 100 AI запросов в минуту
        'document_upload': (50, 300),  # 50 загрузок в 5 минут
        'api_calls': (500, 60),        # 500 API вызовов в минуту
    }
}


def get_user_tier(user_id: int) -> str:
    """
    Определение тира пользователя.
    TODO: Интегрировать с БД для проверки premium статуса.

    Args:
        user_id: ID пользователя

    Returns:
        Tier пользователя ('free', 'premium', 'admin')
    """
    # Временная заглушка - все пользователи free tier
    # В production нужно проверять в БД
    return 'free'


def check_rate_limit(
    user_id: int,
    action: str,
    user_tier: Optional[str] = None
) -> bool:
    """
    Проверка rate limit для пользователя.

    Args:
        user_id: ID пользователя
        action: Тип действия ('ai_requests', 'document_upload', 'api_calls')
        user_tier: Tier пользователя (опционально, автоопределение)

    Returns:
        True если лимит не превышен

    Raises:
        RateLimitExceeded: Если лимит превышен
    """
    if user_tier is None:
        user_tier = get_user_tier(user_id)

    # Получаем лимиты для этого tier и действия
    limits = RATE_LIMITS.get(user_tier, RATE_LIMITS['free'])
    if action not in limits:
        # Если действие не найдено, используем дефолтный лимит
        limit, window = 10, 60
    else:
        limit, window = limits[action]

    # Ключ в Redis
    key = f"rate_limit:{user_id}:{action}"

    # Получаем текущее количество запросов
    current = redis_client.get(key)

    if current is None:
        # Первый запрос в окне - устанавливаем счетчик
        redis_client.setex(key, window, 1)
        return True

    current = int(current)

    if current >= limit:
        # Лимит превышен
        ttl = redis_client.ttl(key)
        if ttl == -1:
            # Нет TTL, сбрасываем
            redis_client.setex(key, window, 1)
            return True

        raise RateLimitExceeded(limit, window, ttl)

    # Инкрементируем счетчик
    redis_client.incr(key)
    return True


def rate_limit(action: str):
    """
    Декоратор для rate limiting Telegram bot handlers.

    Args:
        action: Тип действия для rate limiting

    Example:
        @rate_limit('ai_requests')
        async def handle_message(update, context):
            ...
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(update, context, *args, **kwargs):
            user_id = update.effective_user.id

            try:
                check_rate_limit(user_id, action)
            except RateLimitExceeded as e:
                await update.message.reply_text(
                    f"⏱️ Превышен лимит запросов!\n\n"
                    f"Лимит: {e.limit} запросов в {e.window} секунд.\n"
                    f"Попробуйте снова через {e.retry_after} сек.\n\n"
                    f"💎 Хотите больше? Перейдите на Premium!"
                )
                return

            return await func(update, context, *args, **kwargs)

        return wrapper
    return decorator


def get_rate_limit_info(user_id: int, action: str) -> dict:
    """
    Получить информацию о текущем состоянии rate limit.

    Args:
        user_id: ID пользователя
        action: Тип действия

    Returns:
        Словарь с информацией о лимите
    """
    user_tier = get_user_tier(user_id)
    limits = RATE_LIMITS.get(user_tier, RATE_LIMITS['free'])
    limit, window = limits.get(action, (10, 60))

    key = f"rate_limit:{user_id}:{action}"
    current = redis_client.get(key)
    current = int(current) if current else 0

    ttl = redis_client.ttl(key)
    if ttl == -1 or ttl == -2:
        ttl = window

    return {
        'tier': user_tier,
        'action': action,
        'limit': limit,
        'window': window,
        'current': current,
        'remaining': max(0, limit - current),
        'reset_in': ttl
    }


def reset_rate_limit(user_id: int, action: str):
    """
    Сброс rate limit для пользователя (admin функция).

    Args:
        user_id: ID пользователя
        action: Тип действия
    """
    key = f"rate_limit:{user_id}:{action}"
    redis_client.delete(key)


# === FastAPI middleware ===

class RateLimitMiddleware:
    """
    Middleware для FastAPI rate limiting.
    """
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope['type'] != 'http':
            await self.app(scope, receive, send)
            return

        # Получаем user_id из scope (должен быть установлен auth middleware)
        user_id = scope.get('user_id')

        if user_id:
            try:
                check_rate_limit(user_id, 'api_calls')
            except RateLimitExceeded as e:
                # Возвращаем 429 Too Many Requests
                response = {
                    'detail': str(e),
                    'retry_after': e.retry_after
                }

                import json
                await send({
                    'type': 'http.response.start',
                    'status': 429,
                    'headers': [
                        (b'content-type', b'application/json'),
                        (b'retry-after', str(e.retry_after).encode()),
                    ],
                })
                await send({
                    'type': 'http.response.body',
                    'body': json.dumps(response).encode(),
                })
                return

        await self.app(scope, receive, send)


# Пример использования
if __name__ == "__main__":
    print("Testing rate limiter...")

    # Тест базового rate limiting
    test_user_id = 12345
    action = 'ai_requests'

    try:
        # Симуляция множественных запросов
        for i in range(8):
            try:
                check_rate_limit(test_user_id, action)
                print(f"✅ Request {i+1} allowed")

                # Показываем оставшиеся запросы
                info = get_rate_limit_info(test_user_id, action)
                print(f"   Remaining: {info['remaining']}/{info['limit']}, "
                      f"Resets in: {info['reset_in']}s")

            except RateLimitExceeded as e:
                print(f"❌ Request {i+1} blocked: {e}")
                break

    finally:
        # Очистка тестовых данных
        reset_rate_limit(test_user_id, action)
        print(f"\n🧹 Cleaned up test data")

    print("\n" + "="*50)
    print("Rate limit tiers:")
    for tier, limits in RATE_LIMITS.items():
        print(f"\n{tier.upper()}:")
        for action, (limit, window) in limits.items():
            print(f"  {action}: {limit} requests / {window}s")
