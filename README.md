
# usepolvo-python

Version: 0.1.0

Unlock the power of seamless integrations with our all-in-one integration package. Enjoy advanced features including asynchronous support, intelligent rate limiting, efficient caching, robust logging, secure storage, and so much more.

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file with the following content:

```env
# Example configuration for Stripe
STRIPE_API_KEY=your_encrypted_stripe_api_key

# Encryption key for securing sensitive information
ENCRYPTION_KEY=your_generated_encryption_key
```

## Using the Package in Your Code

### Asynchronous Functions

**Listing Customers**

```python
import asyncio
from my_python_package.stripe.customers import StripeCustomerClient

async def list_customers():
    client = StripeCustomerClient()
    customers = await client.list_customers(page=1, size=10)
    for customer in customers:
        print(f'Customer ID: {customer.id}, Email: {customer.email}')

asyncio.run(list_customers())
```

**Creating a Customer**

```python
import asyncio
from my_python_package.stripe.customers import StripeCustomerClient

async def create_customer():
    client = StripeCustomerClient()
    customer = await client.create_customer(email="new_customer@example.com")
    print(f'Created Customer ID: {customer.id}, Email: {customer.email}')

asyncio.run(create_customer())
```

### Synchronous Functions

If you prefer to use the package synchronously, you can create a synchronous wrapper around the asynchronous functions.

```python
import asyncio
from my_python_package.stripe.customers import StripeCustomerClient

def list_customers_sync():
    client = StripeCustomerClient()
    customers = asyncio.run(client.list_customers(page=1, size=10))
    for customer in customers:
        print(f'Customer ID: {customer.id}, Email: {customer.email}')

def create_customer_sync():
    client = StripeCustomerClient()
    customer = asyncio.run(client.create_customer(email="new_customer@example.com"))
    print(f'Created Customer ID: {customer.id}, Email: {customer.email}')

# Example usage
list_customers_sync()
create_customer_sync()
```

## Features

- Asynchronous functions for better performance
- Command-line interface for common tasks
- Rate limiting and retry logic
- Caching layer to reduce API calls
- Secure token and secret management
- Structured logging and monitoring
- Built-in data validation and transformation
- Unit and integration tests

## Testing

Run unit and integration tests with `pytest`:

```bash
pytest tests/
```

## License

MIT License
