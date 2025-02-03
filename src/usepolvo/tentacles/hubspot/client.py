from typing import Any, Callable, Dict, List, Optional

import hubspot
from hubspot.crm.contacts import ApiException

from usepolvo.arms.base_client import BaseClient
from usepolvo.tentacles.hubspot.auth import HubSpotAuth
from usepolvo.tentacles.hubspot.config import get_settings
from usepolvo.tentacles.hubspot.exceptions import handle_hubspot_error
from usepolvo.tentacles.hubspot.rate_limiter import HubSpotRateLimiter
from usepolvo.tentacles.hubspot.resources.contacts import ContactResource
from usepolvo.tentacles.hubspot.resources.deals.resource import DealResource
from usepolvo.tentacles.hubspot.resources.notes import NoteResource
from usepolvo.tentacles.hubspot.resources.tasks import TaskResource


class HubSpotClient(BaseClient):
    """
    HubSpot API client with OAuth2 authentication and rate limiting.

    Example usage:
        client = HubSpotClient(
            client_id="your-client-id",
            client_secret="your-client-secret",
            redirect_uri="your-redirect-uri"
        )

        # Use the client
        contacts = client.contacts.list()
    """

    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        redirect_uri: Optional[str] = None,
        scopes: Optional[List[str]] = None,
    ):
        """Initialize the HubSpot client and handle authentication."""
        super().__init__()

        # Initialize settings
        self.settings = get_settings()
        self.base_url = "https://api.hubapi.com"

        # Initialize auth
        self.auth = HubSpotAuth(
            client_id=client_id or self.settings.HUBSPOT_CLIENT_ID,
            client_secret=client_secret or self.settings.HUBSPOT_CLIENT_SECRET,
            redirect_uri=redirect_uri or self.settings.HUBSPOT_REDIRECT_URI,
            scopes=scopes or self.settings.HUBSPOT_OAUTH_SCOPES,
        )

        # Initialize rate limiter
        self.rate_limiter = HubSpotRateLimiter()

        # Initialize resources
        self._contacts: Optional[ContactResource] = None
        self._tasks: Optional[TaskResource] = None
        self._notes: Optional[NoteResource] = None
        self._deals: Optional[DealResource] = None

        # Handle authentication
        self._handle_authentication()

    def _handle_authentication(self) -> None:
        """Handle the authentication process."""
        # Start OAuth2 flow if we don't have a valid token
        if not self.auth.access_token:
            self.auth.start_auth_flow()

        # Initialize the SDK client
        self.client = hubspot.Client.create(access_token=self.auth.access_token)

    def authenticate(self) -> Dict[str, str]:
        """Start the OAuth2 authentication flow and initialize the SDK client."""
        tokens = self.auth.start_auth_flow()
        self._initialize_sdk_client()
        return tokens

    def _initialize_sdk_client(self):
        """Initialize or refresh the HubSpot SDK client."""
        # If we have a token, use it
        if self.auth.access_token:
            self.client = hubspot.Client.create(access_token=self.auth.access_token)
        else:
            # Otherwise, initialize with a dummy client that will be updated after authentication
            self.client = hubspot.Client()

    def _ensure_client_authenticated(self):
        """Ensure the SDK client is authenticated with a valid token."""
        if not self.client:
            if self.auth.access_token:
                self._initialize_sdk_client()
            else:
                raise ValueError("Client not authenticated. Please call authenticate() first.")

        # Check if token needs refresh
        self.auth.ensure_valid_token(client_id=self.auth.client_id, client_secret=self.auth.client_secret)

        # Reinitialize client if token was refreshed
        if self.client.configuration.access_token != self.auth.access_token:
            self._initialize_sdk_client()

    def rate_limited_execute(self, api_call: Callable) -> Any:
        """
        Execute a HubSpot SDK function with rate limiting and auth checks.
        """
        # Pass the refresh function to ensure_valid_token
        self.auth.ensure_valid_token(
            self.auth.refresh_token, client_id=self.auth.client_id, client_secret=self.auth.client_secret
        )

        # Reinitialize client if token was refreshed
        if self.client.access_token != self.auth.access_token:
            self._initialize_sdk_client()

        # Apply rate limiting and execute the API call
        self.rate_limiter.wait_if_needed()
        try:
            return api_call()
        except ApiException as e:
            raise handle_hubspot_error(e)
        except Exception as e:
            self.handle_error(e)
            raise

    @property
    def contacts(self) -> ContactResource:
        """Access the contacts resource."""
        if self._contacts is None:
            self._contacts = ContactResource(self)
        return self._contacts

    @property
    def tasks(self) -> TaskResource:
        """Access the tasks resource."""
        if self._tasks is None:
            self._tasks = TaskResource(self)
        return self._tasks

    @property
    def notes(self) -> NoteResource:
        """Access the notes resource."""
        if self._notes is None:
            self._notes = NoteResource(self)
        return self._notes

    @property
    def deals(self) -> DealResource:
        """Access the deals resource."""
        if self._deals is None:
            self._deals = DealResource(self)
        return self._deals

    def get_pagination_params(self, limit: int = 10, after: Optional[str] = None) -> Dict[str, Any]:
        """Get HubSpot-specific pagination parameters."""
        params = {"limit": limit}
        if after:
            params["after"] = after
        return params

    def _request(self, *args, **kwargs):
        """
        Override parent's _request method to prevent direct API calls.
        HubSpot SDK should be used instead.
        """
        raise NotImplementedError("Direct API requests are not supported. Use the HubSpot SDK methods instead.")
