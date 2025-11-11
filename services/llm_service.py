"""
Modular LLM Service abstraction layer.

This module provides a clean abstraction over different LLM providers
(Gemini, OpenAI, Claude, etc.) making it easy to:
- Switch between providers
- Add new providers
- Use multiple providers simultaneously
- Implement retry logic and error handling
- Cache responses
"""
import logging
import time
from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional, Dict, Any, List
from dataclasses import dataclass

from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log,
)

logger = logging.getLogger(__name__)


class LLMProvider(str, Enum):
    """Supported LLM providers."""
    GEMINI = "gemini"
    OPENAI = "openai"
    CLAUDE = "claude"
    LOCAL = "local"


@dataclass
class LLMResponse:
    """
    Standardized LLM response format.

    Attributes:
        content: The generated text
        provider: Which LLM provider was used
        model: The specific model used
        tokens_used: Approximate tokens consumed
        cached: Whether the response was cached
        response_time_ms: Response time in milliseconds
        metadata: Additional provider-specific metadata
    """
    content: str
    provider: LLMProvider
    model: str
    tokens_used: Optional[int] = None
    cached: bool = False
    response_time_ms: Optional[int] = None
    metadata: Optional[Dict[str, Any]] = None


class LLMService(ABC):
    """
    Abstract base class for LLM services.

    All LLM providers should implement this interface.
    """

    def __init__(self, model_name: str, api_key: Optional[str] = None):
        """
        Initialize LLM service.

        Args:
            model_name: Model identifier (e.g., "gemini-1.5-pro-002")
            api_key: API key for the provider
        """
        self.model_name = model_name
        self.api_key = api_key
        self._initialized = False

    @abstractmethod
    def initialize(self) -> None:
        """
        Initialize the LLM service.

        This is called once during application startup.
        Should setup API clients, validate credentials, etc.
        """
        pass

    @abstractmethod
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> LLMResponse:
        """
        Generate text from the LLM.

        Args:
            prompt: User prompt/question
            system_prompt: System instructions (role, style, etc.)
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens to generate
            **kwargs: Provider-specific parameters

        Returns:
            LLMResponse: Standardized response

        Raises:
            LLMError: If generation fails
        """
        pass

    @abstractmethod
    async def generate_with_context(
        self,
        prompt: str,
        context: str,
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> LLMResponse:
        """
        Generate text with document context.

        Args:
            prompt: User question
            context: Document content or context
            system_prompt: System instructions
            **kwargs: Provider-specific parameters

        Returns:
            LLMResponse: Standardized response
        """
        pass

    @property
    def is_initialized(self) -> bool:
        """Check if service is initialized."""
        return self._initialized


class LLMError(Exception):
    """Base exception for LLM errors."""
    pass


class LLMRateLimitError(LLMError):
    """Rate limit exceeded."""
    pass


class LLMAuthenticationError(LLMError):
    """Authentication failed."""
    pass


class LLMConnectionError(LLMError):
    """Connection error."""
    pass


# ==================== Gemini Implementation ====================

class GeminiService(LLMService):
    """
    Google Gemini LLM service implementation.
    """

    def __init__(self, model_name: str = "gemini-1.5-pro-002", api_key: Optional[str] = None):
        super().__init__(model_name, api_key)
        self.client = None
        self.model = None

    def initialize(self) -> None:
        """Initialize Gemini API client."""
        try:
            import google.generativeai as genai

            if not self.api_key:
                raise LLMAuthenticationError("Gemini API key is required")

            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(self.model_name)
            self._initialized = True

            logger.info(f"✅ Gemini service initialized: {self.model_name}")

        except ImportError:
            raise LLMError("google-generativeai package not installed")
        except Exception as e:
            raise LLMError(f"Failed to initialize Gemini: {e}")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((LLMConnectionError, LLMRateLimitError)),
        before_sleep=before_sleep_log(logger, logging.WARNING)
    )
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> LLMResponse:
        """Generate text using Gemini."""
        if not self._initialized:
            raise LLMError("Service not initialized. Call initialize() first.")

        start_time = time.time()

        try:
            # Build full prompt with system instructions
            full_prompt = prompt
            if system_prompt:
                full_prompt = f"{system_prompt}\n\n{prompt}"

            # Configure generation
            generation_config = {
                "temperature": temperature,
            }
            if max_tokens:
                generation_config["max_output_tokens"] = max_tokens

            # Generate response
            response = self.model.generate_content(
                full_prompt,
                generation_config=generation_config
            )

            # Calculate response time
            response_time_ms = int((time.time() - start_time) * 1000)

            # Extract text
            content = response.text if hasattr(response, 'text') else str(response)

            # Estimate tokens (rough estimate: 1 token ≈ 4 characters)
            tokens_used = (len(full_prompt) + len(content)) // 4

            return LLMResponse(
                content=content,
                provider=LLMProvider.GEMINI,
                model=self.model_name,
                tokens_used=tokens_used,
                response_time_ms=response_time_ms,
                metadata={
                    "temperature": temperature,
                }
            )

        except Exception as e:
            error_msg = str(e).lower()

            # Map errors to custom exceptions
            if "rate limit" in error_msg or "quota" in error_msg:
                raise LLMRateLimitError(f"Gemini rate limit exceeded: {e}")
            elif "authentication" in error_msg or "api key" in error_msg:
                raise LLMAuthenticationError(f"Gemini authentication failed: {e}")
            elif "connection" in error_msg or "network" in error_msg:
                raise LLMConnectionError(f"Gemini connection error: {e}")
            else:
                raise LLMError(f"Gemini generation failed: {e}")

    async def generate_with_context(
        self,
        prompt: str,
        context: str,
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> LLMResponse:
        """Generate text with document context."""
        # Build context-aware prompt
        context_prompt = f"""Context (Document Content):
{context}

---

User Question:
{prompt}

Please answer the question based on the provided context."""

        return await self.generate(
            prompt=context_prompt,
            system_prompt=system_prompt,
            **kwargs
        )


# ==================== OpenAI Implementation (Stub) ====================

class OpenAIService(LLMService):
    """
    OpenAI LLM service implementation (GPT-4, GPT-3.5).

    Note: This is a stub implementation. Implement when needed.
    """

    def initialize(self) -> None:
        """Initialize OpenAI API client."""
        raise NotImplementedError("OpenAI service not yet implemented")

    async def generate(self, prompt: str, **kwargs) -> LLMResponse:
        """Generate text using OpenAI."""
        raise NotImplementedError("OpenAI service not yet implemented")

    async def generate_with_context(
        self,
        prompt: str,
        context: str,
        **kwargs
    ) -> LLMResponse:
        """Generate text with context."""
        raise NotImplementedError("OpenAI service not yet implemented")


# ==================== Claude Implementation (Stub) ====================

class ClaudeService(LLMService):
    """
    Anthropic Claude LLM service implementation.

    Note: This is a stub implementation. Implement when needed.
    """

    def initialize(self) -> None:
        """Initialize Claude API client."""
        raise NotImplementedError("Claude service not yet implemented")

    async def generate(self, prompt: str, **kwargs) -> LLMResponse:
        """Generate text using Claude."""
        raise NotImplementedError("Claude service not yet implemented")

    async def generate_with_context(
        self,
        prompt: str,
        context: str,
        **kwargs
    ) -> LLMResponse:
        """Generate text with context."""
        raise NotImplementedError("Claude service not yet implemented")


# ==================== Service Factory ====================

_service_instance: Optional[LLMService] = None


def get_llm_service(
    provider: LLMProvider = LLMProvider.GEMINI,
    model_name: Optional[str] = None,
    api_key: Optional[str] = None,
    force_new: bool = False
) -> LLMService:
    """
    Get LLM service instance (singleton pattern).

    Args:
        provider: LLM provider to use
        model_name: Model name (uses defaults if not specified)
        api_key: API key (reads from config if not specified)
        force_new: Force creation of new instance

    Returns:
        LLMService: Configured LLM service

    Raises:
        LLMError: If service creation fails

    Example:
        >>> service = get_llm_service(LLMProvider.GEMINI)
        >>> response = await service.generate("What is Python?")
        >>> print(response.content)
    """
    global _service_instance

    # Return cached instance if available
    if _service_instance is not None and not force_new:
        return _service_instance

    # Load from config if not specified
    if api_key is None:
        from config import get_settings
        settings = get_settings()

        if provider == LLMProvider.GEMINI:
            api_key = settings.gemini_api_key
            if model_name is None:
                model_name = settings.gemini_model_name
        elif provider == LLMProvider.OPENAI:
            api_key = settings.openai_api_key
            if model_name is None:
                model_name = "gpt-4"

    # Create service instance
    if provider == LLMProvider.GEMINI:
        service = GeminiService(model_name=model_name, api_key=api_key)
    elif provider == LLMProvider.OPENAI:
        service = OpenAIService(model_name=model_name, api_key=api_key)
    elif provider == LLMProvider.CLAUDE:
        service = ClaudeService(model_name=model_name, api_key=api_key)
    else:
        raise LLMError(f"Unsupported provider: {provider}")

    # Initialize service
    service.initialize()

    # Cache instance
    if not force_new:
        _service_instance = service

    return service


def reset_llm_service() -> None:
    """
    Reset the cached LLM service instance.

    Useful for testing or switching providers.
    """
    global _service_instance
    _service_instance = None


# ==================== Helper Functions ====================

async def generate_with_retry(
    prompt: str,
    context: Optional[str] = None,
    provider: LLMProvider = LLMProvider.GEMINI,
    max_retries: int = 3,
    **kwargs
) -> LLMResponse:
    """
    Generate text with automatic retry on failure.

    This is a convenience function that wraps the LLM service
    with additional retry logic.

    Args:
        prompt: User prompt
        context: Optional document context
        provider: LLM provider to use
        max_retries: Maximum retry attempts
        **kwargs: Additional generation parameters

    Returns:
        LLMResponse: Generated response

    Raises:
        LLMError: If all retries fail
    """
    service = get_llm_service(provider)

    for attempt in range(max_retries):
        try:
            if context:
                return await service.generate_with_context(prompt, context, **kwargs)
            else:
                return await service.generate(prompt, **kwargs)

        except (LLMConnectionError, LLMRateLimitError) as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                logger.warning(
                    f"LLM request failed (attempt {attempt + 1}/{max_retries}). "
                    f"Retrying in {wait_time}s... Error: {e}"
                )
                time.sleep(wait_time)
            else:
                logger.error(f"LLM request failed after {max_retries} attempts")
                raise

        except Exception as e:
            logger.error(f"Unexpected error in LLM request: {e}")
            raise


# ==================== Usage Example ====================

if __name__ == "__main__":
    """
    Test LLM service.

    Run: python -m services.llm_service
    """
    import asyncio
    from dotenv import load_dotenv
    import os

    load_dotenv()

    async def test_service():
        print("=" * 60)
        print("🤖 Testing LLM Service")
        print("=" * 60)

        try:
            # Get service
            print("\n[1/3] Initializing Gemini service...")
            service = get_llm_service(
                provider=LLMProvider.GEMINI,
                api_key=os.getenv("GEMINI_API_KEY")
            )
            print(f"✅ Service initialized: {service.model_name}")

            # Test simple generation
            print("\n[2/3] Testing simple generation...")
            response = await service.generate(
                prompt="What is Python? Answer in one sentence.",
                temperature=0.7
            )
            print(f"✅ Response received ({response.response_time_ms}ms):")
            print(f"   {response.content[:100]}...")

            # Test context-aware generation
            print("\n[3/3] Testing context-aware generation...")
            context = "Python is a high-level programming language created by Guido van Rossum in 1991."
            response = await service.generate_with_context(
                prompt="Who created Python?",
                context=context
            )
            print(f"✅ Response received ({response.response_time_ms}ms):")
            print(f"   {response.content}")

            print("\n" + "=" * 60)
            print("✅ All tests passed!")
            print("=" * 60)

        except Exception as e:
            print(f"\n❌ Test failed: {e}")
            import traceback
            traceback.print_exc()

    # Run async test
    asyncio.run(test_service())
