from functools import lru_cache

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


@lru_cache
def get_settings():
    return Settings()


class Settings(BaseSettings, env_file=".env"):
    stripe_api_key: str
    encryption_key: str
