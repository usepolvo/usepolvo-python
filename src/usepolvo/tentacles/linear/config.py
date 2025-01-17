# usepolvo/tentacles/linear/config.py

from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings


@lru_cache
def get_settings():
    return LinearSettings()


class LinearSettings(BaseSettings, env_file=".env", extra="ignore"):
    linear_api_key: Optional[str] = None
    linear_client_id: Optional[str] = None
    linear_client_secret: Optional[str] = None
    linear_base_url: str = "https://api.linear.app/graphql"
