import pytest

from src.usepolvo.schemas.stripe_schemas import Customer
from src.usepolvo.stripe.customers import StripeCustomerClient


@pytest.mark.asyncio
async def test_create_customer():
    client = StripeCustomerClient()
    customer = await client.create_customer(email="test@example.com")
    assert isinstance(customer, Customer)
    assert customer.email == "test@example.com"


@pytest.mark.asyncio
async def test_list_customers():
    client = StripeCustomerClient()
    customers = await client.list_customers(page=1, size=10)
    assert isinstance(customers, list)
