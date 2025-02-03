# usepolvo/beak/config.py

from functools import lru_cache
from typing import Optional

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

from usepolvo.beak.enums import PaginationMethod

load_dotenv()


@lru_cache
def get_settings():
    return PolvoSettings()


class PolvoBaseSettings(BaseSettings):
    """
    Base settings class that reads environment variables with POLVO_ prefix.
    Inherits from BaseSettings to provide environment variable loading functionality.
    """

    model_config = SettingsConfigDict(
        env_prefix="POLVO_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )


class PolvoSettings(PolvoBaseSettings):
    CACHE_SIZE: int = 100  # Default cache size
    CACHE_TTL: int = 600  # Default cache TTL (in seconds)
    PAGINATION_METHOD: PaginationMethod = PaginationMethod.OFFSET_LIMIT  # Default pagination method
    ENCRYPTION_KEY: Optional[str] = None  # Encryption key for sensitive data
