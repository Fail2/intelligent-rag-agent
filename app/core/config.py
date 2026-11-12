from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class Settings(BaseSettings):
    google_api_key: SecretStr | None = None
    groq_api_key: SecretStr | None = None
    brevo_api_key: SecretStr | None = None

    llm_model: str = "openai/gpt-oss-120b"
    embedding_model: str = "gemini-embedding-2"

    database_url: str = "sqlite+aiosqlite:///./data/app.db"
    chroma_persist_directory: str = "./data/chroma"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
