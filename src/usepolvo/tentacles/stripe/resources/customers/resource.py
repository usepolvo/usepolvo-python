from typing import Any, Dict, List

from stripe.error import StripeError

from usepolvo.arms.base_resource import BaseResource
from usepolvo.beak.exceptions import ResourceNotFoundError, ValidationError


class CustomerResource(BaseResource):
    def __init__(self, client):
        super().__init__(client)
        self.stripe = client.stripe

    def list(
        self, page: int = 1, size: int = 10, starting_after: str = None, ending_before: str = None, **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Retrieve a list of Stripe customers.

        :param page: The page number to retrieve
        :param size: A limit on the number of objects to be returned. Limit can range between 1 and 100.
        :param starting_after: A cursor for use in pagination. Defines your place in the list.
        :param ending_before: A cursor for use in pagination. Defines your place in the list.
        :param kwargs: Additional parameters for the list operation
        :return: A list of customer objects
        """
        try:
            self.client.rate_limiter.wait_if_needed(is_write_operation=False)
            params = self.client.get_pagination_params(page, size, starting_after, ending_before)
            params.update(kwargs)
            return self.stripe.Customer.list(**params)
        except StripeError as e:
            self.client.handle_error(e)

    def get(self, resource_id: str) -> Dict[str, Any]:
        """
        Retrieve a single Stripe customer by ID.

        :param resource_id: The ID of the customer to retrieve
        :return: The customer object
        :raises ResourceNotFoundError: If the customer is not found
        """
        try:
            self.client.rate_limiter.wait_if_needed(is_write_operation=False)
            return self.stripe.Customer.retrieve(resource_id)
        except self.stripe.error.InvalidRequestError:
            raise ResourceNotFoundError(f"Customer with ID {resource_id} not found")
        except StripeError as e:
            self.client.handle_error(e)

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new Stripe customer.

        :param data: The data for the new customer
        :return: The created customer object
        :raises ValidationError: If the data is invalid
        """
        try:
            self.client.rate_limiter.wait_if_needed(is_write_operation=True)
            return self.stripe.Customer.create(**data)
        except self.stripe.error.InvalidRequestError as e:
            raise ValidationError(f"Invalid data for creating customer: {str(e)}")
        except StripeError as e:
            self.client.handle_error(e)

    def update(self, resource_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing Stripe customer.

        :param resource_id: The ID of the customer to update
        :param data: The updated data for the customer
        :return: The updated customer object
        :raises ResourceNotFoundError: If the customer is not found
        :raises ValidationError: If the data is invalid
        """
        try:
            self.client.rate_limiter.wait_if_needed(is_write_operation=True)
            customer = self.stripe.Customer.modify(resource_id, **data)
            return customer
        except self.stripe.error.InvalidRequestError as e:
            if "No such customer" in str(e):
                raise ResourceNotFoundError(f"Customer with ID {resource_id} not found")
            else:
                raise ValidationError(f"Invalid data for updating customer: {str(e)}")
        except StripeError as e:
            self.client.handle_error(e)

    def delete(self, resource_id: str) -> None:
        """
        Delete a Stripe customer.

        :param resource_id: The ID of the customer to delete
        :raises ResourceNotFoundError: If the customer is not found
        """
        try:
            self.client.rate_limiter.wait_if_needed(is_write_operation=True)
            self.stripe.Customer.delete(resource_id)
        except self.stripe.error.InvalidRequestError:
            raise ResourceNotFoundError(f"Customer with ID {resource_id} not found")
        except StripeError as e:
            self.client.handle_error(e)
