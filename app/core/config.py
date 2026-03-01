from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
    )

    APP_ENV: str
    DEBUG: bool
    PROJECT_NAME: str

    DATABASE_URL: str

settings = Settings()

POSTGRES_URL = settings.DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")