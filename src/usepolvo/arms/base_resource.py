from abc import ABC, abstractmethod
from typing import Any, Dict, List, Union

import requests

from usepolvo.beak.exceptions import ResourceNotFoundError, ValidationError
from usepolvo.ink.transformations import snake_to_camel


class BaseResource(ABC):
    def __init__(self, client):
        self.client = client

    @abstractmethod
    def list(self, **kwargs) -> List[Dict[str, Any]]:
        """
        Retrieve a list of resources.

        :param kwargs: Additional parameters for the list operation
        :return: A list of resource objects
        """
        pass

    @abstractmethod
    def get(self, resource_id: str) -> Dict[str, Any]:
        """
        Retrieve a single resource by ID.

        :param resource_id: The ID of the resource to retrieve
        :return: The resource object
        :raises ResourceNotFoundError: If the resource is not found
        """
        pass

    @abstractmethod
    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new resource.

        :param data: The data for the new resource
        :return: The created resource object
        :raises ValidationError: If the data is invalid
        """
        pass

    @abstractmethod
    def update(self, resource_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing resource.

        :param resource_id: The ID of the resource to update
        :param data: The updated data for the resource
        :return: The updated resource object
        :raises ResourceNotFoundError: If the resource is not found
        :raises ValidationError: If the data is invalid
        """
        pass

    @abstractmethod
    def delete(self, resource_id: str) -> None:
        """
        Delete a resource.

        :param resource_id: The ID of the resource to delete
        :raises ResourceNotFoundError: If the resource is not found
        """
        pass

    def _prepare_request_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepare data for a request by converting snake_case keys to camelCase.

        :param data: The input data with snake_case keys
        :return: The prepared data with camelCase keys
        """
        return {snake_to_camel(k): v for k, v in data.items()}

    def _make_request(self, method: str, endpoint: str, **kwargs) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Make an HTTP request to the API.

        :param method: The HTTP method (e.g., 'GET', 'POST', 'PUT', 'DELETE')
        :param endpoint: The API endpoint
        :param kwargs: Additional arguments for the request
        :return: The response data
        :raises ResourceNotFoundError: If the resource is not found (404 status)
        :raises ValidationError: If the request data is invalid (400 status)
        """
        try:
            response = self.client.request(method, endpoint, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 404:
                raise ResourceNotFoundError(f"Resource not found at endpoint: {endpoint}") from http_err
            elif response.status_code == 400:
                raise ValidationError(f"Invalid data for request to {endpoint}: {response.text}") from http_err
            else:
                raise
