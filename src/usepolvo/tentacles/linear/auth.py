from typing import Dict, List, Optional

from usepolvo.arms.base_auth import BaseAuth
from usepolvo.beak.exceptions import AuthenticationError
from usepolvo.tentacles.linear.config import get_settings


class LinearAuth(BaseAuth):
    """Linear authentication implementation supporting both API key and OAuth."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        redirect_uri: Optional[str] = None,
        scopes: Optional[List[str]] = None,
    ):
        super().__init__()
        self.settings = get_settings()

        # Set credentials (using provided values or falling back to settings)
        self.api_key = api_key or self.settings.LINEAR_API_KEY
        self.client_id = client_id or self.settings.LINEAR_CLIENT_ID
        self.client_secret = client_secret or self.settings.LINEAR_CLIENT_SECRET
        self.redirect_uri = redirect_uri or self.settings.LINEAR_REDIRECT_URI

        # If client credentials are provided, set the OAuth2 endpoints and scopes.
        if self.client_id and self.client_secret:
            self.auth_url = self.settings.LINEAR_OAUTH_URL
            self.token_url = self.settings.LINEAR_OAUTH_TOKEN_URL
            self.scopes = scopes or self.settings.LINEAR_OAUTH_SCOPES

            # Automatically initiate the OAuth2 flow if no access token exists.
            if not self.access_token:
                # This will prompt the user to complete the OAuth2 flow and update self.access_token.
                self.start_oauth_flow()

        # If neither an API key nor client credentials are provided, raise an error.
        if not self.api_key and not (self.client_id and self.client_secret):
            raise AuthenticationError("Either API key or client credentials (ID and secret) are required")

    def get_auth_headers(self) -> Dict[str, str]:
        """Get Linear-specific authentication headers."""
        if self.api_key:
            return {"Authorization": self.api_key}
        elif self.access_token:
            return {"Authorization": f"Bearer {self.access_token}"}
        else:
            raise AuthenticationError("No valid authentication credentials")

    def start_oauth_flow(self) -> Dict[str, str]:
        """Start the OAuth2 flow if using OAuth authentication."""
        if not (self.client_id and self.client_secret):
            raise AuthenticationError("Client ID and secret required for OAuth flow")

        return self.authenticate(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            scopes=self.scopes,
        )
