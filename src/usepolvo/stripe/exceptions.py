import stripe


class StripeError(Exception):
    """Base class for all Stripe-related exceptions."""

    @staticmethod
    def handle(e: Exception):
        """Handles Stripe exceptions and raises appropriate usepolvo exceptions."""
        if isinstance(e, stripe.error.AuthenticationError):
            raise StripeAuthenticationError(f"Authentication error: {e}")
        elif isinstance(e, stripe.error.APIConnectionError):
            raise StripeAPIError(f"API connection error: {e}")
        elif isinstance(e, stripe.error.APIError):
            raise StripeAPIError(f"API error: {e}")
        elif isinstance(e, stripe.error.CardError):
            raise StripeAPIError(f"Card error: {e}")
        elif isinstance(e, stripe.error.InvalidRequestError):
            raise StripeAPIError(f"Invalid request error: {e}")
        else:
            raise StripeError(f"An unexpected error occurred: {e}")


class StripeAuthenticationError(StripeError):
    """Raised when there is an authentication error with Stripe."""

    pass


class StripeAPIError(StripeError):
    """Raised when there is an API error with Stripe."""

    pass
