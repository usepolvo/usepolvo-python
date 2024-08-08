from unittest.mock import patch

import pytest

from src.usepolvo.tentacles.certn.applications.resource import CertnApplicationResource
from src.usepolvo.tentacles.certn.client import CertnClient
from src.usepolvo.tentacles.stripe.client import StripeClient
from src.usepolvo.tentacles.stripe.customers.resource import StripeCustomerResource


@pytest.fixture
def certn_client():
    with patch("usepolvo.tentacles.certn.client.CertnClient.__init__", return_value=None):
        client = CertnClient()
        client.api_key = "test_api_key"
        client.pagination_method = "cursor"
        client.cache = {}
        return client


@pytest.fixture
def certn_application_resource(certn_client):
    return CertnApplicationResource(client=certn_client)


@pytest.fixture
def stripe_client():
    with patch("usepolvo.tentacles.stripe.client.StripeClient.__init__", return_value=None):
        client = StripeClient()
        client.api_key = "sk_test_4eC39HqLyjWDarjtT1zdp7dc"
        client.stripe = patch("stripe")
        client.pagination_method = "cursor"
        client.cache = {}
        return client


@pytest.fixture
def stripe_customer_resource(stripe_client):
    return StripeCustomerResource(client=stripe_client)
