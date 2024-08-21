from functools import wraps
from typing import Optional

import stripe

from usepolvo.arms.base_client import BaseClient
from usepolvo.tentacles.stripe.config import get_settings
from usepolvo.tentacles.stripe.customers.resource import StripeCustomerResource
from usepolvo.tentacles.stripe.rate_limiter import StripeRateLimiter


class StripeClient(BaseClient):
    def __init__(self, api_key: Optional[str] = None):
        super().__init__()
        settings = get_settings()
        stripe.api_key = api_key if api_key else settings.stripe_api_key
        self.stripe = stripe
        self.rate_limiter = StripeRateLimiter()
        self._customers = None

    @property
    def customers(self):
        if self._customers is None:
            self._customers = StripeCustomerResource(self)
        return self._customers

    def rate_limited_execute(self, method, *args, **kwargs):
        @wraps(method)
        def wrapper(*args, **kwargs):
            is_write_operation = kwargs.get("is_write_operation", False)
            self.rate_limiter.wait_if_needed(is_write_operation=is_write_operation)
            return method(*args, **kwargs)

        return wrapper(*args, **kwargs)

    def handle_error(self, e):
        super().handle_error(e)
        # Additional Stripe-specific error handling can be added here
