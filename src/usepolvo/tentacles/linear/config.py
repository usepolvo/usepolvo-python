# usepolvo/tentacles/linear/config.py

from functools import lru_cache
from typing import List, Optional

from usepolvo.beak.config import PolvoBaseSettings


@lru_cache
def get_settings():
    return LinearSettings()


class LinearSettings(PolvoBaseSettings):
    LINEAR_API_KEY: Optional[str] = None
    LINEAR_CLIENT_ID: Optional[str] = None
    LINEAR_CLIENT_SECRET: Optional[str] = None
    LINEAR_OAUTH_URL: str = "https://linear.app/oauth/authorize"
    LINEAR_OAUTH_TOKEN_URL: str = "https://api.linear.app/oauth/token"
    LINEAR_OAUTH_SCOPES: List[str] = ["read", "write", "issues:create"]
    LINEAR_REDIRECT_URI: str = "https://app.linear.app/oauth/callback"
    LINEAR_BASE_URL: str = "https://api.linear.app/graphql"
    LINEAR_WEBHOOK_SECRET: Optional[str] = None
