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

    SECRET_KEY: str 
    JWT_ALGORITHM: str 
    JWT_SECRET: str 
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10 * 24 * 60  # 10 days

    DATABASE_URI: str = "sqlite+aiosqlite:///./sql_app.db"

    REDIS_URL: str

    FIRST_SUPERUSER: str
    FIRST_SUPERUSER_PASSWORD: str
    FIRST_FULL_NAME: str

    FIRST_SUPERUSER_TEST: str 
    FIRST_SUPERUSER_PASSWORD_TEST: str 
    FIRST_FULL_NAME_TEST: str 
    EMAIL_ANY_TEST: str


@cache
def get_settings() -> Settings:
    return Settings()
