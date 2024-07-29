from pydantic import ValidationError

from ..schemas.stripe_schemas import CreateCustomer, Customer
from ..utils.transformations import transform_customer_data, transform_response_data
from . import StripeClient


class StripeCustomerClient:
    def __init__(self, client: StripeClient):
        self.client = client

    async def list_customers(self, page=1, size=10):
        cache_key = f"list_customers_{page}_{size}"
        if cache_key in self.client.cache:
            return self.client.cache[cache_key]

        params = {"limit": size, "starting_after": None}
        if page > 1:
            previous_page = (page - 1) * size
            params["starting_after"] = await self._get_nth_customer_id(previous_page)

        try:
            response = await self.client.rate_limited_execute(self.client.stripe.Customer.list, **params)
            customers = response.data
        except Exception as e:
            self.client.handle_error(e)

        transformed_customers = [transform_response_data(c) for c in customers]
        result = [Customer(**tc) for tc in transformed_customers]
        self.client.cache[cache_key] = result
        return result

    async def _get_nth_customer_id(self, n):
        cache_key = f"nth_customer_id_{n}"
        if cache_key in self.client.cache:
            return self.client.cache[cache_key]

        try:
            customers = await self.client.rate_limited_execute(self.client.stripe.Customer.list, limit=n + 1)
            if len(customers.data) > n:
                result = customers.data[n]["id"]
                self.client.cache[cache_key] = result
                return result
        except Exception as e:
            self.client.handle_error(e)
        return None

    async def create_customer(self, **kwargs) -> Customer:
        try:
            customer_data = CreateCustomer(**kwargs)
        except ValidationError as e:
            raise ValueError(f"Invalid customer data: {e}")

        transformed_data = transform_customer_data(customer_data.model_dump())

        try:
            customer = await self.client.rate_limited_execute(
                self.client.stripe.Customer.create,
                **transformed_data,
            )
        except Exception as e:
            self.client.handle_error(e)

        transformed_customer = transform_response_data(customer)
        return Customer(**transformed_customer)

    async def retrieve_customer(self, customer_id) -> Customer:
        cache_key = f"retrieve_customer_{customer_id}"
        if cache_key in self.client.cache:
            return self.client.cache[cache_key]

        try:
            customer = await self.client.rate_limited_execute(self.client.stripe.Customer.retrieve, customer_id)
        except Exception as e:
            self.client.handle_error(e)

        transformed_customer = transform_response_data(customer)
        result = Customer(**transformed_customer)
        self.client.cache[cache_key] = result
        return result

    async def update_customer(self, customer_id, **kwargs) -> Customer:
        try:
            customer_data = Customer(id=customer_id, **kwargs)
        except ValidationError as e:
            raise ValueError(f"Invalid customer data: {e}")

        transformed_data = transform_customer_data(customer_data.model_dump())

        try:
            customer = await self.client.rate_limited_execute(
                self.client.stripe.Customer.modify,
                customer_id,
                **transformed_data,
            )
        except Exception as e:
            self.client.handle_error(e)

        transformed_customer = transform_response_data(customer)
        return Customer(**transformed_customer)

    async def delete_customer(self, customer_id) -> Customer:
        try:
            customer = await self.client.rate_limited_execute(self.client.stripe.Customer.delete, customer_id)
        except Exception as e:
            self.client.handle_error(e)

        transformed_customer = transform_response_data(customer)
        return Customer(**transformed_customer)
