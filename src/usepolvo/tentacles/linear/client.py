from typing import Any, Dict, Optional

from usepolvo.arms.base_graphql_client import BaseGraphQLClient
from usepolvo.arms.base_rate_limiter import BaseRateLimiter
from usepolvo.tentacles.linear.config import get_settings
from usepolvo.tentacles.linear.exceptions import handle_linear_error
from usepolvo.tentacles.linear.rate_limiter import LinearRateLimiter
from usepolvo.tentacles.linear.resources.issues.resource import LinearIssueResource


class LinearClient(BaseGraphQLClient):
    def __init__(self, api_key: Optional[str] = None):
        self.settings = get_settings()
        self.api_key = api_key if api_key else self.settings.linear_api_key
        self.base_url = self.settings.linear_base_url
        self.rate_limiter = LinearRateLimiter()
        self._issues = None
        super().__init__()

    def get_auth_headers(self) -> Dict[str, str]:
        """Provide Linear-specific authentication headers."""
        if self.api_key:
            return {"Authorization": f"{self.api_key}"}
        return {"Authorization": f"Bearer {self.api_key}"}

    @property
    def issues(self):
        if self._issues is None:
            self._issues = LinearIssueResource(self)
        return self._issues

    def handle_error(self, e):
        """Override error handling with Linear-specific logic."""
        raise handle_linear_error(e)

    def _get_resource_fields(self, resource_type: str) -> str:
        """Override to specify Linear-specific fields for each resource type."""
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
        Adapter method to maintain compatibility with REST-like interface.
        Translates REST-style requests into GraphQL queries.
        """
        query, variables = self._convert_rest_to_graphql(method, endpoint, **kwargs)
        return self.execute_query(query, variables)
