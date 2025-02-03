# src/usepolvo/tentacles/hubspot/auth.py

import time
from typing import Dict, List, Optional
from urllib.parse import parse_qs, urlparse

import requests

from usepolvo.arms.base_auth import BaseAuth
from usepolvo.beak.exceptions import AuthenticationError
from usepolvo.ink.tokens import SecureTokenStore
from usepolvo.tentacles.hubspot.config import get_settings


class HubSpotAuth(BaseAuth):
    """HubSpot OAuth2 authentication."""

    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        redirect_uri: Optional[str] = None,
        scopes: Optional[List[str]] = None,
    ):
        super().__init__()
        self.settings = get_settings()

        # Set OAuth2 endpoints
        self.auth_url = self.settings.HUBSPOT_OAUTH_URL
        self.token_url = self.settings.HUBSPOT_OAUTH_TOKEN_URL

        # Set credentials
        self.client_id = client_id or self.settings.HUBSPOT_CLIENT_ID
        self.client_secret = client_secret or self.settings.HUBSPOT_CLIENT_SECRET
        self.redirect_uri = redirect_uri or self.settings.HUBSPOT_REDIRECT_URI
        self.scopes = scopes or self.settings.HUBSPOT_OAUTH_SCOPES

        # Initialize token persistence if encryption key available
        encryption_key = getattr(self.settings, "ENCRYPTION_KEY", None)
        if encryption_key:
            self.token_store = SecureTokenStore(encryption_key)
            stored_tokens = self.token_store.load_tokens("hubspot")
            if stored_tokens:
                self.access_token = stored_tokens.get("access_token")
                self.refresh_token = stored_tokens.get("refresh_token")
                self.token_expiry = stored_tokens.get("token_expiry", 0)
        else:
            self.token_store = None

        if not all([self.client_id, self.client_secret, self.redirect_uri]):
            raise AuthenticationError("client_id, client_secret, and redirect_uri are required")

    def start_auth_flow(self) -> Dict[str, str]:
        """Start OAuth2 flow and return tokens."""
        # Create scope string
        scope_string = " ".join(self.scopes)

        # Build auth URL
        auth_url = (
            f"{self.auth_url}?client_id={self.client_id}"
            f"&redirect_uri={self.redirect_uri}"
            f"&scope={scope_string}"
            f"&response_type=code"
        )

        print("Please visit this URL to authenticate:")
        print(auth_url)
        print("\nAfter authenticating, paste the complete redirect URL here:")
        redirect_url = input().strip()

        # Parse auth code from redirect
        parsed_url = urlparse(redirect_url)
        query_params = parse_qs(parsed_url.query)
        if "code" not in query_params:
            raise AuthenticationError("Authorization code not found in redirect URL")
        code = query_params["code"][0]

        # Exchange code for tokens
        token_data = {
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri,
            "code": code,
        }

        response = requests.post(self.token_url, data=token_data)
        if response.status_code != 200:
            raise AuthenticationError(f"Token request failed: {response.text}")

        token_response = response.json()

        # Set token state
        self.access_token = token_response.get("access_token")
        self.refresh_token = token_response.get("refresh_token")
        self.token_expiry = time.time() + token_response.get("expires_in", 3600)

        # Persist tokens if storage available
        if self.token_store:
            self.token_store.save_tokens(
                "hubspot",
                {
                    "access_token": self.access_token,
                    "refresh_token": self.refresh_token,
                    "token_expiry": self.token_expiry,
                },
            )

        return token_response

    def refresh_token(self, client_id: str, client_secret: str) -> Dict[str, str]:
        """Refresh access token using refresh token."""
        if not self.refresh_token:
            raise AuthenticationError("No refresh token available")

        token_data = {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": self.refresh_token,
        }

        response = requests.post(self.token_url, data=token_data)
        if response.status_code != 200:
            raise AuthenticationError(f"Token refresh failed: {response.text}")

        token_response = response.json()

        # Update token state
        self.access_token = token_response.get("access_token")
        self.refresh_token = token_response.get("refresh_token", self.refresh_token)
        self.token_expiry = time.time() + token_response.get("expires_in", 3600)

        # Persist updated tokens
        if self.token_store:
            self.token_store.save_tokens(
                "hubspot",
                {
                    "access_token": self.access_token,
                    "refresh_token": self.refresh_token,
                    "token_expiry": self.token_expiry,
                },
            )

        return token_response

    def get_auth_headers(self) -> Dict[str, str]:
        """Get authentication headers for requests."""
        if not self.access_token or time.time() >= self.token_expiry:
            self.refresh_token(self.client_id, self.client_secret)
        return {"Authorization": f"Bearer {self.access_token}"}
