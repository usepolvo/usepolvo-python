from typing import Any, Dict

from google.api_core import exceptions as google_exceptions

from usepolvo.arms.base_resource import BaseResource
from usepolvo.beak.exceptions import ValidationError


class CompletionResource(BaseResource):
    def __init__(self, client):
        super().__init__(client)
        self.genai = client.client

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new completion using Gemini.

        :param data: The data for the new completion
        :return: The created completion object
        :raises ValidationError: If the data is invalid
        """
        try:
            self.client.rate_limiter.wait_if_needed()
            model = self.genai.GenerativeModel(data.pop("model"))
            response = model.generate_content(data.pop("prompt"), **data)
            return response.text
        except google_exceptions.InvalidArgument as e:
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
