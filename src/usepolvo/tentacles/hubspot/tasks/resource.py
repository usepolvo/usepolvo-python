# usepolvo/tentacles/hubspot/tasks/resource.py

from typing import Any, Dict

from hubspot.crm.tasks import ApiException

from usepolvo.arms.base_resource import BaseResource
from usepolvo.beak.exceptions import ResourceNotFoundError, ValidationError
from usepolvo.tentacles.hubspot.tasks.schemas import CreateTask


class HubSpotTaskResource(BaseResource):
    def __init__(self, client):
        super().__init__(client)
        self.hubspot = client.client

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            validated_data = CreateTask(**data).model_dump()
            return self.client.rate_limited_execute(
                self.hubspot.crm.tasks.basic_api.create,
                is_write_operation=True,
                simple_public_object_input=validated_data,
            )
        except ApiException as e:
            if e.status == 400:
                raise ValidationError(f"Invalid data for creating task: {str(e)}")
            self.client.handle_error(e)
