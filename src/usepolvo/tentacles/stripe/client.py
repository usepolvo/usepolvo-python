from functools import wraps
from typing import Any, Dict, Optional

import stripe

from usepolvo.arms.base_client import BaseClient
from usepolvo.tentacles.stripe.config import get_settings
from usepolvo.tentacles.stripe.rate_limiter import StripeRateLimiter
from usepolvo.tentacles.stripe.resources.customers.resource import CustomerResource


class StripeClient(BaseClient):
    def __init__(self, api_key: Optional[str] = None):
        super().__init__()
        settings = get_settings()
        stripe.api_key = api_key or settings.STRIPE_API_KEY
        self.stripe = stripe
        self.rate_limiter = StripeRateLimiter()
        self._customers = None

    @property
    def customers(self):
        if self._customers is None:
            self._customers = CustomerResource(self)
        return self._customers

    def rate_limited_execute(self, method, *args, **kwargs):
        @wraps(method)
        def wrapper(*args, **kwargs):
            is_write_operation = kwargs.get("is_write_operation", False)
            self.rate_limiter.wait_if_needed(is_write_operation=is_write_operation)
            return method(*args, **kwargs)

        return wrapper(*args, **kwargs)

    def get_pagination_params(
        self, page: int = 1, size: int = 10, starting_after: Optional[str] = None, ending_before: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Override base pagination method with Stripe-specific pagination.

        :param page: The page number to retrieve (used for conceptual pagination)
        :param size: Number of items per page (limit). Can range between 1 and 100.
        :param starting_after: A cursor for use in pagination. Retrieve the next page after this ID.
        :param ending_before: A cursor for use in pagination. Retrieve the previous page before this ID.
        :return: A dictionary of pagination parameters for Stripe API
        """
        # Validate page and size parameters
        if page < 1:
            raise ValueError("Page number must be 1 or greater")
        if size < 1 or size > 100:
            raise ValueError("Size must be between 1 and 100")

        # Prepare pagination parameters
        params = {"limit": size}

        # Add starting_after or ending_before if provided
        # These are mutually exclusive in Stripe API
        if starting_after:
            params["starting_after"] = starting_after
        elif ending_before:
            params["ending_before"] = ending_before

        return params

    def handle_error(self, e):
        super().handle_error(e)
        # Additional Stripe-specific error handling can be added here
