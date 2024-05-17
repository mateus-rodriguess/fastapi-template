from math import ceil

from fastapi import HTTPException, Request, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.core.settings import get_settings
from app.utils.logger import logger

settings = get_settings()


class ExceptionHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if settings.DEBUG:
            return await call_next(request)
        try:
            return await call_next(request)
        except Exception as error:
            logger.fatal(error)
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=jsonable_encoder({"detail": "Internal server error."}),
            )


async def validate_error_exception_handler(
    _: Request, exc: RequestValidationError
):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )


async def limit_request_callback(
    request: Request, _: Response, pexpire: int
) -> None:

    expire = ceil(pexpire / 1000)
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        ip: str = forwarded.split(",")[0]
    else:
        ip: str = request.client.host + ":" + request.scope["path"]

    logger.debug(msg=f"Too Many Requests, IP: {ip}.")

    raise HTTPException(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        headers={"Retry-After": str(expire)},
        detail=f"Too Many Requests. Retry after {expire} seconds.",
    )
