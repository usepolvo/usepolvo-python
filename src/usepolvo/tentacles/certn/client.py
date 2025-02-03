from typing import Any, Dict, Optional

from usepolvo.arms.base_client import BaseClient
from usepolvo.arms.base_rate_limiter import BaseRateLimiter
from usepolvo.tentacles.certn.auth import CertnAuth
from usepolvo.tentacles.certn.config import get_settings
from usepolvo.tentacles.certn.exceptions import handle_certn_error
from usepolvo.tentacles.certn.rate_limiter import CertnRateLimiter
from usepolvo.tentacles.certn.resources.applications import ApplicationResource


class CertnClient(BaseClient):
    """
    Certn API client with API key authentication.

    Example usage:
        client = CertnClient(api_key="your-api-key")
        applications = client.applications.list()
    """

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the Certn client."""
        super().__init__()

        # Initialize settings and auth
        self.settings = get_settings()
        self.base_url = self.settings.CERTN_BASE_URL
        self.auth = CertnAuth(api_key=api_key)

        # Initialize rate limiter
        self.rate_limiter = CertnRateLimiter()

        # Initialize resources
        self._applications = None

    @property
    def applications(self):
        """Access the applications resource."""
        if self._applications is None:
            self._applications = ApplicationResource(self)
        return self._applications

    @BaseRateLimiter.rate_limited
    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        Make a rate-limited request to the Certn API.

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            **kwargs: Additional request parameters

        Returns:
            API response data
        """
        try:
            return super()._request(method=method, endpoint=endpoint, **kwargs)
        except Exception as e:
            raise handle_certn_error(e)

    def get_pagination_params(self, page: int, size: int) -> Dict[str, Any]:
        """Get Certn-specific pagination parameters."""
        return {"page": page, "size": size}
