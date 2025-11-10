"""
Unit tests for rate limiting middleware.
Tests rate limiter functionality and quotas.
"""
import pytest
from middleware.rate_limiter import (
    check_rate_limit,
    get_rate_limit_info,
    reset_rate_limit,
    RateLimitExceeded,
    RATE_LIMITS,
)


@pytest.mark.unit
@pytest.mark.redis
class TestRateLimitBasics:
    """Tests for basic rate limiting functionality."""

    def test_first_request_allowed(self, mock_redis_client):
        """Test that first request is always allowed."""
        mock_redis_client.get.return_value = None

        result = check_rate_limit(12345, 'ai_requests')
        assert result is True

        # Should have called setex to initialize counter
        mock_redis_client.setex.assert_called_once()

    def test_within_limit_allowed(self, mock_redis_client):
        """Test requests within limit are allowed."""
        # Simulate 2 requests already made (limit is 5)
        mock_redis_client.get.return_value = b'2'

        result = check_rate_limit(12345, 'ai_requests')
        assert result is True

        # Should increment counter
        mock_redis_client.incr.assert_called_once()

    def test_exceeding_limit_raises_error(self, mock_redis_client):
        """Test that exceeding limit raises exception."""
        # Simulate 5 requests already made (limit is 5)
        mock_redis_client.get.return_value = b'5'
        mock_redis_client.ttl.return_value = 45

        with pytest.raises(RateLimitExceeded) as exc_info:
            check_rate_limit(12345, 'ai_requests')

        assert exc_info.value.limit == 5
        assert exc_info.value.window == 60
        assert exc_info.value.retry_after == 45

    def test_rate_limit_exception_message(self, mock_redis_client):
        """Test RateLimitExceeded exception message."""
        mock_redis_client.get.return_value = b'5'
        mock_redis_client.ttl.return_value = 30

        with pytest.raises(RateLimitExceeded) as exc_info:
            check_rate_limit(12345, 'ai_requests')

        error_msg = str(exc_info.value)
        assert '5 requests' in error_msg
        assert '60 seconds' in error_msg
        assert '30 seconds' in error_msg


@pytest.mark.unit
@pytest.mark.redis
class TestRateLimitTiers:
    """Tests for different user tiers."""

    def test_free_tier_limits(self, mock_redis_client, monkeypatch):
        """Test free tier has correct limits."""
        # Mock get_user_tier to return 'free'
        import middleware.rate_limiter as rl_module
        monkeypatch.setattr(rl_module, 'get_user_tier', lambda uid: 'free')

        mock_redis_client.get.return_value = None

        check_rate_limit(12345, 'ai_requests', user_tier='free')

        # Free tier: 5 requests per 60 seconds
        call_args = mock_redis_client.setex.call_args
        assert call_args[0][0] == 'rate_limit:12345:ai_requests'
        assert call_args[0][1] == 60  # window

    def test_premium_tier_limits(self, mock_redis_client):
        """Test premium tier has higher limits."""
        mock_redis_client.get.return_value = b'15'  # 15 requests made

        # Premium tier: 20 requests per minute
        result = check_rate_limit(12345, 'ai_requests', user_tier='premium')
        assert result is True  # Still within limit

    def test_admin_tier_limits(self, mock_redis_client):
        """Test admin tier has highest limits."""
        mock_redis_client.get.return_value = b'50'  # 50 requests made

        # Admin tier: 100 requests per minute
        result = check_rate_limit(12345, 'ai_requests', user_tier='admin')
        assert result is True  # Still within limit

    def test_different_actions_different_limits(self, mock_redis_client):
        """Test different actions have different limits."""
        mock_redis_client.get.return_value = None

        # AI requests: 5/min for free tier
        check_rate_limit(12345, 'ai_requests', user_tier='free')
        call1 = mock_redis_client.setex.call_args[0]

        # Document uploads: 3/5min for free tier
        check_rate_limit(12345, 'document_upload', user_tier='free')
        call2 = mock_redis_client.setex.call_args[0]

        # Different windows
        assert call1[1] == 60  # AI: 1 minute
        assert call2[1] == 300  # Upload: 5 minutes


@pytest.mark.unit
@pytest.mark.redis
class TestRateLimitInfo:
    """Tests for rate limit information retrieval."""

    def test_get_rate_limit_info_no_requests(self, mock_redis_client):
        """Test getting info when no requests made."""
        mock_redis_client.get.return_value = None

        info = get_rate_limit_info(12345, 'ai_requests')

        assert info['tier'] == 'free'
        assert info['action'] == 'ai_requests'
        assert info['limit'] == 5
        assert info['window'] == 60
        assert info['current'] == 0
        assert info['remaining'] == 5

    def test_get_rate_limit_info_with_requests(self, mock_redis_client):
        """Test getting info after some requests."""
        mock_redis_client.get.return_value = b'3'
        mock_redis_client.ttl.return_value = 45

        info = get_rate_limit_info(12345, 'ai_requests')

        assert info['current'] == 3
        assert info['remaining'] == 2  # 5 - 3
        assert info['reset_in'] == 45

    def test_get_rate_limit_info_limit_exceeded(self, mock_redis_client):
        """Test getting info when limit exceeded."""
        mock_redis_client.get.return_value = b'6'  # Over limit of 5
        mock_redis_client.ttl.return_value = 30

        info = get_rate_limit_info(12345, 'ai_requests')

        assert info['current'] == 6
        assert info['remaining'] == 0  # Can't go negative


@pytest.mark.unit
@pytest.mark.redis
class TestRateLimitReset:
    """Tests for rate limit reset functionality."""

    def test_reset_rate_limit(self, mock_redis_client):
        """Test resetting rate limit for user."""
        reset_rate_limit(12345, 'ai_requests')

        mock_redis_client.delete.assert_called_once_with(
            'rate_limit:12345:ai_requests'
        )

    def test_reset_allows_new_requests(self, mock_redis_client):
        """Test that reset allows new requests."""
        # First, exceed limit
        mock_redis_client.get.return_value = b'5'
        mock_redis_client.ttl.return_value = 30

        with pytest.raises(RateLimitExceeded):
            check_rate_limit(12345, 'ai_requests')

        # Reset
        reset_rate_limit(12345, 'ai_requests')

        # Now should work
        mock_redis_client.get.return_value = None
        result = check_rate_limit(12345, 'ai_requests')
        assert result is True


@pytest.mark.unit
class TestRateLimitConfig:
    """Tests for rate limit configuration."""

    def test_rate_limits_structure(self):
        """Test that RATE_LIMITS has correct structure."""
        assert 'free' in RATE_LIMITS
        assert 'premium' in RATE_LIMITS
        assert 'admin' in RATE_LIMITS

        for tier in ['free', 'premium', 'admin']:
            assert 'ai_requests' in RATE_LIMITS[tier]
            assert 'document_upload' in RATE_LIMITS[tier]
            assert 'api_calls' in RATE_LIMITS[tier]

    def test_rate_limits_format(self):
        """Test that rate limits are tuples of (limit, window)."""
        for tier_limits in RATE_LIMITS.values():
            for action_limit in tier_limits.values():
                assert isinstance(action_limit, tuple)
                assert len(action_limit) == 2
                limit, window = action_limit
                assert isinstance(limit, int)
                assert isinstance(window, int)
                assert limit > 0
                assert window > 0

    def test_premium_higher_than_free(self):
        """Test that premium tier has higher limits than free."""
        for action in ['ai_requests', 'document_upload', 'api_calls']:
            free_limit = RATE_LIMITS['free'][action][0]
            premium_limit = RATE_LIMITS['premium'][action][0]
            assert premium_limit > free_limit

    def test_admin_highest_limits(self):
        """Test that admin tier has highest limits."""
        for action in ['ai_requests', 'document_upload', 'api_calls']:
            free_limit = RATE_LIMITS['free'][action][0]
            premium_limit = RATE_LIMITS['premium'][action][0]
            admin_limit = RATE_LIMITS['admin'][action][0]

            assert admin_limit >= premium_limit >= free_limit
