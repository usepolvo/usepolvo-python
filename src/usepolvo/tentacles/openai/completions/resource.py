from typing import Any, Dict

from openai import OpenAI

from usepolvo.arms.base_resource import BaseResource


class CompletionResource(BaseResource):
    def __init__(self, client):
        super().__init__(client)
        self.openai: OpenAI = client.client

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new completion using OpenAI.

        :param data: The data for the new completion
        :return: The created completion object
        :raises ValidationError: If the data is invalid
        """
        try:
            self.client.rate_limiter.wait_if_needed()
            response = self.openai.chat.completions.create(**data)
            return response
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
