from cachetools import TTLCache

from .config import get_settings


class BaseClient:
    def __init__(self):
        settings = get_settings()
        self.cache = TTLCache(maxsize=settings.cache_size, ttl=settings.cache_ttl)

    def handle_error(self, e):
        # Base error handling logic
        print(f"Error: {e}")
