from functools import lru_cache

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


@lru_cache
def get_settings():
    return Settings()


class Settings(BaseSettings, env_file=".env", extra="ignore"):
    stripe_api_key: str
    stripe_calls: int = 100  # Default value
    stripe_period: int = 1  # Default value (in seconds)
