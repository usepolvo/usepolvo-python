# usepolvo/tentacles/salesforce/config.py

from functools import lru_cache
from typing import Optional
from urllib.parse import urlparse

from pydantic_settings import BaseSettings


class SalesforceSettings(BaseSettings):
    salesforce_consumer_key: Optional[str] = None
    salesforce_consumer_secret: Optional[str] = None
    salesforce_redirect_uri: Optional[str] = "http://localhost:8000/callback"
    salesforce_environment: str = "production"  # Can be 'production' or 'sandbox'
    salesforce_custom_domain: Optional[str] = None
    salesforce_api_version: str = "v61.0"  # TODO: make this configurable

    @property
    def salesforce_instance_url(self):
        if self.salesforce_custom_domain:
            return f"https://{self.salesforce_custom_domain}.my.salesforce.com"
        else:
            domain = "test.salesforce.com" if self.salesforce_environment == "sandbox" else "login.salesforce.com"
            return f"https://{domain}"

    @property
    def salesforce_oauth2_url(self):
        return f"{self.salesforce_instance_url}/services/oauth2"

    @property
    def salesforce_auth_url(self):
        return f"{self.salesforce_oauth2_url}/authorize"

    @property
    def salesforce_token_url(self):
        return f"{self.salesforce_oauth2_url}/token"

    @property
    def salesforce_api_base_url(self):
        return f"{self.salesforce_instance_url}/services/data/{self.salesforce_api_version}"

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache
def get_settings():
    return SalesforceSettings()
