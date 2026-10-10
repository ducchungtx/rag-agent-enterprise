from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Default OpenAI-compatible base URLs when provider is mistral / gemini.
_PROVIDER_BASE_URLS = {
    "mistral": "https://api.mistral.ai/v1",
    "gemini": "https://generativelanguage.googleapis.com/v1beta/openai/",
}


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "rag-agent-enterprise"
    debug: bool = True
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/rag_enterprise"
    jwt_secret: str = "dev-only-change-me"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    redis_url: str = "redis://localhost:6379/0"
    use_async_ingest: bool = False
    data_dir: str = "./data/uploads"
    embedding_dim: int = 384
    embedding_provider: str = "fake"  # fake | openai | mistral | gemini
    chat_provider: str = "fake"  # fake | openai | mistral | gemini
    llm_base_url: str = "http://localhost:11434/v1"
    llm_api_key: str = "ollama"
    mistral_api_key: str = ""
    gemini_api_key: str = ""
    embedding_model: str = "nomic-embed-text"
    chat_model: str = "qwen2.5:7b"
    # M6.0: từ chối chat nếu max citation score < ngưỡng (0–1, hybrid-lite)
    retrieval_min_score: float = 0.22
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    def ensure_data_dir(self) -> Path:
        path = Path(self.data_dir)
        path.mkdir(parents=True, exist_ok=True)
        return path

    def resolved_llm_api_key(self, provider: str | None = None) -> str:
        """Pick API key for a provider. Keep many keys in .env; switch via CHAT_PROVIDER."""
        p = provider or self.chat_provider
        if p == "mistral" and self.mistral_api_key.strip():
            return self.mistral_api_key.strip()
        if p == "gemini" and self.gemini_api_key.strip():
            return self.gemini_api_key.strip()
        return self.llm_api_key

    def resolved_llm_base_url(self, provider: str | None = None) -> str:
        """Auto base URL for mistral/gemini; otherwise LLM_BASE_URL."""
        p = provider or self.chat_provider
        if p in _PROVIDER_BASE_URLS:
            return _PROVIDER_BASE_URLS[p]
        return self.llm_base_url

    def uses_openai_compatible_chat(self) -> bool:
        return self.chat_provider in {"openai", "mistral", "gemini"}

    def uses_openai_compatible_embed(self) -> bool:
        return self.embedding_provider in {"openai", "mistral", "gemini"}


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
