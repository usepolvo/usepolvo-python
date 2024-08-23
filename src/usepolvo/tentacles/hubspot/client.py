from functools import wraps
from typing import Optional

import hubspot

from usepolvo.arms.base_client import BaseClient
from usepolvo.tentacles.hubspot.config import get_settings
from usepolvo.tentacles.hubspot.contacts.resource import HubSpotContactResource
from usepolvo.tentacles.hubspot.exceptions import HubSpotError
from usepolvo.tentacles.hubspot.notes.resource import HubSpotNoteResource
from usepolvo.tentacles.hubspot.rate_limiter import HubSpotRateLimiter
from usepolvo.tentacles.hubspot.tasks.resource import HubSpotTaskResource


class HubSpotClient(BaseClient):
    def __init__(self, api_key: Optional[str] = None):
        super().__init__()
        settings = get_settings()
        self.api_key = api_key if api_key else settings.hubspot_api_key
        self.client = hubspot.Client.create(api_key=self.api_key)
        self.rate_limiter = HubSpotRateLimiter()
        self._contacts = None
        self._tasks = None
        self._notes = None

    @property
    def contacts(self):
        if self._contacts is None:
            self._contacts = HubSpotContactResource(self)
        return self._contacts

    @property
    def tasks(self):
        if self._tasks is None:
            self._tasks = HubSpotTaskResource(self)
        return self._tasks

    @property
    def notes(self):
        if self._notes is None:
            self._notes = HubSpotNoteResource(self)
        return self._notes

    def rate_limited_execute(self, method, *args, **kwargs):
        @wraps(method)
        def wrapper(*args, **kwargs):
            self.rate_limiter.wait_if_needed()
            return method(*args, **kwargs)

        return wrapper(*args, **kwargs)

    def handle_error(self, e):
        super().handle_error(e)
        # Additional HubSpot-specific error handling can be added here
