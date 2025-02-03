from typing import Any, Dict, Optional

from usepolvo.arms.base_client import BaseClient
from usepolvo.arms.base_rate_limiter import BaseRateLimiter
from usepolvo.beak.exceptions import AuthenticationError
from usepolvo.tentacles.salesforce.auth import SalesforceAuth
from usepolvo.tentacles.salesforce.config import get_settings
from usepolvo.tentacles.salesforce.exceptions import handle_salesforce_error
from usepolvo.tentacles.salesforce.rate_limiter import SalesforceRateLimiter
from usepolvo.tentacles.salesforce.resources.accounts import AccountResource


class SalesforceClient(BaseClient):
    """
    Salesforce API client with OAuth2 authentication.

    Example usage:
        client = SalesforceClient(
            consumer_key="your-consumer-key",
            consumer_secret="your-consumer-secret",
            redirect_uri="your-redirect-uri"
        )

        # Start OAuth2 flow
        tokens = client.authenticate()

        # Use the client
        accounts = client.accounts.list()
    """

    def __init__(
        self,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
        redirect_uri: Optional[str] = None,
    ):
        """Initialize the Salesforce client."""
        super().__init__()

        # Initialize settings and auth
        self.settings = get_settings()
        self.auth = SalesforceAuth(
            consumer_key=consumer_key, consumer_secret=consumer_secret, redirect_uri=redirect_uri
        )

        # Set API URLs
        self.base_url = self.settings.salesforce_api_base_url

        # Initialize rate limiter
        self.rate_limiter = SalesforceRateLimiter()

        # Initialize resources
        self._accounts = None

        # Handle authentication during initialization
        self._handle_authentication()

    def _handle_authentication(self) -> None:
        """
        Handle the authentication process during client initialization.

        This method ensures that the client is authenticated before use.
        If no access token exists, it starts the OAuth2 flow to obtain one.
        """
        try:
            # Check if we already have a valid access token
            if not self.auth.access_token:
                # Start OAuth2 flow to get tokens
                tokens = self.auth.start_oauth_flow()

                # Log successful authentication (optional)
                print("Salesforce authentication successful")

        except Exception as e:
            # Log authentication failure
            print(f"Salesforce authentication failed: {str(e)}")
            raise AuthenticationError(f"Failed to authenticate with Salesforce: {str(e)}")

    @property
    def accounts(self) -> AccountResource:
        """Access the accounts resource."""
        if self._accounts is None:
            self._accounts = AccountResource(self)
        return self._accounts

    @BaseRateLimiter.rate_limited
    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        if not self.auth.instance_url:
            raise AuthenticationError("Not authenticated. Call authenticate() first")

        # Build the full URL using the instance_url, API version, and endpoint
        url = f"{self.auth.instance_url}/services/data/{self.settings.SALESFORCE_API_VERSION}/{endpoint.lstrip('/')}"

        try:
            # Pass the full URL as the endpoint; do not pass base_url separately
            return super()._request(method=method, endpoint=url, **kwargs)
        except Exception as e:
            raise handle_salesforce_error(e)

    def get_pagination_params(self, page: int, size: int) -> Dict[str, Any]:
        """Get Salesforce-specific pagination parameters using SOQL."""
        return {
            "q": (
                f"SELECT Id, Name, Type, Industry, Rating, Phone, Website, "
                f"AnnualRevenue, NumberOfEmployees, Description FROM Account "
                f"LIMIT {size} OFFSET {(page - 1) * size}"
            )
        }
