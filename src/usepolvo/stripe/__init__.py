import asyncio
from functools import wraps

import stripe

from .. import BaseClient
from ..rate_limit import rate_limited_call
from .config import get_settings


class StripeClient(BaseClient):
    def __init__(self):
        super().__init__()
        settings = get_settings()
        stripe.api_key = settings.stripe_api_key
        self.stripe = stripe
        self.calls = settings.stripe_calls
        self.period = settings.stripe_period

    def rate_limited_execute(self, method, *args, **kwargs):
        @rate_limited_call(calls=self.calls, period=self.period)
        @wraps(method)
        def wrapper():
            return asyncio.to_thread(method, *args, **kwargs)

        return wrapper()

    def handle_error(self, e):
        super().handle_error(e)
        # Additional Stripe-specific error handling can be added here
