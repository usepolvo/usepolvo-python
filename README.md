# usepolvo-python

Version: 0.1.24

Unlock the power of seamless integrations with our all-in-one integration package. Enjoy advanced features including asynchronous support, intelligent rate limiting, efficient caching, robust logging, secure storage, and so much more.

## Project Structure

Our project follows an octopus-themed structure to keep things organized and fun:

```
usepolvo-python/
├── src/
│   └── usepolvo/
│       ├── tentacles/                  # Integrations
│       │   ├── certn/
│       │   │   ├── applications/       # API resources
│       │   │   │   └── resource.py
│       │   │   │   └── ...
│       │   │   ├── webhooks/           # Webhook handler
│       │   │   │   └── handler.py
│       │   │   │   └── ...
│       │   │   ├── client.py           # API client
│       │   │   └── ...
│       │   ├── stripe/
│       │   │   └── ...
│       │   └── ...
│       ├── arms/                       # Shared functionality
│       ├── ink/                        # Utilities
│       ├── beak/                       # Core functionality
│       └── mantle/                     # Advanced features
├── tests/
├── examples/
└── [configuration files]
```

### Key Directories

- **tentacles/**: Each subdirectory represents an API integration (e.g., `stripe/`).
- **arms/**: Shared functionality used across different API integrations.
- **ink/**: Utility functions and helpers.
- **beak/**: Core functionality of the library.
- **mantle/**: Advanced features like logging and complex configurations.
- **tests/**: All test files, mirroring the structure of the `src/` directory.
- **examples/**: Example scripts demonstrating how to use the library.

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
from usepolvo.tentacles.stripe.customers import StripeCustomerClient

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
from usepolvo.tentacles.stripe.customers import StripeCustomerClient

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
from usepolvo.tentacles.stripe.customers import StripeCustomerClient

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
