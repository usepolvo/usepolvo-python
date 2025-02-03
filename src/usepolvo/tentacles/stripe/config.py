# usepolvo/tentacles/stripe/config.py

from functools import lru_cache
from typing import Optional

from usepolvo.beak.config import PolvoBaseSettings


@lru_cache
def get_settings():
    return StripeSettings()


class StripeSettings(PolvoBaseSettings):
    STRIPE_API_KEY: Optional[str] = None
