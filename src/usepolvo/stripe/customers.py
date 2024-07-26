import asyncio

import stripe
from cachetools import TTLCache, cached
from pydantic import ValidationError

from ..rate_limit import rate_limited_call
from ..schemas.stripe_schemas import CreateCustomer, Customer
from ..utils.transformations import transform_customer_data, transform_response_data
from .config import get_settings
from .exceptions import StripeError

# Set up cache: max size 100, TTL 10 minutes
cache = TTLCache(maxsize=100, ttl=600)


class StripeCustomerClient:
    def __init__(self):
        settings = get_settings()
        stripe.api_key = settings.api_key
        self.stripe = stripe

    @rate_limited_call
    @cached(cache)
    async def list_customers(self, page=1, size=10):
        params = {"limit": size, "starting_after": None}
        if page > 1:
            previous_page = (page - 1) * size
            params["starting_after"] = await self._get_nth_customer_id(previous_page)

        try:
            response = await asyncio.to_thread(stripe.Customer.list, **params)
            customers = response.data
        except Exception as e:
            StripeError.handle(e)

        transformed_customers = [transform_response_data(c) for c in customers]
        return [Customer(**tc) for tc in transformed_customers]

    async def _get_nth_customer_id(self, n):
        try:
            customers = await asyncio.to_thread(stripe.Customer.list, limit=n + 1)
            if len(customers.data) > n:
                return customers.data[n]["id"]
        except Exception as e:
            StripeError.handle(e)
        return None

    @rate_limited_call
    async def create_customer(self, **kwargs) -> Customer:
        try:
            customer_data = CreateCustomer(**kwargs)
        except ValidationError as e:
            raise ValueError(f"Invalid customer data: {e}")

        transformed_data = transform_customer_data(customer_data.dict())

        try:
            customer = await asyncio.to_thread(stripe.Customer.create, **transformed_data)
        except Exception as e:
            StripeError.handle(e)

        transformed_customer = transform_response_data(customer)
        return Customer(**transformed_customer)

    @rate_limited_call
    async def retrieve_customer(self, customer_id) -> Customer:
        try:
            customer = await asyncio.to_thread(stripe.Customer.retrieve, customer_id)
        except Exception as e:
            StripeError.handle(e)

        transformed_customer = transform_response_data(customer)
        return Customer(**transformed_customer)

    @rate_limited_call
    async def update_customer(self, customer_id, **kwargs) -> Customer:
        try:
            customer_data = Customer(id=customer_id, **kwargs)
        except ValidationError as e:
            raise ValueError(f"Invalid customer data: {e}")

        transformed_data = transform_customer_data(customer_data.dict())

        try:
            customer = await asyncio.to_thread(stripe.Customer.modify, customer_id, **transformed_data)
        except Exception as e:
            StripeError.handle(e)

        transformed_customer = transform_response_data(customer)
        return Customer(**transformed_customer)

    @rate_limited_call
    async def delete_customer(self, customer_id) -> Customer:
        try:
            customer = await asyncio.to_thread(stripe.Customer.delete, customer_id)
        except Exception as e:
            StripeError.handle(e)

        transformed_customer = transform_response_data(customer)
        return Customer(**transformed_customer)
