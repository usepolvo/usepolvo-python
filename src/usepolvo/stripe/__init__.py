import asyncio
from functools import wraps

import stripe

from .. import BaseClient
from ..rate_limit import rate_limited_call
from .config import get_settings


class StripeClient(BaseClient):
    def __init__(self, api_key: str | None = None):
        super().__init__()
        settings = get_settings()
        stripe.api_key = api_key if api_key else settings.stripe_api_key
        self.stripe = stripe
        self.calls = settings.stripe_calls
        self.period = settings.stripe_period
        self._customers = None

    @property
    def customers(self):
        if self._customers is None:
            from .customers import StripeCustomerClient

            self._customers = StripeCustomerClient(self)
        return self._customers

    def rate_limited_execute(self, method, *args, **kwargs):
        @rate_limited_call(calls=self.calls, period=self.period)
        @wraps(method)
        def wrapper():
            return asyncio.to_thread(method, *args, **kwargs)

        return wrapper()

    def handle_error(self, e):
        super().handle_error(e)
        # Additional Stripe-specific error handling can be added here
