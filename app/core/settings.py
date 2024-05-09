import os
import secrets
from functools import cache
from typing import Annotated, Any, Literal

from pydantic import AnyUrl, BeforeValidator
from pydantic_settings import BaseSettings, SettingsConfigDict

description = """
    Template for FastAPI application.
    Nested template, contains examples of how to create a robust
    application with FastAPI. This API already contains authentication.
"""

description_auth = """
    Function for route authentication. In this example, the routes are
    authenticated by AUTH EXEMPLE, with JWT token.
"""

ENV = os.getenv("ENV")

if ENV in ["local", "staging", "production"]:
    ...
else:
    ENV = "local"


def parse_cors(value: Any) -> list[str] | str:
    if isinstance(value, str) and not value.startswith("["):
        return [i.strip() for i in value.split(",")]
    if isinstance(value, list | str):
        return value
    raise ValueError(value)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        case_sensitive=True,
        extra="ignore",
        env_file_encoding=" 'utf-8'",
    )

    APP_NAME: str = "FastAPI Back-End Template"
    VERSION: str = "0.0.1"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: Literal["local", "staging", "production"] = ENV
    DEBUG: bool = ENVIRONMENT == "local"
    DESCRIPTION: str = description
    DESCRIPTION_AUTH: str = description_auth

    BASE_URL: str = "http://0.0.0.0"
    URL_ACCESS_TOKEN: str = f"{API_V1_STR}/login/access-token"
    DOMAIN: str = "localhost"
    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = []
    SECRET_KEY: str = secrets.token_urlsafe(32)
    JWT_ALGORITHM: str = "HS256"
    JWT_SECRET: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10 * 24 * 60  # 10 days

    DATABASE_URI: str = "sqlite+aiosqlite:///./sql_app.db"

    FIRST_SUPERUSER: str = "admin@example.com"
    FIRST_SUPERUSER_PASSWORD: str = "insecure!secret@KEY"
    FIRST_FULL_NAME: str = "admin"


@cache
def get_settings() -> Settings:
    """
    ## Example
    ```python
        from app.core.settings import get_settings

        settings = get_settings()
        VERSION = settings.VERSION
    ```

    """
    return Settings()
