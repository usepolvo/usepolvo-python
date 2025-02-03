from typing import Dict, Optional

from usepolvo.arms.base_auth import BaseAuth
from usepolvo.beak.exceptions import AuthenticationError
from usepolvo.tentacles.certn.config import get_settings


class CertnAuth(BaseAuth):
    """Certn API key authentication implementation."""

    def __init__(self, api_key: Optional[str] = None):
        super().__init__()
        self.settings = get_settings()
        self.api_key = api_key or self.settings.CERTN_API_KEY

        if not self.api_key:
            raise AuthenticationError("API key is required")

    def get_auth_headers(self) -> Dict[str, str]:
        """Get Certn-specific authentication headers."""
        return {"Authorization": f"Bearer {self.api_key}"}
