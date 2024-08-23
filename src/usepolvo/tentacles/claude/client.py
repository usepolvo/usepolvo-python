from typing import Optional

from anthropic import Anthropic

from usepolvo.arms.base_client import BaseClient
from usepolvo.tentacles.claude.completions.resource import ClaudeCompletionResource
from usepolvo.tentacles.claude.config import get_settings
from usepolvo.tentacles.claude.rate_limiter import ClaudeRateLimiter


class ClaudeClient(BaseClient):
    def __init__(self, api_key: Optional[str] = None):
        super().__init__()
        settings = get_settings()
        self.api_key = api_key if api_key else settings.claude_api_key
        self.client = Anthropic(api_key=self.api_key)
        self.rate_limiter = ClaudeRateLimiter()
        self._completions = None

    @property
    def completions(self):
        if self._completions is None:
            self._completions = ClaudeCompletionResource(self)
        return self._completions

    def handle_error(self, e):
        super().handle_error(e)
        # Additional Claude-specific error handling can be added here
