class ResourceNotFoundError(Exception):
    """Exception raised when a requested resource is not found."""

    def __init__(self, message="Resource not found"):
        self.message = message
        super().__init__(self.message)


class ValidationError(Exception):
    """Exception raised for validation errors in the request data."""

    def __init__(self, message="Validation error"):
        self.message = message
        super().__init__(self.message)
