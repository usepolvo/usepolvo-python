from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Tuple

from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport

from usepolvo.arms.base_client import BaseClient


class BaseGraphQLClient(BaseClient, ABC):
    """Base client for GraphQL-based API integrations."""

    def __init__(self):
        super().__init__()
        self._client = None
        self._setup_graphql_client()

    def _setup_graphql_client(self):
        """Initialize the GraphQL client with authentication headers."""
        if not self.base_url:
            raise ValueError("base_url must be set before initializing the GraphQL client")

        transport = RequestsHTTPTransport(
            url=self.base_url,
            headers=self.auth.get_auth_headers(),
            use_json=True,
        )
        self._client = Client(transport=transport, fetch_schema_from_transport=True)

    def execute_query(self, query: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute a GraphQL query with error handling.

        :param query: The GraphQL query string
        :param variables: Optional variables for the query
        :return: The query result
        """
        if not self._client:
            raise RuntimeError("GraphQL client not initialized")

        try:
            result = self._client.execute(gql(query), variable_values=variables)
            return result
        except Exception as e:
            self.handle_error(e)

    def _convert_rest_to_graphql(self, method: str, endpoint: str, **kwargs) -> Tuple[str, Dict[str, Any]]:
        """
        Convert REST-style requests to GraphQL queries.

        :param method: HTTP method
        :param endpoint: The endpoint path
        :param kwargs: Additional arguments
        :return: Tuple of (query_string, variables)
        """
        parts = endpoint.strip("/").split("/")
        resource_type = parts[0]
        resource_id = parts[1] if len(parts) > 1 else None
        request_payload = kwargs.get("json", {})
        request_params = kwargs.get("params", {})

        if method == "GET":
            if resource_id:
                return self._build_get_query(resource_type), {"id": resource_id}
            return self._build_list_query(resource_type, request_params), request_params
        elif method == "POST":
            return self._build_create_mutation(resource_type), request_payload
        elif method == "PUT":
            return self._build_update_mutation(resource_type), {"id": resource_id, **request_payload}
        elif method == "DELETE":
            return self._build_delete_mutation(resource_type, resource_id), {"id": resource_id}

        raise ValueError(f"Unsupported method: {method}")

    def _build_get_query(self, resource_type: str) -> str:
        """Build a GraphQL query for fetching a single resource."""
        return f"""
            query Get{resource_type.title()}($id: String!) {{
                {resource_type}(id: $id) {{
                    id
                    {self._get_resource_fields(resource_type)}
                }}
            }}
        """

    def _build_list_query(self, resource_type: str, params: Dict[str, Any]) -> str:
        """Build a GraphQL query for listing resources."""
        return f"""
            query List{resource_type.title()}s($first: Int, $after: String) {{
                {resource_type}s(first: $first, after: $after) {{
                    nodes {{
                        id
                        {self._get_resource_fields(resource_type)}
                    }}
                    pageInfo {{
                        hasNextPage
                        endCursor
                    }}
                }}
            }}
        """

    def _build_create_mutation(self, resource_type: str) -> str:
        """Build a GraphQL mutation for creating a resource."""
        return f"""
            mutation Create{resource_type.title()}($input: Create{resource_type.title()}Input!) {{
                create{resource_type.title()}(input: $input) {{
                    id
                    {self._get_resource_fields(resource_type)}
                }}
            }}
        """

    def _build_update_mutation(self, resource_type: str) -> str:
        """Build a GraphQL mutation for updating a resource."""
        resource_title = resource_type.title()
        return f"""
            mutation {resource_title}Update($id: String!, $input: {resource_title}UpdateInput!) {{
                {resource_type}Update(id: $id, input: $input) {{
                    issue {{ id }}
                }}
            }}
        """

    def _build_delete_mutation(self, resource_type: str, resource_id: str) -> str:
        """Build a GraphQL mutation for deleting a resource."""
        return f"""
            mutation Delete{resource_type.title()}($id: ID!) {{
                delete{resource_type.title()}(id: $id) {{
                    success
                }}
            }}
        """

    def _get_resource_fields(self, resource_type: str) -> str:
        """
        Get the fields to be queried for a specific resource type.
        Should be overridden by child classes to specify fields for each resource.
        """
        return """
            title
            description
        """
