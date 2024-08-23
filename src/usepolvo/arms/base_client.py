from cachetools import TTLCache

from usepolvo.beak.config import get_settings
from usepolvo.beak.enums import PaginationMethod


class BaseClient:
    def __init__(self):
        self.settings = get_settings()
        self.cache = TTLCache(maxsize=self.settings.cache_size, ttl=self.settings.cache_ttl)
        self.pagination_method = self.settings.pagination_method

    def handle_error(self, e):
        # Base error handling logic
        print(f"Error: {e}")
