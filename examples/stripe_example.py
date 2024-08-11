from usepolvo.tentacles.stripe import StripeClient, StripeWebhook
import asyncio

client = StripeClient()
webhook = StripeWebhook()


async def list_customers():
    customers = await client.customers.list(page=1, size=10)
    for customer in customers:
        print(f"Customer ID: {customer.id}, Email: {customer.email}")


@webhook.register("customer.created")
async def handle_customer_created(payload):
    customer = payload["data"]["object"]
    print(f"New customer created: ID: {customer['id']}, Email: {customer['email']}")


@webhook.register("customer.updated")
async def handle_customer_updated(payload):
    customer = payload["data"]["object"]
    print(f"Customer updated: ID: {customer['id']}, Email: {customer['email']}")


async def main():
    # Start the webhook server
    await webhook.start_server("/webhook/stripe", port=8081)

    # List customers
    await list_customers()

    # Keep the server running
    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
