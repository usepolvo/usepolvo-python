from typing import Optional

from usepolvo.arms.base_client import BaseClient
from usepolvo.tentacles.gemini.auth import GeminiAuth
from usepolvo.tentacles.gemini.completions.resource import CompletionResource
from usepolvo.tentacles.gemini.config import get_settings
from usepolvo.tentacles.gemini.rate_limiter import GeminiRateLimiter


class GeminiClient(BaseClient):
    """
    Gemini API client with API key authentication.

    Example usage:
        client = GeminiClient(api_key="your-api-key")
        completion = client.completions.generate(prompt="Hello!")
    """

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the Gemini client."""
        super().__init__()

        # Initialize settings and auth
        self.settings = get_settings()
        self.auth = GeminiAuth(api_key=api_key)

        # Get configured Google AI client from auth
        self.client = self.auth.client

        # Initialize rate limiter
        self.rate_limiter = GeminiRateLimiter()

        # Initialize resources
        self._completions = None

    @property
    def completions(self) -> CompletionResource:
        """Access the completions resource."""
        if self._completions is None:
            self._completions = CompletionResource(self)
        return self._completions

    def handle_error(self, e):
        """Handle Gemini-specific errors."""
        super().handle_error(e)
        # Additional Gemini-specific error handling can be added here
