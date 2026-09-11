import os
from typing import Final

from dotenv import load_dotenv

load_dotenv()


class Settings:
    DATABASE_URL: Final[str | None] = os.getenv("DATABASE_URL")
    GOOGLE_API_KEY: Final[str | None] = os.getenv("GOOGLE_API_KEY")
    API_BASE_URL: Final[str] = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
    PORT: Final[int] = int(os.getenv("PORT", "8000"))
    UPLOAD_DIR: Final[str] = os.getenv("UPLOAD_DIR", "api/uploads")
    CORS_ALLOWED_ORIGINS: Final[str] = os.getenv("CORS_ALLOWED_ORIGINS", "*")


settings = Settings()


def get_database_url() -> str:
    if not settings.DATABASE_URL:
        raise RuntimeError("DATABASE_URL is not configured.")
    return settings.DATABASE_URL


def require_google_api_key() -> str:
    if not settings.GOOGLE_API_KEY:
        raise RuntimeError("GOOGLE_API_KEY is not configured.")
    return settings.GOOGLE_API_KEY
