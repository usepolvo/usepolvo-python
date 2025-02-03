from typing import Any, Dict

from usepolvo.arms.base_resource import BaseResource
from usepolvo.beak.exceptions import ResourceNotFoundError, ValidationError
from usepolvo.tentacles.linear.resources.issues.schemas import Issue, IssueListResponse


class IssueResource(BaseResource):
    def __init__(self, client):
        super().__init__(client)
        self.resource_type = "issue"

    def list(self, page: int = 1, size: int = 10) -> IssueListResponse:
        """
        List issues with GraphQL pagination.
        """
        try:
            response = self.client._request(
                "GET", self.resource_type, params={"first": size, "after": None}  # GraphQL pagination
            )

            result = IssueListResponse(**response[f"{self.resource_type}s"])
            return result
        except Exception as e:
            self.client.handle_error(e)

    def get(self, resource_id: str) -> Issue:
        """
        Get a single issue by ID.
        """
        try:
            response = self.client._request("GET", f"{self.resource_type}/{resource_id}")
            if not response.get(self.resource_type):
                raise ResourceNotFoundError(f"Issue with ID {resource_id} not found")
            return Issue(**response[self.resource_type])
        except Exception as e:
            self.client.handle_error(e)

    def create(self, data: Dict[str, Any]) -> Issue:
        """
        Create a new issue.
        """
        try:
            response = self.client._request(
                "POST", self.resource_type, json={"input": self._prepare_request_data(data)}
            )
            return Issue(**response[f"create{self.resource_type.title()}"])
        except Exception as e:
            raise ValidationError(f"Invalid data for creating issue: {str(e)}")

    def update(self, resource_id: str, data: Dict[str, Any]) -> Issue:
        """
        Update an existing issue.
        """
        try:
            response = self.client._request(
                "PUT", f"{self.resource_type}/{resource_id}", json={"input": self._prepare_request_data(data)}
            )
            return Issue(**response[f"{self.resource_type}Update"][self.resource_type])
        except Exception as e:
            self.client.handle_error(e)

    def delete(self, resource_id: str) -> bool:
        """
        Delete an issue.
        """
        try:
            response = self.client._request("DELETE", f"{self.resource_type}/{resource_id}")
            return response[f"delete{self.resource_type.title()}"]["success"]
        except Exception as e:
            self.client.handle_error(e)

    def _prepare_request_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepare data for GraphQL mutations.
        """
        # Convert snake_case to camelCase and handle any specific Linear API requirements
        prepared_data = super()._prepare_request_data(data)

        # Handle any specific Linear API field transformations
        if "team_id" in prepared_data:
            prepared_data["teamId"] = prepared_data.pop("team_id")

        return prepared_data
