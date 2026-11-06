from pathlib import Path
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Script Scrapper"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"

    # Host & Server Configuration
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    UVICORN_WORKERS: int = 2

    # Database Configuration (PostgreSQL 16 via asyncpg)
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@127.0.0.1:5432/script_scrapper"
    DB_POOL_SIZE: int = 15
    DB_MAX_OVERFLOW: int = 5
    DB_POOL_TIMEOUT: float = 30.0
    DB_POOL_RECYCLE: float = 1800.0
    DB_ECHO: bool = False

    # Security
    SECRET_KEY: str = "insecure-gate1-dev-key-change-in-production-only-abcdef123456"
    SESSION_EXPIRE_HOURS: int = 24

    # Storage Paths
    STORAGE_DIR: str = str(Path(__file__).resolve().parent.parent.parent.parent / "storage")

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://localhost",
        "https://127.0.0.1",
    ]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


settings = Settings()
