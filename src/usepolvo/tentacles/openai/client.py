from typing import Optional

from openai import OpenAI

from usepolvo.arms.base_client import BaseClient
from usepolvo.tentacles.openai.auth import OpenAIAuth
from usepolvo.tentacles.openai.completions.resource import CompletionResource
from usepolvo.tentacles.openai.config import get_settings
from usepolvo.tentacles.openai.rate_limiter import OpenAIRateLimiter


class OpenAIClient(BaseClient):
    """
    OpenAI API client with API key authentication.

    Example usage:
        client = OpenAIClient(api_key="your-api-key")
        completion = client.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": "Hello!"}]
        )
    """

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the OpenAI client."""
        super().__init__()

        # Initialize settings and auth
        self.settings = get_settings()
        self.auth = OpenAIAuth(api_key=api_key or self.settings.OPENAI_API_KEY)

        # Get configured OpenAI client from auth
        self.client: OpenAI = self.auth.client

        # Initialize rate limiter
        self.rate_limiter = OpenAIRateLimiter()

        # Initialize resources
        self._completions: Optional[CompletionResource] = None

    @property
    def completions(self) -> CompletionResource:
        """Access the completions resource."""
        if self._completions is None:
            self._completions = CompletionResource(self)
        return self._completions

    def handle_error(self, e):
        """Handle OpenAI-specific errors."""
        super().handle_error(e)
        # Additional OpenAI-specific error handling can be added here
