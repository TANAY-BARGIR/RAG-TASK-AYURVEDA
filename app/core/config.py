from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    # Application config
    PROJECT_NAME: str = "Ayurvedic Grantha Reference System"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Database config
    DATABASE_URL: str = "sqlite:///./db/ayurveda.db"
    
    # Vector DB config
    CHROMA_PERSIST_DIRECTORY: str = "./db/chroma_db"
    CHROMA_COLLECTION_NAME: str = "ayurveda_texts"

    # RAG Settings
    SUPPORTED_THRESHOLD: float = 0.85
    PARTIAL_THRESHOLD: float = 0.70
    TOP_K_RETRIEVAL: int = 5
    MAX_TOP_K_RETRIEVAL: int = 20
    MAX_QUERY_LENGTH: int = 500
    MAX_LIST_LIMIT: int = 200

    # API Keys
    NVIDIA_API_KEY: str = ""

    # Auth for write endpoints (POST /ingredients, /formulations). Must be set
    # explicitly; an empty value disables writes rather than silently allowing them.
    ADMIN_API_KEY: str = ""

    # Comma-separated list of allowed browser origins for CORS.
    ALLOWED_ORIGINS: str = "http://localhost:3000"

    # Rate limit applied to /api/v1/search (it triggers billed NVIDIA API calls).
    SEARCH_RATE_LIMIT: str = "20/minute"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=True, extra="ignore")

    @property
    def origins_list(self) -> list[str]:
        return [o.strip() for o in self.ALLOWED_ORIGINS.split(",") if o.strip()]

@lru_cache
def get_settings() -> Settings:
    return Settings()
