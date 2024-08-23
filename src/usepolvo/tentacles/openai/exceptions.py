import openai


class OpenAIError(Exception):
    """Base class for all OpenAI-related exceptions."""

    @staticmethod
    def handle(e: Exception):
        """Handles OpenAI exceptions and raises appropriate usepolvo exceptions."""
        if isinstance(e, openai.error.AuthenticationError):
            raise OpenAIAuthenticationError(f"Authentication error: {e}")
        elif isinstance(e, openai.error.APIError):
            raise OpenAIAPIError(f"API error: {e}")
        elif isinstance(e, openai.error.InvalidRequestError):
            raise OpenAIAPIError(f"Invalid request error: {e}")
        elif isinstance(e, openai.error.RateLimitError):
            raise OpenAIAPIError(f"Rate limit exceeded: {e}")
        else:
            raise OpenAIError(f"An unexpected error occurred: {e}")


class OpenAIAuthenticationError(OpenAIError):
    """Raised when there is an authentication error with OpenAI."""

    pass


class OpenAIAPIError(OpenAIError):
    """Raised when there is an API error with OpenAI."""

    pass
