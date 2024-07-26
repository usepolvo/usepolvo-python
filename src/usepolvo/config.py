import os

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    stripe_api_key: str
    encryption_key: str

    class Config:
        env_file = ".env"


settings = Settings()
