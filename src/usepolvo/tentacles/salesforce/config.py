# usepolvo/tentacles/salesforce/config.py

from functools import lru_cache
from typing import Optional

from usepolvo.beak.config import PolvoBaseSettings


@lru_cache
def get_settings():
    return SalesforceSettings()


class SalesforceSettings(PolvoBaseSettings):
    SALESFORCE_CONSUMER_KEY: Optional[str] = None
    SALESFORCE_CONSUMER_SECRET: Optional[str] = None
    SALESFORCE_REDIRECT_URI: str = "http://localhost:8000/callback"
    SALESFORCE_ENV: str = "production"  # Can be 'production' or 'sandbox'
    SALESFORCE_CUSTOM_DOMAIN: Optional[str] = None
    SALESFORCE_API_VERSION: str = "v61.0"  # TODO: make this configurable

    @property
    def salesforce_instance_url(self):
        if self.SALESFORCE_CUSTOM_DOMAIN:
            return f"https://{self.SALESFORCE_CUSTOM_DOMAIN}.my.salesforce.com"
        else:
            domain = "test.salesforce.com" if self.SALESFORCE_ENV == "sandbox" else "login.salesforce.com"
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
        return f"{self.salesforce_instance_url}/services/data/{self.SALESFORCE_API_VERSION}"
