# usepolvo/tentacles/certn/config.py

from functools import lru_cache

from pydantic_settings import BaseSettings


@lru_cache
def get_settings():
    return CertnSettings()


class CertnSettings(BaseSettings, env_file=".env", extra="ignore"):
    certn_api_key: str
    certn_base_url: str = "https://demo-api.certn.co"  # Default API URL
