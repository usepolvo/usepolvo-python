from functools import lru_cache
from typing import Optional

from usepolvo.beak.config import PolvoBaseSettings


@lru_cache
def get_settings():
    return GeminiSettings()


class GeminiSettings(PolvoBaseSettings):
    GEMINI_API_KEY: Optional[str] = None
