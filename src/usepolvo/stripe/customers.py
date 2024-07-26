import stripe
from cachetools import TTLCache, cached
from pydantic import ValidationError

from ..config import settings
from ..rate_limit import rate_limited_call
from ..schemas.stripe_schemas import Customer
from ..utils.encryption import EncryptionManager
from ..utils.transformations import transform_customer_data, transform_response_data

# Set up cache: max size 100, TTL 10 minutes
cache = TTLCache(maxsize=100, ttl=600)


class StripeCustomerClient:
    def __init__(self):
        encryption_key = settings.encryption_key.encode()
        self.encryption_manager = EncryptionManager(encryption_key)
        self.api_key = self.encryption_manager.decrypt(settings.stripe_api_key)
        stripe.api_key = self.api_key
        self.stripe = stripe

    @rate_limited_call
    @cached(cache)
    async def list_customers(self, page=1, size=10):
        params = {"limit": size, "starting_after": None}
        if page > 1:
            previous_page = (page - 1) * size
            params["starting_after"] = await self._get_nth_customer_id(previous_page)
        customers = await stripe.Customer.list(**params).data
        transformed_customers = [transform_response_data(c) for c in customers]
        return [Customer(**tc) for tc in transformed_customers]

    async def _get_nth_customer_id(self, n):
        customers = await stripe.Customer.list(limit=n + 1).data
        if len(customers) > n:
            return customers[n]["id"]
        return None

    @rate_limited_call
    async def create_customer(self, **kwargs) -> Customer:
        try:
            customer_data = Customer(**kwargs)
        except ValidationError as e:
            raise ValueError(f"Invalid customer data: {e}")
        transformed_data = transform_customer_data(customer_data.dict())
        customer = await stripe.Customer.create(**transformed_data)
        transformed_customer = transform_response_data(customer)
        return Customer(**transformed_customer)

    @rate_limited_call
    async def retrieve_customer(self, customer_id) -> Customer:
        customer = await stripe.Customer.retrieve(customer_id)
        transformed_customer = transform_response_data(customer)
        return Customer(**transformed_customer)

    @rate_limited_call
    async def update_customer(self, customer_id, **kwargs) -> Customer:
        try:
            customer_data = Customer(id=customer_id, **kwargs)
        except ValidationError as e:
            raise ValueError(f"Invalid customer data: {e}")
        transformed_data = transform_customer_data(customer_data.dict())
        customer = await stripe.Customer.modify(customer_id, **transformed_data)
        transformed_customer = transform_response_data(customer)
        return Customer(**transformed_customer)

    @rate_limited_call
    async def delete_customer(self, customer_id) -> Customer:
        customer = await stripe.Customer.delete(customer_id)
        transformed_customer = transform_response_data(customer)
        return Customer(**transformed_customer)
