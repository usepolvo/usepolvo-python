from functools import lru_cache

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


@lru_cache
def get_settings():
    return Settings()


class Settings(BaseSettings):
    cache_size: int = 100  # Default cache size
    cache_ttl: int = 600  # Default cache TTL (in seconds)
