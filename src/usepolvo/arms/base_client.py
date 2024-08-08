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

    def get_pagination_params(
        self, page: int = 1, size: int = 10, starting_after: str = None, ending_before: str = None
    ) -> dict:
        if self.pagination_method == PaginationMethod.OFFSET_LIMIT:
            return {"offset": (page - 1) * size, "limit": size}
        elif self.pagination_method == PaginationMethod.PAGE_SIZE:
            return {"page": page, "size": size}
        elif self.pagination_method == PaginationMethod.PAGE:
            return {"page": page}
        elif self.pagination_method == PaginationMethod.CURSOR:
            params = {"limit": size}
            if starting_after:
                params["starting_after"] = starting_after
            if ending_before:
                params["ending_before"] = ending_before
            return params
        else:
            raise ValueError(f"Unsupported pagination method: {self.pagination_method}")
