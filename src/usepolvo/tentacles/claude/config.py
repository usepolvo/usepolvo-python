from functools import lru_cache
from typing import Optional

from usepolvo.beak.config import PolvoBaseSettings


@lru_cache
def get_settings():
    return ClaudeSettings()


class ClaudeSettings(PolvoBaseSettings):
    CLAUDE_API_KEY: Optional[str] = None
