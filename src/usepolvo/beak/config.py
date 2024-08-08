# usepolvo/config.py

from enum import Enum
from functools import lru_cache

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

from usepolvo.beak.enums import PaginationMethod

load_dotenv()


class Settings(BaseSettings):
    cache_size: int = 100  # Default cache size
    cache_ttl: int = 600  # Default cache TTL (in seconds)
    pagination_method: PaginationMethod = PaginationMethod.OFFSET_LIMIT  # Default pagination method

    class Config:
        env_prefix = "USEPOLVO_"


@lru_cache
def get_settings():
    return Settings()
