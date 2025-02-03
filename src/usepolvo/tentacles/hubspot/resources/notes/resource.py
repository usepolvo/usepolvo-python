# usepolvo/tentacles/hubspot/notes/resource.py

from typing import Any, Dict

from hubspot.crm.objects import ApiException, SimplePublicObjectInputForCreate

from usepolvo.arms.base_resource import BaseResource
from usepolvo.beak.exceptions import ResourceNotFoundError, ValidationError
from usepolvo.tentacles.hubspot.resources.notes.schemas import CreateNote


class NoteResource(BaseResource):
    def __init__(self, client):
        super().__init__(client)
        self.hubspot = client.client

    def create(self, data: CreateNote) -> Dict[str, Any]:
        try:
            create_note = CreateNote(**data).model_dump()
            validated_data = SimplePublicObjectInputForCreate(**create_note)
            res = self.client.rate_limited_execute(
                lambda: self.hubspot.crm.objects.basic_api.create(
                    object_type="notes", simple_public_object_input_for_create=validated_data
                )
            )
            return res
        except ApiException as e:
            if e.status == 400:
                raise ValidationError(f"Invalid data for creating note: {str(e)}")
            self.client.handle_error(e)

    def get(self):
        pass

    def list(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass
