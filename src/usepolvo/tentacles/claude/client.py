from typing import Optional

from anthropic import Anthropic

from usepolvo.arms.base_client import BaseClient
from usepolvo.tentacles.claude.auth import ClaudeAuth
from usepolvo.tentacles.claude.completions import CompletionResource
from usepolvo.tentacles.claude.config import get_settings
from usepolvo.tentacles.claude.rate_limiter import ClaudeRateLimiter


class ClaudeClient(BaseClient):
    """
    Claude API client with API key authentication.

    Example usage:
        client = ClaudeClient(api_key="your-api-key")
        completion = client.completions.create(prompt="Hello!")
    """

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the Claude client."""
        super().__init__()

        # Initialize settings and auth
        self.settings = get_settings()
        self.auth = ClaudeAuth(api_key=api_key)

        # Initialize Anthropic client
        self.client = Anthropic(api_key=self.auth.api_key)

        # Initialize rate limiter
        self.rate_limiter = ClaudeRateLimiter()

        # Initialize resources
        self._completions = None

    @property
    def completions(self) -> CompletionResource:
        """Access the completions resource."""
        if self._completions is None:
            self._completions = CompletionResource(self)
        return self._completions

    def handle_error(self, e):
        """Handle Claude-specific errors."""
        super().handle_error(e)
        # Additional Claude-specific error handling can be added here
