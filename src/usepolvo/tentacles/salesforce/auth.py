import time
from typing import Dict, Optional
from urllib.parse import parse_qs, urlparse

from usepolvo.arms.base_auth import BaseAuth
from usepolvo.beak.exceptions import AuthenticationError
from usepolvo.tentacles.salesforce.config import get_settings


class SalesforceAuth(BaseAuth):
    """
    Salesforce OAuth2 authentication implementation using the implicit grant flow.

    This class builds the authorization URL (with response_type=token), prompts the user
    to authenticate, and then parses the URL fragment from the redirect to extract the token(s).
    It also implements a refresh method using the BaseAuth _make_token_request.
    """

    def __init__(
        self,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
        redirect_uri: Optional[str] = None,
    ):
        super().__init__()
        self.settings = get_settings()
        self.consumer_key = consumer_key or self.settings.SALESFORCE_CONSUMER_KEY
        self.consumer_secret = consumer_secret or self.settings.SALESFORCE_CONSUMER_SECRET
        self.redirect_uri = redirect_uri or self.settings.SALESFORCE_REDIRECT_URI

        # Set OAuth2 endpoints from settings
        self.auth_url = (
            self.settings.salesforce_auth_url
        )  # e.g., "https://login.salesforce.com/services/oauth2/authorize"
        self.token_url = (
            self.settings.salesforce_token_url
        )  # e.g., "https://login.salesforce.com/services/oauth2/token"

        # Salesforce-specific property
        self.instance_url: Optional[str] = None

        if not all([self.consumer_key, self.consumer_secret, self.redirect_uri]):
            raise AuthenticationError("consumer_key, consumer_secret, and redirect_uri are required")

    def start_oauth_flow(self) -> Dict[str, str]:
        """
        Initiates the Salesforce OAuth2 implicit flow.

        1. Constructs the authorization URL with response_type=token.
        2. Prompts the user to authenticate and paste the entire redirect URL.
        3. Parses the URL fragment to extract access token and related parameters.

        Returns:
            A dictionary containing the access token, refresh token (if provided), instance URL, and token expiry.
        """
        # Construct the authorization URL (using implicit flow)
        auth_url = (
            f"{self.auth_url}?response_type=token"
            f"&client_id={self.consumer_key}"
            f"&redirect_uri={self.redirect_uri}"
        )

        print("Please visit the following URL to authenticate with Salesforce:")
        print(auth_url)
        print("\nAfter authenticating, you will be redirected. Paste the entire redirect URL here:")
        redirect_url = input().strip()

        # Parse the URL fragment where Salesforce returns the tokens
        parsed_url = urlparse(redirect_url)
        fragment = parse_qs(parsed_url.fragment)

        if "access_token" not in fragment:
            raise AuthenticationError("No access token found in the redirect URL fragment.")

        # Extract tokens and instance URL (if provided)
        self.access_token = fragment["access_token"][0]
        self.refresh_token = fragment.get("refresh_token", [None])[0]
        self.instance_url = fragment.get("instance_url", [None])[0]

        # Calculate token expiry using the issued_at parameter (in milliseconds) if available.
        try:
            issued_at_ms = int(fragment.get("issued_at", [str(int(time.time() * 1000))])[0])
        except ValueError:
            issued_at_ms = int(time.time() * 1000)
        issued_at = issued_at_ms / 1000.0  # convert to seconds

        # Salesforce implicit flow tokens often have a default lifetime (e.g., 3600 seconds)
        expires_in = 3600
        self.token_expiry = issued_at + expires_in

        return {
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "instance_url": self.instance_url,
            "expires_in": expires_in,
        }

    def refresh_token_auth(self) -> Dict[str, str]:
        """
        Refresh the Salesforce access token using the refresh token.

        Utilizes the _make_token_request method from BaseAuth.
        """
        if not self.refresh_token:
            raise AuthenticationError("No refresh token available")

        token_data = {
            "grant_type": "refresh_token",
            "client_id": self.consumer_key,
            "client_secret": self.consumer_secret,
            "refresh_token": self.refresh_token,
        }

        token_response = self._make_token_request(self.token_url, token_data)
        # Update instance_url if provided in the refresh response
        self.instance_url = token_response.get("instance_url", self.instance_url)
        return token_response

    def get_auth_headers(self) -> Dict[str, str]:
        """
        Returns the authentication headers for Salesforce API requests.
        """
        if not self.access_token:
            raise AuthenticationError("Not authenticated")
        return {"Authorization": f"Bearer {self.access_token}", "Content-Type": "application/json"}
