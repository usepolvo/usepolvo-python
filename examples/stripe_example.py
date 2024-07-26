import asyncio

from usepolvo.stripe.customers import StripeCustomerClient


async def list_customers():
    client = StripeCustomerClient()
    customers = await client.list_customers(page=1, size=10)
    for customer in customers:
        print(f"Customer ID: {customer.id}, Email: {customer.email}")


async def create_customer():
    client = StripeCustomerClient()
    customer = await client.create_customer(email="new_customer@example.com")
    print(f"Created Customer ID: {customer.id}, Email: {customer.email}")


if __name__ == "__main__":
    asyncio.run(list_customers())
    asyncio.run(create_customer())
