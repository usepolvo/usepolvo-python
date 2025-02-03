from typing import Any, Dict, Optional

import requests
from cachetools import TTLCache

from usepolvo.arms.base_auth import BaseAuth
from usepolvo.beak.config import get_settings
from usepolvo.beak.exceptions import APIError, AuthenticationError


class BaseClient:
    """
    Base client for API integrations with built-in authentication, caching,
    error handling, and common functionality.
    """

    def __init__(self):
        """Initialize the base client with settings and cache."""
        self.settings = get_settings()
        self.cache = TTLCache(maxsize=self.settings.CACHE_SIZE, ttl=self.settings.CACHE_TTL)
        self.pagination_method = self.settings.PAGINATION_METHOD

        # Only set these if they haven’t already been defined by a child class
        if not hasattr(self, "base_url"):
            self.base_url: Optional[str] = None
        if not hasattr(self, "auth"):
            self.auth: Optional[BaseAuth] = None  # type: ignore

    def _request(
        self,
        method: str,
        endpoint: str,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        use_cache: bool = True,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Make an authenticated HTTP request.

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            client_id: OAuth2 client ID (if using OAuth)
            client_secret: OAuth2 client secret (if using OAuth)
            use_cache: Whether to use request caching
            **kwargs: Additional request parameters

        Returns:
            API response data

        Raises:
            APIError: If the request fails
            AuthenticationError: If authentication fails
        """
        if not self.base_url:
            raise ValueError("base_url must be set by the child class")

        # Check cache for GET requests
        cache_key = None
        if method == "GET" and use_cache:
            cache_key = f"{method}:{endpoint}:{str(kwargs)}"
            if cache_key in self.cache:
                return self.cache[cache_key]

        # Build request URL
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"

        # Get authentication headers
        headers = {}
        if self.auth:
            if client_id and client_secret:
                self.auth.ensure_valid_token(client_id, client_secret)
            headers = self.auth.get_auth_headers()

        # Add content type for JSON requests
        headers["Content-Type"] = "application/json"

        # Merge with any custom headers
        if "headers" in kwargs:
            headers.update(kwargs.pop("headers"))
        kwargs["headers"] = headers

        try:
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()
            data = response.json()

            # Cache successful GET responses
            if cache_key:
                self.cache[cache_key] = data

            return data

        except requests.exceptions.HTTPError as e:
            if e.response.status_code in (401, 403):
                raise AuthenticationError(f"Authentication failed: {e.response.text}")
            raise APIError(f"Request failed: {e.response.text}")

        except requests.exceptions.RequestException as e:
            raise APIError(f"Request failed: {str(e)}")

        except Exception as e:
            self.handle_error(e)
            raise

    def handle_error(self, error: Exception):
        """
        Handle errors from API requests.
        Can be overridden by child classes for custom error handling.

        Args:
            error: The exception that occurred
        """
        error_message = f"Error occurred: {str(error)}"
        # Log the error (implement logging in the future)
        print(error_message)

    def clear_cache(self):
        """Clear the request cache."""
        self.cache.clear()

    def get_pagination_params(self, page: Optional[int] = None, size: Optional[int] = None) -> Dict[str, Any]:
        """
        Get pagination parameters based on the configured pagination method.
        Can be overridden by child classes for custom pagination.

        Args:
            page: Page number (optional)
            size: Page size (optional)

        Returns:
            Dictionary of pagination parameters
        """
        if not page and not size:
            return {}

        if self.pagination_method == "offset":
            return {
                "offset": (page - 1) * size if page else 0,
                "limit": size if size else self.settings.DEFAULT_PAGE_SIZE,
            }
        elif self.pagination_method == "page":
            return {
                "page": page if page else 1,
                "per_page": size if size else self.settings.DEFAULT_PAGE_SIZE,
            }
        else:
            return {
                "limit": size if size else self.settings.DEFAULT_PAGE_SIZE,
                "after": None,  # Cursor-based pagination requires implementation by child classes
            }
