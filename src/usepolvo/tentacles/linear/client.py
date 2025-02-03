from typing import Any, Dict, Optional

from usepolvo.arms.base_graphql_client import BaseGraphQLClient
from usepolvo.arms.base_rate_limiter import BaseRateLimiter
from usepolvo.tentacles.linear.auth import LinearAuth
from usepolvo.tentacles.linear.config import get_settings
from usepolvo.tentacles.linear.exceptions import handle_linear_error
from usepolvo.tentacles.linear.rate_limiter import LinearRateLimiter
from usepolvo.tentacles.linear.resources.issues import IssueResource


class LinearClient(BaseGraphQLClient):
    """
    Linear API client supporting both API key and OAuth authentication.

    Example usage:
        # Using API key
        client = LinearClient(api_key="your-api-key")

        # Using OAuth
        client = LinearClient(
            client_id="your-client-id",
            client_secret="your-client-secret"
        )
        tokens = client.authenticate()  # Starts OAuth flow
    """

    def __init__(
        self, api_key: Optional[str] = None, client_id: Optional[str] = None, client_secret: Optional[str] = None
    ):
        """Initialize the Linear client."""
        self.settings = get_settings()
        self.base_url = self.settings.LINEAR_BASE_URL

        # Initialize auth
        self.auth = LinearAuth(api_key=api_key, client_id=client_id, client_secret=client_secret)

        # Initialize rate limiter
        self.rate_limiter = LinearRateLimiter()

        # Initialize resources
        self._issues = None

        super().__init__()

    def authenticate(self) -> Dict[str, str]:
        """Start the OAuth authentication flow if using OAuth."""
        return self.auth.start_oauth_flow()

    @property
    def issues(self) -> IssueResource:
        """Access the issues resource."""
        if self._issues is None:
            self._issues = IssueResource(self)
        return self._issues

    def _get_resource_fields(self, resource_type: str) -> str:
        """Get Linear-specific fields for each resource type."""
        if resource_type == "issue":
            return """
                title
                description
                state {
                    id
                    name
                }
                assignee {
                    id
                    name
                }
            """
        return super()._get_resource_fields(resource_type)

    @BaseRateLimiter.rate_limited
    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        Make a rate-limited request to the Linear API.
        Translates REST-style requests into GraphQL queries.
        """
        try:
            query, variables = self._convert_rest_to_graphql(method, endpoint, **kwargs)
            return self.execute_query(query, variables)
        except Exception as e:
            raise handle_linear_error(e)
