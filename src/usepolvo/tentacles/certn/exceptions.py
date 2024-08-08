# usepolvo/tentacles/certn/exceptions.py

import requests


class CertnError(Exception):
    """Base class for all Certn-related exceptions."""

    pass


class CertnAuthenticationError(CertnError):
    """Raised when there is an authentication error with Certn."""

    pass


class CertnAPIError(CertnError):
    """Raised when there is an API error with Certn."""

    pass


def handle_certn_error(error: requests.RequestException):
    if isinstance(error, requests.exceptions.HTTPError):
        if error.response.status_code == 401:
            return CertnAuthenticationError("Authentication failed. Please check your API key.")
        elif error.response.status_code == 403:
            return CertnAuthenticationError("Permission denied. Please check your API key permissions.")
        else:
            return CertnAPIError(f"API error: {error.response.status_code} - {error.response.text}")
    elif isinstance(error, requests.exceptions.ConnectionError):
        return CertnAPIError("Connection error. Please check your internet connection.")
    elif isinstance(error, requests.exceptions.Timeout):
        return CertnAPIError("Request timed out. Please try again later.")
    else:
        return CertnError(f"An unexpected error occurred: {str(error)}")
