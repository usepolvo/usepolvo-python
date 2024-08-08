# usepolvo/tentacles/certn/client.py

from functools import wraps
from typing import Any, Dict

import requests

from usepolvo.arms.base_client import BaseClient
from usepolvo.tentacles.certn.applications.resource import CertnApplicationResource
from usepolvo.tentacles.certn.config import get_settings
from usepolvo.tentacles.certn.exceptions import handle_certn_error
from usepolvo.tentacles.certn.rate_limiter import CertnRateLimiter


class CertnClient(BaseClient):
    def __init__(self, api_key: str | None = None):
        super().__init__()
        certn_settings = get_settings()
        self.api_key = api_key if api_key else certn_settings.certn_api_key
        self.base_url = certn_settings.certn_base_url
        self.rate_limiter = CertnRateLimiter()
        self._applications = None

    @property
    def applications(self):
        if self._applications is None:
            self._applications = CertnApplicationResource(self)
        return self._applications

    def rate_limited_execute(self, method, *args, **kwargs):
        @wraps(method)
        def wrapper(*args, **kwargs):
            self.rate_limiter.wait_if_needed()
            return method(*args, **kwargs)

        return wrapper(*args, **kwargs)

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = self.rate_limited_execute(requests.request, method, url, headers=headers, **kwargs)
        try:
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise handle_certn_error(e)

    def handle_error(self, e):
        super().handle_error(e)
        # Additional Certn-specific error handling can be added here
