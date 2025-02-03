from typing import Dict, Optional

import google.generativeai as genai

from usepolvo.arms.base_auth import BaseAuth
from usepolvo.beak.exceptions import AuthenticationError
from usepolvo.tentacles.gemini.config import get_settings


class GeminiAuth(BaseAuth):
    """Gemini API key authentication implementation."""

    def __init__(self, api_key: Optional[str] = None):
        super().__init__()
        self.settings = get_settings()
        self.api_key = api_key or self.settings.GEMINI_API_KEY

        if not self.api_key:
            raise AuthenticationError("API key is required")

        # Configure Google AI SDK
        genai.configure(api_key=self.api_key)

    def get_auth_headers(self) -> Dict[str, str]:
        """Get Gemini-specific authentication headers."""
        return {"x-goog-api-key": self.api_key}

    @property
    def client(self):
        """Get configured Google AI client."""
        return genai
