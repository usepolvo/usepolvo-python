from hubspot.crm.contacts import ApiException


class HubSpotError(Exception):
    """Base class for all HubSpot-related exceptions."""

    pass


class HubSpotAuthenticationError(HubSpotError):
    """Raised when there is an authentication error with HubSpot."""

    pass


class HubSpotAPIError(HubSpotError):
    """Raised when there is an API error with HubSpot."""

    pass


class HubSpotRateLimitError(HubSpotError):
    """Raised when HubSpot's rate limit is exceeded."""

    pass


def handle_hubspot_error(e: Exception):
    """Handles HubSpot exceptions and raises appropriate usepolvo exceptions."""
    if isinstance(e, ApiException):
        if e.status == 401:
            raise HubSpotAuthenticationError(f"Authentication error: {e}")
        elif e.status == 429:
            raise HubSpotRateLimitError(f"Rate limit exceeded: {e}")
        else:
            raise HubSpotAPIError(f"API error: {e}")
    else:
        raise HubSpotError(f"An unexpected error occurred: {e}")
