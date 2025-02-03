from typing import Any, Dict

from usepolvo.arms.base_resource import BaseResource
from usepolvo.beak.exceptions import ResourceNotFoundError, ValidationError
from usepolvo.tentacles.certn.resources.applications.schemas import (
    ApplicationListResponse,
    ApplicationResponse,
)


class ApplicationResource(BaseResource):
    def __init__(self, client):
        super().__init__(client)
        self.base_path = "/hr/v1/applicants/"

    def list(self, page: int = 1, size: int = 10) -> ApplicationListResponse:
        try:
            params = self.client.get_pagination_params(page, size)
            response = self.client._request("GET", self.base_path, params=params)
            result = ApplicationListResponse(**response)
            return result
        except Exception as e:
            self.client.handle_error(e)

    def get(self, resource_id: str) -> ApplicationResponse:
        try:
            response = self.client._request("GET", f"{self.base_path}{resource_id}/")
            return ApplicationResponse(**response)
        except ResourceNotFoundError:
            raise ResourceNotFoundError(f"Application with ID {resource_id} not found")

    def create(self, data: Dict[str, Any]) -> ApplicationResponse:
        try:
            prepared_data = self._prepare_request_data(data)
            response = self.client._request("POST", self.base_path, json=prepared_data)
            return ApplicationResponse(**response)
        except ValidationError as e:
            raise ValidationError(f"Invalid data for creating application: {str(e)}")

    def update(self, resource_id: str, data: Dict[str, Any]) -> ApplicationResponse:
        try:
            prepared_data = self._prepare_request_data(data)
            response = self.client._request("PUT", f"{self.base_path}{resource_id}/", json=prepared_data)
            return ApplicationResponse(**response)
        except ResourceNotFoundError:
            raise ResourceNotFoundError(f"Application with ID {resource_id} not found")
        except ValidationError as e:
            raise ValidationError(f"Invalid data for updating application: {str(e)}")

    def delete(self, resource_id: str) -> None:
        try:
            self.client._request("DELETE", f"{self.base_path}{resource_id}/")
        except ResourceNotFoundError:
            raise ResourceNotFoundError(f"Application with ID {resource_id} not found")
