# usepolvo/tentacles/hubspot/tasks/resource.py

from typing import Any, Dict

from hubspot.crm.objects import ApiException, SimplePublicObjectInputForCreate

from usepolvo.arms.base_resource import BaseResource
from usepolvo.beak.exceptions import ValidationError
from usepolvo.tentacles.hubspot.resources.tasks.schemas import CreateTask


class TaskResource(BaseResource):
    def __init__(self, client):
        super().__init__(client)
        self.hubspot = client.client

    def create(self, data: CreateTask) -> Dict[str, Any]:
        try:
            create_task = CreateTask(**data).model_dump()
            validated_data = SimplePublicObjectInputForCreate(**create_task)
            res = self.client.rate_limited_execute(
                lambda: self.hubspot.crm.objects.basic_api.create(
                    object_type="tasks", simple_public_object_input_for_create=validated_data
                )
            )
            return res
        except ApiException as e:
            if e.status == 400:
                raise ValidationError(f"Invalid data for creating task: {str(e)}")
            self.client.handle_error(e)

    def get(self):
        pass

    def list(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass
