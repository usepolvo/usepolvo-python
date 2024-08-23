class ClaudeError(Exception):
    """Base class for all Claude-related exceptions."""

    @staticmethod
    def handle(e: Exception):
        """Handles Claude exceptions and raises appropriate usepolvo exceptions."""
        if isinstance(e, ValueError):
            raise ClaudeAPIError(f"Invalid request error: {e}")
        elif isinstance(e, TypeError):
            raise ClaudeAPIError(f"Type error: {e}")
        else:
            raise ClaudeError(f"An unexpected error occurred: {e}")


class ClaudeAuthenticationError(ClaudeError):
    """Raised when there is an authentication error with Claude."""

    pass


class ClaudeAPIError(ClaudeError):
    """Raised when there is an API error with Claude."""

    pass
