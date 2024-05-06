import os
from functools import cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

description = """
    Template for FastAPI application. 
    Nested template, contains examples of how to create a robust application with FastAPI. 
    This API already contains authentication.
"""

description_auth = """
    Function for route authentication. In this example, the routes are authenticated by AUTH EXEMPLE, with JWT token.
"""

ENV = os.getenv("ENV")

if ENV in ["local", "staging", "production"]:
    ...
else:
    ENV = "local"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        case_sensitive=True,
        extra="ignore",
        env_file_encoding=" 'utf-8'",
    )

    APP_NAME: str = "FastAPI Back-End Template."
    VERSION: str = "0.0.1"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: Literal["local", "staging", "production"] = ENV
    DEBUG: bool = True if ENVIRONMENT == "local" else False
    DESCRIPTION: str = description
    DESCRIPTION_AUTH: str = description_auth

    DOMAIN: str = "localhost"
    # insecure secret key
    SECRET_KEY: str = (
        "VJHBINoirmJleHAiOjE3MTM1MzQwNzUsInN1UbEElqmZD1fHd6zn5jn54jbn5j4"
    )
    JWT_ALGORITHM: str = "HS256"
    # insecure secret key
    JWT_SECRET: str = (
        "eyJleHAiOjE3MTM1MzQwNzUsInN1YiI6IjEifQ.ZUbE-ElqmZD1fHd6zn5-PxxIdcvIhfqxybZPuRkCse0"
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = (
        60 * 24 * 10
    )  # 60 minutes * 24 hours * 8 days = 10 days

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
