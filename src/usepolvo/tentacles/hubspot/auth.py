from typing import Dict, List, Optional
from urllib.parse import parse_qs, urlparse

import requests

from usepolvo.arms.base_auth import BaseAuth
from usepolvo.beak.exceptions import AuthenticationError
from usepolvo.tentacles.hubspot.config import get_settings


class HubSpotAuth(BaseAuth):
    """HubSpot-specific authentication implementation using the authorization code flow."""

    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        redirect_uri: Optional[str] = None,
        scopes: Optional[List[str]] = None,
    ):
        super().__init__()
        self.settings = get_settings()

        # Set OAuth2 endpoints from settings
        self.auth_url = self.settings.HUBSPOT_OAUTH_URL
        self.token_url = self.settings.HUBSPOT_OAUTH_TOKEN_URL

        # Set credentials and parameters
        self.client_id = client_id or self.settings.HUBSPOT_CLIENT_ID
        self.client_secret = client_secret or self.settings.HUBSPOT_CLIENT_SECRET
        self.redirect_uri = redirect_uri or self.settings.HUBSPOT_REDIRECT_URI
        self.scopes = scopes or self.settings.HUBSPOT_OAUTH_SCOPES

        if not all([self.client_id, self.client_secret, self.redirect_uri]):
            raise AuthenticationError("client_id, client_secret, and redirect_uri are required")

    def start_auth_flow(self) -> Dict[str, str]:
        """
        Initiates the OAuth2 flow by constructing the HubSpot authorization URL,
        prompting the user to authenticate, and parsing the redirect response.
        Then exchanges the authorization code for tokens.
        """
        # Create the scope string (HubSpot expects scopes to be space-delimited)
        scope_string = "%20".join(self.scopes)

        # Construct the HubSpot authorization URL
        auth_url = (
            f"{self.auth_url}?client_id={self.client_id}"
            f"&redirect_uri={self.redirect_uri}"
            f"&scope={scope_string}"
            f"&response_type=code"
        )

        print("Please visit the following URL to authenticate:")
        print(auth_url)
        print("\nAfter authenticating, you will be redirected to a URL. Paste the entire redirect URL here:")
        redirect_url = input().strip()

        # Parse the URL to extract the authorization code
        parsed_url = urlparse(redirect_url)
        query_params = parse_qs(parsed_url.query)
        if "code" not in query_params:
            raise AuthenticationError("Authorization code not found in the redirect URL")
        code = query_params["code"][0]

        # Prepare token request data and exchange the code for tokens
        token_data = {
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri,
            "code": code,
        }
        token_response = self._make_token_request(self.token_url, token_data)
        return token_response

    def refresh_token(self, client_id: str, client_secret: str) -> Dict[str, str]:
        """
        Refresh the HubSpot access token using the refresh token.
        """
        if not self.refresh_token:
            raise AuthenticationError("No refresh token available")

        token_data = {
            "grant_type": "refresh_token",
            "client_id": self.client_id,  # or use client_id argument if needed
            "client_secret": self.client_secret,  # or use client_secret argument if needed
            "refresh_token": self.refresh_token,
        }

        token_response = self._make_token_request(self.token_url, token_data)
        return token_response
