from functools import lru_cache
from typing import Optional

from usepolvo.beak.config import PolvoBaseSettings


@lru_cache
def get_settings():
    return OpenAiSettings()


class OpenAiSettings(PolvoBaseSettings):
    OPENAI_API_KEY: Optional[str] = None
