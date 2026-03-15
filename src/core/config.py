from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    DATABASE_URL: str
    OPENAI_API_KEY: str | None = None
    PROJECT_NAME: str = "CorpKnow AI"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"  # Игнорировать лишние переменные в .env
    )

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()