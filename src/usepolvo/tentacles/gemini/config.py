from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings


@lru_cache
def get_settings():
    return Settings()


class Settings(BaseSettings, env_file=".env", extra="ignore"):
    gemini_api_key: Optional[str] = None
