import os
from functools import cache
from typing import Annotated, Any, Literal

from dotenv import load_dotenv
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

load_dotenv(override=True)
ENVIRONMENT = os.getenv("ENVIRONMENT", "production")

def parse_cors(value: Any) -> list[str] | str:
    if isinstance(value, str) and not value.startswith("["):
        return [i.strip() for i in value.split(",")]
    if isinstance(value, list | str):
        return value
    raise ValueError(value)


class Settings(BaseSettings):
    """
    # Example
    ```python
        from app.core.settings import get_settings

        settings = get_settings()
        VERSION = settings.VERSION
    ```

    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        case_sensitive=True,
        extra="ignore",
        env_file_encoding="utf-8",
    )

    APP_NAME: str = "FastAPI Template"
    VERSION: str = "0.0.1"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: Literal["local", "staging", "production"] = ENVIRONMENT
    DEBUG: bool = ENVIRONMENT == "local"
    DOMAIN: str = "localhost"
    DESCRIPTION: str = description
    DESCRIPTION_AUTH: str = description_auth

    HOST: str = "0.0.0.0"
    PORT: int = 8000
    BASE_URL: str = f"http://{HOST}/{PORT}"
    
    URL_ACCESS_TOKEN: str = f"{API_V1_STR}/login/access-token"
    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = []

    SECRET_KEY: str = "insecure!717-4562-b3fc-2c963f66afa6Y"
    JWT_ALGORITHM: str = "HS256"
    JWT_SECRET: str = "insecure!717-4562-b3fc-2c963f66afa6"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10 * 24 * 60  # 10 days

    DATABASE_URI: str = "sqlite+aiosqlite:///./sql_app.db"

    REDIS_HOST: str = "redis-cache"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = "insecure!secret@KEY"
    REDIS_URL: str = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/0"

    FIRST_SUPERUSER: str = "admin@example.com"
    FIRST_SUPERUSER_PASSWORD: str = "insecure!secret@KEY"
    FIRST_FULL_NAME: str = "admin"

    FIRST_SUPERUSER_TEST: str = "admin_test@example.com"
    FIRST_SUPERUSER_PASSWORD_TEST: str = "insecure!secret@KEY2"
    FIRST_FULL_NAME_TEST: str = "admin_test"
    EMAIL_ANY_TEST: str = "eeezlotjpbrddoeybnvqnoipsgpsjtst@any.com"


@cache
def get_settings() -> Settings:
    return Settings()
