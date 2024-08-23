import json
import os
import time
from typing import Any, Dict, Optional
from urllib.parse import parse_qs, urlparse

import requests
from hubspot import hubspot
from hubspot.hubspot import Client

from usepolvo.arms.base_client import BaseClient
from usepolvo.tentacles.hubspot.config import get_settings
from usepolvo.tentacles.hubspot.contacts.resource import HubSpotContactResource
from usepolvo.tentacles.hubspot.exceptions import HubSpotAuthenticationError, handle_hubspot_error
from usepolvo.tentacles.hubspot.notes.resource import HubSpotNoteResource
from usepolvo.tentacles.hubspot.rate_limiter import HubSpotRateLimiter
from usepolvo.tentacles.hubspot.tasks.resource import HubSpotTaskResource


class HubSpotClient(BaseClient):
    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        redirect_uri: Optional[str] = None,
    ):
        super().__init__()
        self.settings = get_settings()
        self.client_id = client_id if client_id else self.settings.hubspot_client_id
        self.client_secret = client_secret if client_secret else self.settings.hubspot_client_secret
        self.redirect_uri = redirect_uri if redirect_uri else self.settings.hubspot_redirect_uri
        self.rate_limiter = HubSpotRateLimiter()
        self.access_token = None
        self.refresh_token = None
        self.token_expiry = 0
        self.token_file = os.path.expanduser("~/.hubspot_token.json")
        self.load_tokens()
        self.client: Client = None
        self.authenticate()
        self._contacts = None
        self._tasks = None
        self._notes = None

    @property
    def contacts(self):
        if self._contacts is None:
            self._contacts = HubSpotContactResource(self)
        return self._contacts

    @property
    def tasks(self):
        if self._tasks is None:
            self._tasks = HubSpotTaskResource(self)
        return self._tasks

    @property
    def notes(self):
        if self._notes is None:
            self._notes = HubSpotNoteResource(self)
        return self._notes

    def load_tokens(self):
        if os.path.exists(self.token_file):
            with open(self.token_file, "r") as f:
                token_data = json.load(f)
                self.access_token = token_data.get("access_token")
                self.refresh_token = token_data.get("refresh_token")
                self.token_expiry = token_data.get("expiry", 0)

    def save_tokens(self):
        token_data = {
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "expiry": self.token_expiry,
        }
        os.makedirs(os.path.dirname(self.token_file), exist_ok=True)
        with open(self.token_file, "w") as f:
            json.dump(token_data, f)

    def authenticate(self):
        if not self.access_token or time.time() > self.token_expiry:
            if self.refresh_token:
                self.refresh_access_token()
            else:
                self.get_oauth_token()

        self.client = hubspot.Client(access_token=self.access_token)

    def get_oauth_token(self):
        auth_url = f"https://app.hubspot.com/oauth/authorize?client_id={self.client_id}&redirect_uri={self.redirect_uri}&scope=crm.objects.contacts.write%20oauth%20crm.objects.contacts.read"
        print(f"Please visit this URL to authenticate: {auth_url}")
        print("After authentication, you will be redirected to a URL. Please copy and paste that entire URL here:")
        redirect_url = input().strip()

        parsed_url = urlparse(redirect_url)
        query_params = parse_qs(parsed_url.query)

        if "code" in query_params:
            code = query_params["code"][0]
            token_url = "https://api.hubapi.com/oauth/v1/token"
            data = {
                "grant_type": "authorization_code",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "redirect_uri": self.redirect_uri,
                "code": code,
            }
            response = requests.post(token_url, data=data)

            if response.status_code == 200:
                token_data = response.json()
                self.access_token = token_data["access_token"]
                self.refresh_token = token_data["refresh_token"]
                self.token_expiry = time.time() + token_data["expires_in"]
                self.save_tokens()
            else:
                raise HubSpotAuthenticationError("Failed to obtain access token.")
        else:
            raise HubSpotAuthenticationError("Authorization code not found in the redirect URL.")

    def refresh_access_token(self):
        token_url = "https://api.hubapi.com/oauth/v1/token"
        data = {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": self.refresh_token,
        }
        response = requests.post(token_url, data=data)

        if response.status_code == 200:
            token_data = response.json()
            self.access_token = token_data["access_token"]
            self.refresh_token = token_data["refresh_token"]
            self.token_expiry = time.time() + token_data["expires_in"]
            self.save_tokens()
        else:
            # If refresh fails, we need to re-authenticate
            self.refresh_token = None
            self.get_oauth_token()

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        self.authenticate()

        try:
            response = self.client.api_client.call_api(endpoint, method, **kwargs)
            return response
        except Exception as e:
            if "401" in str(e):
                # Token might be expired, try to re-authenticate
                self.authenticate()
                response = self.client.api_client.call_api(endpoint, method, **kwargs)
                return response
            else:
                raise handle_hubspot_error(e)

    def rate_limited_execute(self, func, *args, **kwargs):
        self.rate_limiter.wait_if_needed()
        try:
            return func(*args, **kwargs)
        except Exception as e:
            raise handle_hubspot_error(e)

    def handle_error(self, e):
        super().handle_error(e)
        # Additional HubSpot-specific error handling can be added here

    def get_pagination_params(self, limit: int = 10, after: Optional[str] = None) -> Dict[str, Any]:
        params = {"limit": limit}
        if after:
            params["after"] = after
        return params
