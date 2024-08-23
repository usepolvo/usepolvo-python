from typing import Any, Dict, List

from hubspot.crm.contacts import ApiException

from usepolvo.arms.base_resource import BaseResource
from usepolvo.beak.exceptions import ResourceNotFoundError, ValidationError
from usepolvo.tentacles.hubspot.contacts.schemas import Contact, CreateContact


class HubSpotContactResource(BaseResource):
    def __init__(self, client):
        super().__init__(client)
        self.hubspot = client.client

    def list(
        self, page: int = 1, size: int = 10, after: str = None, before: str = None, **kwargs
    ) -> List[Dict[str, Any]]:
        try:
            params = self.client.get_pagination_params(page, size, after, before)
            params.update(kwargs)
            return self.client.rate_limited_execute(
                self.hubspot.crm.contacts.basic_api.get_page, is_write_operation=False, **params
            )
        except ApiException as e:
            self.client.handle_error(e)

    def get(self, resource_id: str) -> Dict[str, Any]:
        try:
            return self.client.rate_limited_execute(
                self.hubspot.crm.contacts.basic_api.get_by_id, is_write_operation=False, contact_id=resource_id
            )
        except ApiException as e:
            if e.status == 404:
                raise ResourceNotFoundError(f"Contact with ID {resource_id} not found")
            self.client.handle_error(e)

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            validated_data = CreateContact(**data).model_dump()
            return self.client.rate_limited_execute(
                self.hubspot.crm.contacts.basic_api.create, is_write_operation=True, properties=validated_data
            )
        except ApiException as e:
            if e.status == 400:
                raise ValidationError(f"Invalid data for creating contact: {str(e)}")
            self.client.handle_error(e)

    def update(self, resource_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            validated_data = Contact(**data).model_dump()
            return self.client.rate_limited_execute(
                self.hubspot.crm.contacts.basic_api.update,
                is_write_operation=True,
                contact_id=resource_id,
                properties=validated_data,
            )
        except ApiException as e:
            if e.status == 404:
                raise ResourceNotFoundError(f"Contact with ID {resource_id} not found")
            elif e.status == 400:
                raise ValidationError(f"Invalid data for updating contact: {str(e)}")
            self.client.handle_error(e)

    def delete(self, resource_id: str) -> None:
        try:
            self.client.rate_limited_execute(
                self.hubspot.crm.contacts.basic_api.archive, is_write_operation=True, contact_id=resource_id
            )
        except ApiException as e:
            if e.status == 404:
                raise ResourceNotFoundError(f"Contact with ID {resource_id} not found")
            self.client.handle_error(e)
