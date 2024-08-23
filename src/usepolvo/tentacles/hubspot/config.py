from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings


@lru_cache
def get_settings():
    return Settings()


class Settings(BaseSettings):
    hubspot_api_key: Optional[str] = None
    hubspot_client_id: Optional[str] = None
    hubspot_client_secret: Optional[str] = None
    hubspot_redirect_uri: Optional[str] = None

    class Config:
        env_file = ".env"
        extra = "ignore"
