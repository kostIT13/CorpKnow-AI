from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    DATABASE_URL: str

    CHROMA_HOST: str = "chromadb"
    CHROMA_PORT: str = "8000"
    CHROMA_COLLECTION: str = "corp_docs"

    OLLAMA_HOST: str = "http://ollama:11434"
    OLLAMA_EMBEDDING_MODEL: str = "nomic-embed-text"
    OLLAMA_LLM_MODEL: str = "llama3.2:3b"
    OLLAMA_TOKEN: str = "7LAxUKXNzRZCKzGyT1974GTM6DSXzf9Huou_lsSjdmM"

    OPENAI_API_KEY: str | None = None
    PROJECT_NAME: str = "CorpKnow AI"

    ENVIRONMENT: str = "development"

    SECRET_KEY: str 
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"
    )

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()