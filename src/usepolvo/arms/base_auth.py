import time
from typing import Dict, Optional

import requests

from usepolvo.beak.exceptions import AuthenticationError


class BaseAuth:
    """
    Base authentication class that provides common methods for handling
    OAuth2 token requests and managing token state.

    Provider-specific flows should be implemented in the child classes.
    """

    def __init__(self):
        # OAuth2 token state
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.token_expiry: float = 0

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

    def get_auth_headers(self) -> Dict[str, str]:
        """
        Returns the authorization headers needed for API requests.

        Returns:
            A dictionary with the 'Authorization' header.

        Raises:
            AuthenticationError: If no access token is present.
        """
        if not self.access_token:
            raise AuthenticationError("Not authenticated")
        return {"Authorization": f"Bearer {self.access_token}"}
