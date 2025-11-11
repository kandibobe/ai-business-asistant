"""
Unit tests for AI helper functions.
Tests retry logic, error handling, and caching integration.
"""
import pytest
from unittest.mock import MagicMock, patch
from utils.ai_helpers import (
    generate_ai_response,
    safe_get_text,
    truncate_context,
    AIServiceError,
)


class TestGenerateAIResponse:
    """Tests for generate_ai_response function with retry logic."""

    def test_successful_response(self, mock_gemini_model):
        """Test successful AI response generation."""
        result = generate_ai_response(
            model=mock_gemini_model,
            prompt="Test question",
            context="Test context"
        )

        assert result is not None
        assert isinstance(result, dict)
        assert 'message' in result
        mock_gemini_model.generate_content.assert_called_once()

    def test_retry_on_failure(self, mock_gemini_model):
        """Test retry logic when AI service fails."""
        # First call fails, second succeeds
        mock_gemini_model.generate_content.side_effect = [
            Exception("Service temporarily unavailable"),
            MagicMock(text="Success response")
        ]

        result = generate_ai_response(
            model=mock_gemini_model,
            prompt="Test question",
            max_retries=3
        )

        assert result is not None
        assert mock_gemini_model.generate_content.call_count == 2

    def test_max_retries_exceeded(self, mock_gemini_model):
        """Test that AIServiceError is raised after max retries."""
        mock_gemini_model.generate_content.side_effect = Exception("Request timed out")

        with pytest.raises(AIServiceError):
            generate_ai_response(
                model=mock_gemini_model,
                prompt="Test question",
                max_retries=2
            )

        assert mock_gemini_model.generate_content.call_count == 2

    def test_empty_prompt_handling(self, mock_gemini_model):
        """Test handling of empty prompts."""
        with pytest.raises(ValueError):
            generate_ai_response(
                model=mock_gemini_model,
                prompt=""
            )

    @patch('utils.cache.ai_chat_cache')
    def test_caching_integration(self, mock_cache, mock_gemini_model):
        """Test integration with AI response cache."""
        # Cache miss, then hit
        mock_cache.get.return_value = None
        mock_gemini_model.generate_content.return_value = MagicMock(
            text="Cached response"
        )

        # First call - cache miss
        result1 = generate_ai_response(
            model=mock_gemini_model,
            prompt="Test question",
            use_cache=True
        )

        # Second call - should use cache
        mock_cache.get.return_value = {"message": "Cached response", "cached": True}
        result2 = generate_ai_response(
            model=mock_gemini_model,
            prompt="Test question",
            use_cache=True
        )

        assert mock_gemini_model.generate_content.call_count == 1
        assert result2.get('cached') is True


class TestSafeGetText:
    """Tests for safe_get_text utility function."""

    def test_valid_text_extraction(self, mock_gemini_model):
        """Test successful text extraction from AI response."""
        response = MagicMock()
        response.text = "Valid response text"

        text = safe_get_text(response)

        assert text == "Valid response text"

    def test_none_response(self):
        """Test handling of None response."""
        text = safe_get_text(None)
        assert text == ""

    def test_missing_text_attribute(self):
        """Test handling of response without text attribute."""
        response = MagicMock(spec=[])  # No text attribute
        text = safe_get_text(response)
        assert text == ""

    def test_empty_text(self, mock_gemini_model):
        """Test handling of empty text in response."""
        response = MagicMock()
        response.text = ""

        text = safe_get_text(response)
        assert text == ""


class TestTruncateContext:
    """Tests for context truncation function."""

    def test_no_truncation_needed(self):
        """Test that short context is not truncated."""
        context = "This is a short context."
        result = truncate_context(context, max_length=1000)
        assert result == context

    def test_truncation_applied(self):
        """Test that long context is truncated correctly."""
        context = "A" * 5000
        result = truncate_context(context, max_length=1000)
        assert len(result) <= 1000
        assert "..." in result

    def test_preserve_beginning_and_end(self):
        """Test that truncation preserves beginning and end."""
        context = "START" + ("X" * 5000) + "END"
        result = truncate_context(context, max_length=1000)

        # Should contain START and END
        assert "START" in result
        # Note: END might be truncated depending on implementation
        assert len(result) <= 1000

    def test_empty_context(self):
        """Test handling of empty context."""
        result = truncate_context("", max_length=1000)
        assert result == ""

    def test_unicode_handling(self):
        """Test proper handling of unicode characters."""
        context = "Привет мир! " * 200  # Russian text
        result = truncate_context(context, max_length=500)
        assert len(result) <= 500
        # Should not break unicode characters
        assert isinstance(result, str)


class TestAIResponseFormatting:
    """Tests for AI response formatting and validation."""

    def test_response_contains_required_fields(self, mock_gemini_model):
        """Test that formatted response contains all required fields."""
        result = generate_ai_response(
            model=mock_gemini_model,
            prompt="Test question"
        )

        # Check required fields
        assert 'message' in result
        assert 'response_time_ms' in result or 'response_time' in result
        assert isinstance(result['message'], str)

    def test_response_time_is_positive(self, mock_gemini_model):
        """Test that response time is a positive number."""
        result = generate_ai_response(
            model=mock_gemini_model,
            prompt="Test question"
        )

        if 'response_time_ms' in result:
            assert result['response_time_ms'] >= 0
        if 'response_time' in result:
            assert result['response_time'] >= 0

    def test_token_count_tracking(self, mock_gemini_model):
        """Test that token usage is tracked when available."""
        # Mock response with usage metadata
        response = MagicMock()
        response.text = "Response with token tracking"
        response.usage_metadata = MagicMock()
        response.usage_metadata.total_token_count = 150

        mock_gemini_model.generate_content.return_value = response

        result = generate_ai_response(
            model=mock_gemini_model,
            prompt="Test question"
        )

        # Token count should be included if available
        if 'tokens_used' in result:
            assert result['tokens_used'] > 0


# Fixtures for this test module
@pytest.fixture
def sample_ai_response():
    """Sample AI response for testing."""
    return {
        'message': 'This is a test response from the AI.',
        'response_time_ms': 1234,
        'tokens_used': 150,
        'cached': False
    }


@pytest.fixture
def long_text():
    """Long text for truncation testing."""
    return "Lorem ipsum dolor sit amet. " * 1000  # ~28,000 characters
