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


def generate_ai_response(
    model: genai.GenerativeModel,
    prompt: str,
    context: Optional[str] = None,
    max_retries: int = 3,
    use_cache: bool = False,
    **kwargs
) -> Dict[str, Any]:
    """
    Generate AI response with automatic retry logic and caching.

    Retries on:
    - ConnectionError (network issues)
    - TimeoutError (request timeout)
    - BlockedPromptException (safety filter triggered, retryable)

    Args:
        model: Gemini GenerativeModel instance
        prompt: The prompt to send to AI
        context: Optional context to prepend to prompt
        max_retries: Maximum number of retry attempts (default: 3)
        use_cache: Whether to use AI response caching (default: False)
        **kwargs: Additional arguments for generate_content

    Returns:
        Dict with:
        - message: The AI response text
        - response_time_ms: Response time in milliseconds
        - cached: Whether response was from cache
        - tokens_used: Token count (if available)

    Raises:
        ValueError: If prompt is empty
        AIServiceError: On permanent failures
        ConnectionError: After max retry attempts
    """
    import time

    # Validate input
    if not prompt or not prompt.strip():
        raise ValueError("Prompt cannot be empty")

    # Build full prompt with context
    full_prompt = prompt
    if context:
        full_prompt = f"Context: {context}\n\nQuestion: {prompt}"

    # Check cache if enabled
    if use_cache:
        from utils.cache import ai_chat_cache
        cached = ai_chat_cache.get(full_prompt)
        if cached:
            logger.info("Retrieved response from cache")
            return cached

    # Retry logic
    last_error = None
    start_time = time.time()

    for attempt in range(max_retries):
        try:
            logger.info(f"Generating AI response (attempt {attempt + 1}/{max_retries}, prompt length: {len(full_prompt)} chars)")

            response = model.generate_content(full_prompt, **kwargs)

            # Check if response was blocked
            if not response.text:
                if hasattr(response, 'prompt_feedback') and response.prompt_feedback.block_reason:
                    raise AIServiceError(
                        f"AI blocked response: {response.prompt_feedback.block_reason}"
                    )

            # Calculate response time
            response_time_ms = int((time.time() - start_time) * 1000)

            # Extract token count if available
            tokens_used = None
            if hasattr(response, 'usage_metadata') and response.usage_metadata:
                tokens_used = getattr(response.usage_metadata, 'total_token_count', None)

            # Build result
            result = {
                'message': response.text,
                'response_time_ms': response_time_ms,
                'cached': False,
            }

            if tokens_used:
                result['tokens_used'] = tokens_used

            logger.info(f"AI response generated successfully in {response_time_ms}ms")

            # Cache if enabled
            if use_cache:
                from utils.cache import ai_chat_cache
                ai_chat_cache.set(full_prompt, result)

            return result

        except genai.types.BlockedPromptException as e:
            logger.warning(f"AI blocked prompt (attempt {attempt + 1}/{max_retries}): {str(e)}")
            last_error = e
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                time.sleep(wait_time)
                continue
            else:
                raise AIServiceError(f"AI blocked prompt after {max_retries} attempts")

        except Exception as e:
            error_str = str(e).lower()

            # Check if this is a retryable error
            is_retryable = (
                "rate limit" in error_str or "429" in error_str or
                "quota" in error_str or "403" in error_str or
                "timeout" in error_str or "timed out" in error_str or
                "connection" in error_str or "network" in error_str or
                "temporarily unavailable" in error_str or "503" in error_str or
                "service unavailable" in error_str or "500" in error_str
            )

            # Classify errors
            if "rate limit" in error_str or "429" in error_str:
                last_error = AIRateLimitError(f"AI rate limit exceeded: {str(e)}")
                logger.warning(f"Rate limit error (attempt {attempt + 1}/{max_retries}): {str(e)}")
            elif "quota" in error_str or "403" in error_str:
                last_error = AIQuotaError(f"AI quota exceeded: {str(e)}")
                logger.warning(f"Quota error (attempt {attempt + 1}/{max_retries}): {str(e)}")
            elif is_retryable:
                # Retryable error - log and continue
                logger.warning(f"Retryable error (attempt {attempt + 1}/{max_retries}): {str(e)}")
                last_error = e
            else:
                # Non-retryable pattern, but still retry max_retries times
                logger.warning(f"Error (attempt {attempt + 1}/{max_retries}): {str(e)}")
                last_error = AIServiceError(f"AI service error: {str(e)}")

            # Retry if not last attempt
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                logger.info(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                # Max retries exceeded
                raise AIServiceError(f"Max retries ({max_retries}) exceeded. Last error: {str(last_error)}")

    # Should not reach here, but just in case
    raise AIServiceError(f"Max retries ({max_retries}) exceeded")


def safe_get_text(response: Optional[Any]) -> str:
    """
    Safely extract text from AI response.

    Args:
        response: Gemini response object (or any object with .text attribute)

    Returns:
        Extracted text or empty string if unavailable
    """
    if response is None:
        return ""

    try:
        if hasattr(response, 'text'):
            text = response.text
            return text if text else ""
        return ""
    except ValueError:
        # Response doesn't have text (e.g., blocked)
        return ""
    except Exception as e:
        logger.error(f"Error extracting text from AI response: {str(e)}")
        return ""


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


def truncate_context(text: str, max_length: Optional[int] = None, max_tokens: int = 30000) -> str:
    """
    Truncate text to fit within character or token limit.

    Args:
        text: Input text
        max_length: Maximum character length (if provided, takes precedence over max_tokens)
        max_tokens: Maximum allowed tokens (used if max_length not provided)

    Returns:
        Truncated text with ellipsis if truncated
    """
    if not text:
        return ""

    # Use max_length if provided, otherwise calculate from tokens
    max_chars = max_length if max_length is not None else (max_tokens * 4)

    if len(text) <= max_chars:
        return text

    logger.warning(
        f"Context too long ({len(text)} chars), truncating to {max_chars} chars"
    )

    # Truncate and add ellipsis
    # Try to preserve beginning and end
    if max_chars > 200:
        # Take more from beginning, less from end
        beginning_chars = int(max_chars * 0.7) - 100
        end_chars = max_chars - beginning_chars - 10

        truncated = text[:beginning_chars] + " ... " + text[-end_chars:] if end_chars > 0 else text[:max_chars - 10]

        # If result is still too long, just truncate from end
        if len(truncated) > max_chars:
            truncated = text[:max_chars - 5] + " ..."
    else:
        # For very short limits, just truncate
        truncated = text[:max_chars - 5] + " ..." if max_chars > 5 else text[:max_chars]

    return truncated
