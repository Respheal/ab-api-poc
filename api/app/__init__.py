from functools import lru_cache

from app.utils.config import Settings


@lru_cache
def get_settings() -> Settings:
    return Settings()
