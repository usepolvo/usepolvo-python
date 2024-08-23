from typing import Any, Dict

import openai

from usepolvo.arms.base_resource import BaseResource
from usepolvo.beak.exceptions import ResourceNotFoundError, ValidationError
from usepolvo.tentacles.openai.exceptions import OpenAIError


class OpenAICompletionResource(BaseResource):
    def __init__(self, client):
        super().__init__(client)
        self.openai = client.client

    async def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new completion using OpenAI.

        :param data: The data for the new completion
        :return: The created completion object
        :raises ValidationError: If the data is invalid
        """
        try:
            await self.client.rate_limiter.wait_if_needed()
            response = await self.openai.Completion.acreate(**data)
            return response
        except openai.error.InvalidRequestError as e:
            raise ValidationError(f"Invalid data for creating completion: {str(e)}")
        except Exception as e:
            self.client.handle_error(e)

    # Additional methods like list(), get(), update(), delete() can be added if applicable
