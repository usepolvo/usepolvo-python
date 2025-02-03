class PolvoError(Exception):
    """Base exception class for all usepolvo errors."""

    def __init__(self, message: str = "An error occurred"):
        self.message = message
        super().__init__(self.message)


class AuthenticationError(PolvoError):
    """Exception raised when authentication fails."""

    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message)


class APIError(PolvoError):
    """Exception raised when an API request fails."""

    def __init__(self, message: str = "API request failed", status_code: int = None, response_text: str = None):
        self.status_code = status_code
        self.response_text = response_text
        full_message = f"{message}"
        if status_code:
            full_message += f" (Status: {status_code})"
        if response_text:
            full_message += f": {response_text}"
        super().__init__(full_message)


class RateLimitError(PolvoError):
    """Exception raised when rate limits are exceeded."""

    def __init__(self, message: str = "Rate limit exceeded", retry_after: int = None):
        self.retry_after = retry_after
        full_message = message
        if retry_after:
            full_message += f". Retry after {retry_after} seconds"
        super().__init__(full_message)


class ResourceNotFoundError(PolvoError):
    """Exception raised when a requested resource is not found."""

    def __init__(self, message: str = "Resource not found", resource_type: str = None, resource_id: str = None):
        self.resource_type = resource_type
        self.resource_id = resource_id
        full_message = message
        if resource_type and resource_id:
            full_message = f"{resource_type} with ID {resource_id} not found"
        super().__init__(full_message)


class ValidationError(PolvoError):
    """Exception raised for validation errors in the request data."""

    def __init__(self, message: str = "Validation error", errors: dict = None):
        self.errors = errors
        full_message = message
        if errors:
            full_message += f": {errors}"
        super().__init__(full_message)


class ConfigurationError(PolvoError):
    """Exception raised when there are configuration issues."""

    def __init__(self, message: str = "Configuration error"):
        super().__init__(message)


class WebhookError(PolvoError):
    """Exception raised for webhook-related errors."""

    def __init__(self, message: str = "Webhook error", event_type: str = None):
        self.event_type = event_type
        full_message = message
        if event_type:
            full_message += f" for event type {event_type}"
        super().__init__(full_message)


class SDKError(PolvoError):
    """Exception raised for SDK-specific errors."""

    def __init__(self, message: str = "SDK error", provider: str = None):
        self.provider = provider
        full_message = message
        if provider:
            full_message = f"[{provider}] {message}"
        super().__init__(full_message)
