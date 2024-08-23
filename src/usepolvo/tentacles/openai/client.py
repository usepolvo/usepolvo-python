from typing import Optional

from openai import OpenAI

from usepolvo.arms.base_client import BaseClient
from usepolvo.tentacles.openai.completions.resource import OpenAICompletionResource
from usepolvo.tentacles.openai.config import get_settings
from usepolvo.tentacles.openai.rate_limiter import OpenAIRateLimiter


class OpenAIClient(BaseClient):
    def __init__(self, api_key: Optional[str] = None):
        super().__init__()
        settings = get_settings()
        self.api_key = api_key if api_key else settings.openai_api_key
        self.client: OpenAI = OpenAI(api_key=self.api_key)
        self.rate_limiter = OpenAIRateLimiter()
        self._completions: Optional[OpenAICompletionResource] = None

    @property
    def completions(self):
        if self._completions is None:
            self._completions = OpenAICompletionResource(self)
        return self._completions

    def handle_error(self, e):
        super().handle_error(e)
        # Additional OpenAI-specific error handling can be added here
