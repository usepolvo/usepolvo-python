# usepolvo/tentacles/certn/config.py

from functools import lru_cache
from typing import Optional

from usepolvo.beak.config import PolvoBaseSettings


@lru_cache
def get_settings():
    return CertnSettings()


class CertnSettings(PolvoBaseSettings):
    CERTN_API_KEY: Optional[str] = None
    CERTN_BASE_URL: str = "https://demo-api.certn.co"  # Default API URL
