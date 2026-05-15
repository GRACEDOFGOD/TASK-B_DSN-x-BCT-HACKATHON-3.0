"""
Configuration — loaded from environment / .env file
"""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Groq API
    GROQ_API_KEY: str = ""

    # Model
    MODEL_NAME: str = "llama-3.3-70b-versatile"
    MAX_TOKENS_PROFILE: int = 400
    MAX_TOKENS_RECOMMEND: int = 1500
    MAX_TOKENS_MULTITURN: int = 400
    TEMPERATURE_PROFILE: float = 0.2
    TEMPERATURE_RECOMMEND: float = 0.6
    TEMPERATURE_MULTITURN: float = 0.7

    # App
    APP_NAME: str = "DSN x BCT Task B — Recommendation Agent"
    DEFAULT_NUM_RECS: int = 10
    MAX_NUM_RECS: int = 20

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
