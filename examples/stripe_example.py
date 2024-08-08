from usepolvo.tentacles.stripe import StripeClient

client = StripeClient()


def list_customers():
    customers = client.customers.list(page=1, size=10)
    for customer in customers:
        print(f"Customer ID: {customer.id}, Email: {customer.email}")


if __name__ == "__main__":
    list_customers()
