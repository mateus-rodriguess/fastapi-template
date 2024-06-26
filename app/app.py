from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi_pagination import add_pagination
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.cors import CORSMiddleware

from app.api.api_v1.api import api_router
from app.api.api_v1.deps import lifespan
from app.core.settings import get_settings
from app.middlewares.authentication import (
    BearerTokenAuthBackend,
    on_auth_error,
)
from app.middlewares.exception_handler import (
    ExceptionHandlerMiddleware,
    validate_error_exception_handler,
)
from app.middlewares.utils_header import header_utils
from app.utils.indentifier import custom_generate_unique_id

settings = get_settings()

APP_NAME = settings.APP_NAME
VERSION = settings.VERSION
DEBUG = settings.DEBUG
DESCRIPTION = settings.DESCRIPTION
DESCRIPTION_AUTH = settings.DESCRIPTION_AUTH
BACKEND_CORS_ORIGINS = settings.BACKEND_CORS_ORIGINS


app = FastAPI(
    debug=DEBUG,
    version=VERSION,
    title=APP_NAME,
    description=DESCRIPTION,
    openapi_url="/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin).strip("/") for origin in BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(ExceptionHandlerMiddleware)
app.add_middleware(
    AuthenticationMiddleware,
    backend=BearerTokenAuthBackend(),
    on_error=on_auth_error,
)

app.add_exception_handler(
    RequestValidationError, validate_error_exception_handler
)
app.middleware("http")(header_utils)
app.add_middleware(CorrelationIdMiddleware)
app.include_router(router=api_router)

add_pagination(app)
