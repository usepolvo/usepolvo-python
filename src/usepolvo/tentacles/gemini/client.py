from typing import Optional

import google.generativeai as genai

from usepolvo.arms.base_client import BaseClient
from usepolvo.tentacles.gemini.completions.resource import GeminiCompletionResource
from usepolvo.tentacles.gemini.config import get_settings
from usepolvo.tentacles.gemini.rate_limiter import GeminiRateLimiter


class GeminiClient(BaseClient):
    def __init__(self, api_key: Optional[str] = None):
        super().__init__()
        settings = get_settings()
        self.api_key = api_key if api_key else settings.gemini_api_key
        genai.configure(api_key=self.api_key)
        self.client = genai
        self.rate_limiter = GeminiRateLimiter()
        self._completions = None

    @property
    def completions(self):
        if self._completions is None:
            self._completions = GeminiCompletionResource(self)
        return self._completions

    def handle_error(self, e):
        super().handle_error(e)
        # Additional Gemini-specific error handling can be added here
