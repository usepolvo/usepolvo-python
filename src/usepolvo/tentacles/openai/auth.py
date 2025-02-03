from typing import Dict, Optional

from openai import OpenAI

from usepolvo.arms.base_auth import BaseAuth
from usepolvo.beak.exceptions import AuthenticationError
from usepolvo.tentacles.openai.config import get_settings


class OpenAIAuth(BaseAuth):
    """OpenAI API key authentication implementation."""

    def __init__(self, api_key: Optional[str] = None):
        super().__init__()
        self.settings = get_settings()
        self.api_key = api_key or self.settings.OPENAPI_API_KEY

        if not self.api_key:
            raise AuthenticationError("API key is required")

        # Initialize OpenAI client
        self._client = OpenAI(api_key=self.api_key)

    def get_auth_headers(self) -> Dict[str, str]:
        """Get OpenAI-specific authentication headers."""
        return {"Authorization": f"Bearer {self.api_key}", "OpenAI-Organization": self.settings.OPENAI_ORG_ID or ""}

    @property
    def client(self) -> OpenAI:
        """Get configured OpenAI client."""
        return self._client
