# usepolvo/tentacles/salesforce/accounts/resource.py

from typing import Any, Dict

from usepolvo.arms.base_resource import BaseResource
from usepolvo.beak.exceptions import ResourceNotFoundError, ValidationError
from usepolvo.tentacles.salesforce.resources.accounts.schemas import (
    AccountListResponse,
    AccountResponse,
)


class AccountResource(BaseResource):
    def __init__(self, client):
        super().__init__(client)
        self.base_path = "/sobjects/Account"

    def list(self, page: int = 1, size: int = 10) -> AccountListResponse:
        try:
            response = self.client._request("GET", self.base_path)
            result = AccountListResponse(**response)
            return result
        except Exception as e:
            self.client.handle_error(e)

    def get(self, resource_id: str) -> AccountResponse:
        try:
            response = self.client._request("GET", f"{self.base_path}/{resource_id}")
            return AccountResponse(**response)
        except ResourceNotFoundError:
            raise ResourceNotFoundError(f"Account with ID {resource_id} not found")

    def create(self, data: Dict[str, Any]) -> AccountResponse:
        try:
            prepared_data = self._prepare_request_data(data)
            response = self.client._request("POST", self.base_path, json=prepared_data)
            return AccountResponse(**response)
        except ValidationError as e:
            raise ValidationError(f"Invalid data for creating account: {str(e)}")

    def update(self, resource_id: str, data: Dict[str, Any]) -> AccountResponse:
        try:
            prepared_data = self._prepare_request_data(data)
            response = self.client._request("PATCH", f"{self.base_path}/{resource_id}", json=prepared_data)
            return AccountResponse(**response)
        except ResourceNotFoundError:
            raise ResourceNotFoundError(f"Account with ID {resource_id} not found")
        except ValidationError as e:
            raise ValidationError(f"Invalid data for updating account: {str(e)}")

    def delete(self, resource_id: str) -> None:
        try:
            self.client._request("DELETE", f"{self.base_path}{resource_id}")
        except ResourceNotFoundError:
            raise ResourceNotFoundError(f"Account with ID {resource_id} not found")
