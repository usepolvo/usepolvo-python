from typing import Any, Dict, List

from hubspot.crm.contacts import ApiException, SimplePublicObjectInput, SimplePublicObjectInputForCreate

from usepolvo.arms.base_resource import BaseResource
from usepolvo.beak.exceptions import ResourceNotFoundError, ValidationError
from usepolvo.tentacles.hubspot.contacts.schemas import CreateContact


class HubSpotContactResource(BaseResource):
    def __init__(self, client):
        super().__init__(client)

    def list(self, limit: int = 10, after: str = None, **kwargs) -> List[Dict[str, Any]]:
        try:
            params = self.client.get_pagination_params(limit=limit, after=after)
            params.update(kwargs)
            return self.client.rate_limited_execute(
                self.client.client.crm.contacts.basic_api.get_page, **params
            ).results
        except ApiException as e:
            self.client.handle_error(e)

    def get(self, resource_id: str) -> Dict[str, Any]:
        try:
            return self.client.rate_limited_execute(
                self.client.client.crm.contacts.basic_api.get_by_id,
                contact_id=resource_id,
                properties=["firstname", "lastname", "email"],
            )
        except ApiException as e:
            if e.status == 404:
                raise ResourceNotFoundError(f"Contact with ID {resource_id} not found")
            self.client.handle_error(e)

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            validated_data = CreateContact(**data).model_dump()
            simple_public_object_input = SimplePublicObjectInputForCreate(properties=validated_data)
            return self.client.rate_limited_execute(
                self.client.client.crm.contacts.basic_api.create,
                simple_public_object_input_for_create=simple_public_object_input,
            )
        except ApiException as e:
            if e.status == 400:
                raise ValidationError(f"Invalid data for creating contact: {str(e)}")
            self.client.handle_error(e)

    def update(self, resource_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            simple_public_object_input = SimplePublicObjectInput(properties=data)
            return self.client.rate_limited_execute(
                self.client.client.crm.contacts.basic_api.update,
                contact_id=resource_id,
                simple_public_object_input=simple_public_object_input,
            )
        except ApiException as e:
            if e.status == 404:
                raise ResourceNotFoundError(f"Contact with ID {resource_id} not found")
            elif e.status == 400:
                raise ValidationError(f"Invalid data for updating contact: {str(e)}")
            self.client.handle_error(e)

    def delete(self, resource_id: str) -> None:
        try:
            self.client.rate_limited_execute(self.client.client.crm.contacts.basic_api.archive, contact_id=resource_id)
        except ApiException as e:
            if e.status == 404:
                raise ResourceNotFoundError(f"Contact with ID {resource_id} not found")
            self.client.handle_error(e)
