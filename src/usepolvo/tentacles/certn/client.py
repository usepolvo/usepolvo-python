from typing import Any, Dict, Optional

import requests

from usepolvo.arms.base_client import BaseClient
from usepolvo.arms.base_rate_limiter import BaseRateLimiter
from usepolvo.tentacles.certn.applications.resource import CertnApplicationResource
from usepolvo.tentacles.certn.config import get_settings
from usepolvo.tentacles.certn.exceptions import handle_certn_error
from usepolvo.tentacles.certn.rate_limiter import CertnRateLimiter


class CertnClient(BaseClient):
    def __init__(self, api_key: Optional[str] = None):
        super().__init__()
        self.settings = get_settings()
        self.api_key = api_key if api_key else self.settings.certn_api_key
        self.base_url = self.settings.certn_base_url
        self.rate_limiter = CertnRateLimiter()
        self._applications = None

    @property
    def applications(self):
        if self._applications is None:
            self._applications = CertnApplicationResource(self)
        return self._applications

    @BaseRateLimiter.rate_limited
    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        kwargs["headers"] = headers

        try:
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise handle_certn_error(e)

    def handle_error(self, e):
        super().handle_error(e)
        # Additional Certn-specific error handling can be added here

    def get_pagination_params(self, page: int, size: int) -> Dict[str, Any]:
        # Implement Certn-specific pagination logic here
        return {"page": page, "size": size}
