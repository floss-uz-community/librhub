from pydantic_settings import BaseSettings
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

class Settings(BaseSettings):
    APP_ENV: str
    DEBUG: bool
    PROJECT_NAME: str

    DATABASE_URL: str

    class Config:
        env_file = PROJECT_ROOT / ".env"
        env_file_encoding = "utf-8"

settings = Settings()