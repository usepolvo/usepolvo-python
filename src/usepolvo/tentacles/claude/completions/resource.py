from typing import Any, Dict

from usepolvo.arms.base_resource import BaseResource
from usepolvo.beak.exceptions import ValidationError


class CompletionResource(BaseResource):
    def __init__(self, client):
        super().__init__(client)
        self.anthropic = client.client

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new completion using Claude.

        :param data: The data for the new completion
        :return: The created completion object
        :raises ValidationError: If the data is invalid
        """
        try:
            self.client.rate_limiter.wait_if_needed()
            response = self.anthropic.completions.create(**data)
            return response.model_dump()
        except ValueError as e:
            raise ValidationError(f"Invalid data for creating completion: {str(e)}")
        except Exception as e:
            self.client.handle_error(e)

    def get(self, completion_id: str) -> Dict[str, Any]:
        pass

    def list(self, **kwargs) -> Dict[str, Any]:
        pass

    def update(self, completion_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        pass

    def delete(self, completion_id: str) -> Dict[str, Any]:
        pass
