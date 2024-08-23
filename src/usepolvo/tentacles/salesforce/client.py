import json
import os
import time
from typing import Any, Dict, Optional
from urllib.parse import parse_qs, urlparse

import requests

from usepolvo.arms.base_client import BaseClient
from usepolvo.arms.base_rate_limiter import BaseRateLimiter
from usepolvo.tentacles.salesforce.accounts.resource import SalesforceAccountResource
from usepolvo.tentacles.salesforce.config import get_settings
from usepolvo.tentacles.salesforce.exceptions import SalesforceAuthenticationError, handle_salesforce_error
from usepolvo.tentacles.salesforce.rate_limiter import SalesforceRateLimiter


class SalesforceClient(BaseClient):
    def __init__(
        self,
        consumer_key: Optional[str] | None = None,
        consumer_secret: Optional[str] | None = None,
        redirect_uri: Optional[str] | None = None,
    ):
        super().__init__()
        self.settings = get_settings()
        self.consumer_key = consumer_key if consumer_key else self.settings.salesforce_consumer_key
        self.consumer_key = consumer_secret if consumer_secret else self.settings.salesforce_consumer_secret
        self.redirect_uri = redirect_uri if redirect_uri else self.settings.salesforce_redirect_uri
        self.instance_url = self.settings.salesforce_instance_url
        self.api_base_url = self.settings.salesforce_api_base_url
        self.rate_limiter = SalesforceRateLimiter()
        self._accounts = None
        self.access_token = None
        self.refresh_token = None
        self.token_expiry = 0
        self.token_file = "~/.salesforce_token.json"
        self.load_tokens()

    @property
    def accounts(self):
        if self._accounts is None:
            self._accounts = SalesforceAccountResource(self)
        return self._accounts

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
        with open(self.token_file, "w") as f:
            json.dump(token_data, f)

    def authenticate(self):
        if not self.access_token or time.time() > self.token_expiry:
            if self.refresh_token:
                self.refresh_access_token()
            else:
                self.get_oauth_token()

    def get_oauth_token(self):
        auth_url = f"{self.instance_url}/services/oauth2/authorize?response_type=token&client_id={self.consumer_key}&redirect_uri={self.redirect_uri}"
        print(f"Please visit this URL to authenticate: {auth_url}")
        print("After authentication, you will be redirected to a URL. Please copy and paste that entire URL here:")
        redirect_url = input().strip()

        parsed_url = urlparse(redirect_url)
        fragment = parse_qs(parsed_url.fragment)

        if "access_token" in fragment:
            self.access_token = fragment["access_token"][0]
            self.refresh_token = fragment.get("refresh_token", [None])[0]
            self.instance_url = fragment["instance_url"][0]

            # Use issued_at to calculate expiry if available, otherwise use a default expiration time
            issued_at = int(fragment.get("issued_at", [str(int(time.time() * 1000))])[0]) / 1000
            default_expiration = 3600  # 1 hour in seconds
            self.token_expiry = issued_at + default_expiration

            self.save_tokens()
        else:
            raise SalesforceAuthenticationError("Failed to obtain access token from the provided URL.")

    def refresh_access_token(self):
        response = requests.post(
            f"{self.instance_url}/services/oauth2/token",
            data={
                "grant_type": "refresh_token",
                "client_id": self.consumer_key,
                "client_secret": self.consumer_secret,
                "refresh_token": self.refresh_token,
            },
        )
        if response.status_code == 200:
            data = response.json()
            self.access_token = data["access_token"]
            self.instance_url = data["instance_url"]
            self.refresh_token = data.get("refresh_token", self.refresh_token)

            # Use issued_at to calculate expiry if available, otherwise use a default expiration time
            issued_at = int(data.get("issued_at", time.time() * 1000)) / 1000
            default_expiration = 3600  # 1 hour in seconds
            self.token_expiry = issued_at + default_expiration

            self.save_tokens()
        else:
            # If refresh fails, we need to re-authenticate
            self.refresh_token = None
            self.get_oauth_token()

    @BaseRateLimiter.rate_limited
    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        self.authenticate()

        url = f"{self.api_base_url}{endpoint}"
        headers = {"Authorization": f"Bearer {self.access_token}", "Content-Type": "application/json"}
        kwargs["headers"] = headers

        try:
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                # Token might be expired, try to re-authenticate
                self.authenticate()
                headers["Authorization"] = f"Bearer {self.access_token}"
                kwargs["headers"] = headers
                retry_response = requests.request(method, url, **kwargs)
                retry_response.raise_for_status()
                return retry_response.json()
            else:
                raise handle_salesforce_error(e)

    def handle_error(self, e):
        super().handle_error(e)
        # Additional Salesforce-specific error handling can be added here

    def get_pagination_params(self, page: int, size: int) -> Dict[str, Any]:
        return {
            "q": f"SELECT Id, Name, Type, Industry, Rating, Phone, Website, AnnualRevenue, NumberOfEmployees, Description FROM Account LIMIT {size} OFFSET {(page - 1) * size}"
        }
