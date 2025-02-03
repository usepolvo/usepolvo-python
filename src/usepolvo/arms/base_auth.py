# src/usepolvo/arms/base_auth.py

import time
from typing import Dict, Optional

import requests

from usepolvo.beak.exceptions import AuthenticationError


class BaseAuth:
    """
    Base authentication class that provides a foundation for different auth methods.
    Specific authentication implementations (API key, OAuth2, etc) should extend this class.
    """

    def __init__(self):
        # Basic auth state
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.token_expiry: float = 0

    def get_auth_headers(self) -> Dict[str, str]:
        """
        Get authentication headers for API requests.
        Should be implemented by child classes.

        Returns:
            A dictionary with authentication headers.

        Raises:
            AuthenticationError: If authentication credentials are not available.
        """
        raise NotImplementedError("Subclasses must implement get_auth_headers()")

    def _make_token_request(self, token_url: str, token_data: Dict[str, str]) -> Dict[str, str]:
        """
        Makes a POST request to the token endpoint and updates internal token state.

        Args:
            token_url: The URL to which the token request is sent.
            token_data: The data payload for the token request.

        Returns:
            The token response as a dictionary.

        Raises:
            AuthenticationError: If the token request fails.
        """
        response = requests.post(token_url, data=token_data)
        if response.status_code != 200:
            raise AuthenticationError(f"Token request failed: {response.text}")
        token_response = response.json()
        self.access_token = token_response.get("access_token")
        self.refresh_token = token_response.get("refresh_token", self.refresh_token)
        expires_in = token_response.get("expires_in", 3600)
        self.token_expiry = time.time() + expires_in
        return token_response

    def validate_credentials(self) -> bool:
        """
        Validate that required authentication credentials are available.
        Should be implemented by child classes that need validation.

        Returns:
            bool: True if credentials are valid, False otherwise.
        """
        return True

    def clear_credentials(self) -> None:
        """Clear all authentication credentials."""
        self.access_token = None
        self.refresh_token = None
        self.token_expiry = 0

    def ensure_valid_token(self, refresh_func, *args, **kwargs):
        """
        Ensures that a valid access token is available. If the token has expired,
        calls the provided refresh function to update it.

        Args:
            refresh_func: A callable that performs a token refresh.
            *args, **kwargs: Arguments to pass to the refresh function.
        """
        if not self.access_token or time.time() >= self.token_expiry:
            refresh_func(*args, **kwargs)
