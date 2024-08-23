from google.api_core import exceptions as google_exceptions


class GeminiError(Exception):
    """Base class for all Gemini-related exceptions."""

    @staticmethod
    def handle(e: Exception):
        """Handles Gemini exceptions and raises appropriate usepolvo exceptions."""
        if isinstance(e, google_exceptions.PermissionDenied):
            raise GeminiAuthenticationError(f"Authentication error: {e}")
        elif isinstance(e, google_exceptions.InvalidArgument):
            raise GeminiAPIError(f"Invalid argument error: {e}")
        elif isinstance(e, google_exceptions.ResourceExhausted):
            raise GeminiAPIError(f"Rate limit exceeded: {e}")
        else:
            raise GeminiError(f"An unexpected error occurred: {e}")


class GeminiAuthenticationError(GeminiError):
    """Raised when there is an authentication error with Gemini."""

    pass


class GeminiAPIError(GeminiError):
    """Raised when there is an API error with Gemini."""

    pass
