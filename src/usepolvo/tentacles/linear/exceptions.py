# usepolvo/tentacles/linear/exceptions.py

import requests


class LinearError(Exception):
    """Base class for all Linear-related exceptions."""

    pass


class LinearAuthenticationError(LinearError):
    """Raised when there is an authentication error with Linear."""

    pass


class LinearAPIError(LinearError):
    """Raised when there is an API error with Linear."""

    pass


def handle_linear_error(error: requests.RequestException):
    if isinstance(error, requests.exceptions.HTTPError):
        if error.response.status_code == 401:
            return LinearAuthenticationError("Authentication failed. Please check your API key.")
        elif error.response.status_code == 403:
            return LinearAuthenticationError("Permission denied. Please check your API key permissions.")
        else:
            return LinearAPIError(f"API error: {error.response.status_code} - {error.response.text}")
    elif isinstance(error, requests.exceptions.ConnectionError):
        return LinearAPIError("Connection error. Please check your internet connection.")
    elif isinstance(error, requests.exceptions.Timeout):
        return LinearAPIError("Request timed out. Please try again later.")
    else:
        return LinearError(f"An unexpected error occurred: {str(error)}")
