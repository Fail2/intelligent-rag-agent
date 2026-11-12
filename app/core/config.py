from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    google_api_key: str | None = None
    embedding_model: str = "gemini-embedding-2"

    database_url: str = "sqlite+aiosqlite:///./data/app.db"
    chroma_persist_directory: str = "./data/chroma"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
