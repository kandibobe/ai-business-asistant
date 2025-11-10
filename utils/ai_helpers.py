"""
AI helper functions with retry logic and error handling.
"""
import logging
from typing import Optional, Dict, Any
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log,
)
import google.generativeai as genai

logger = logging.getLogger(__name__)


class AIServiceError(Exception):
    """Base exception for AI service errors."""
    pass


class AIRateLimitError(AIServiceError):
    """Raised when AI service rate limit is exceeded."""
    pass


class AIQuotaError(AIServiceError):
    """Raised when AI service quota is exceeded."""
    pass


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type((
        ConnectionError,
        TimeoutError,
        genai.types.BlockedPromptException,
    )),
    before_sleep=before_sleep_log(logger, logging.WARNING),
    reraise=True,
)
def generate_ai_response(
    model: genai.GenerativeModel,
    prompt: str,
    **kwargs
) -> genai.types.GenerateContentResponse:
    """
    Generate AI response with automatic retry logic.

    Retries on:
    - ConnectionError (network issues)
    - TimeoutError (request timeout)
    - BlockedPromptException (safety filter triggered, retryable)

    Args:
        model: Gemini GenerativeModel instance
        prompt: The prompt to send to AI
        **kwargs: Additional arguments for generate_content

    Returns:
        GenerateContentResponse from Gemini

    Raises:
        AIServiceError: On permanent failures
        ConnectionError: After 3 retry attempts
    """
    try:
        logger.info(f"Generating AI response (prompt length: {len(prompt)} chars)")
        response = model.generate_content(prompt, **kwargs)

        # Check if response was blocked
        if not response.text:
            if response.prompt_feedback.block_reason:
                raise AIServiceError(
                    f"AI blocked response: {response.prompt_feedback.block_reason}"
                )

        logger.info(f"AI response generated successfully")
        return response

    except genai.types.BlockedPromptException as e:
        logger.warning(f"AI blocked prompt, will retry: {str(e)}")
        raise

    except Exception as e:
        error_str = str(e).lower()

        # Classify errors
        if "rate limit" in error_str or "429" in error_str:
            raise AIRateLimitError(f"AI rate limit exceeded: {str(e)}")

        if "quota" in error_str or "403" in error_str:
            raise AIQuotaError(f"AI quota exceeded: {str(e)}")

        if "timeout" in error_str or "timed out" in error_str:
            logger.warning(f"AI request timed out, will retry: {str(e)}")
            raise TimeoutError(str(e))

        if "connection" in error_str or "network" in error_str:
            logger.warning(f"Network error, will retry: {str(e)}")
            raise ConnectionError(str(e))

        # Permanent error, don't retry
        logger.error(f"AI service error (non-retryable): {str(e)}")
        raise AIServiceError(f"AI service error: {str(e)}")


def safe_get_text(response: genai.types.GenerateContentResponse) -> Optional[str]:
    """
    Safely extract text from AI response.

    Args:
        response: Gemini response object

    Returns:
        Extracted text or None if unavailable
    """
    try:
        return response.text
    except ValueError:
        # Response doesn't have text (e.g., blocked)
        return None
    except Exception as e:
        logger.error(f"Error extracting text from AI response: {str(e)}")
        return None


def estimate_tokens(text: str) -> int:
    """
    Estimate token count for text.

    Rough estimation: ~4 characters per token for English text.

    Args:
        text: Input text

    Returns:
        Estimated token count
    """
    return len(text) // 4


def truncate_context(text: str, max_tokens: int = 30000) -> str:
    """
    Truncate text to fit within token limit.

    Args:
        text: Input text
        max_tokens: Maximum allowed tokens

    Returns:
        Truncated text
    """
    max_chars = max_tokens * 4  # Rough estimate

    if len(text) <= max_chars:
        return text

    logger.warning(
        f"Context too long ({len(text)} chars), truncating to {max_chars} chars"
    )

    # Truncate and add notice
    truncated = text[:max_chars - 200]  # Leave room for notice
    truncated += "\n\n[... Context truncated due to length ...]"

    return truncated
