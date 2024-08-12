# usepolvo/tentacles/salesforce/exceptions.py

import requests


class SalesforceError(Exception):
    """Base class for all Salesforce-related exceptions."""

    pass


class SalesforceAuthenticationError(SalesforceError):
    """Raised when there is an authentication error with Salesforce."""

    pass


class SalesforceAPIError(SalesforceError):
    """Raised when there is an API error with Salesforce."""

    pass


def handle_salesforce_error(error: requests.RequestException):
    if isinstance(error, requests.exceptions.HTTPError):
        if error.response.status_code == 401:
            return SalesforceAuthenticationError("Authentication failed. Please check your API key.")
        elif error.response.status_code == 403:
            return SalesforceAuthenticationError("Permission denied. Please check your API key permissions.")
        else:
            return SalesforceAPIError(f"API error: {error.response.status_code} - {error.response.text}")
    elif isinstance(error, requests.exceptions.ConnectionError):
        return SalesforceAPIError("Connection error. Please check your internet connection.")
    elif isinstance(error, requests.exceptions.Timeout):
        return SalesforceAPIError("Request timed out. Please try again later.")
    else:
        return SalesforceError(f"An unexpected error occurred: {str(error)}")
