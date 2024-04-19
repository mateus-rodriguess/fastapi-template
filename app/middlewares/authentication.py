from fastapi import status
from jose import JWTError, jwt
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.authentication import (AuthCredentials, AuthenticationBackend,
                                      AuthenticationError)
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.core.settings import get_settings
from app.db.connection import engine
from app.models.user import User

settings = get_settings()


def on_auth_error(request: Request, exc: Exception):
    status_code = status.HTTP_401_UNAUTHORIZED
    if len(exc.args) > 1:
        status_code = exc.args[1]
    return JSONResponse({"detail": str(exc.args[0])}, status_code=status_code)


class BearerTokenAuthBackend(AuthenticationBackend):

    async def authenticate(self, request):
        if "Authorization" not in request.headers:
            return

        auth: str = request.headers["Authorization"]

        try:
            scheme, token = auth.split()
            if scheme.lower() != "bearer":
                return

            decoded = jwt.decode(
                token=token,
                key=settings.JWT_SECRET,
                algorithms=[settings.JWT_ALGORITHM],
            )
        except (ValueError, UnicodeDecodeError, JWTError) as error:
            raise AuthenticationError("Invalid JWT Token.")
        async_session = AsyncSession(
            engine, expire_on_commit=False, autoflush=False
        )

        async with async_session as session:
            user = await session.get(User, decoded.get("sub"))

        if not user:
            raise AuthenticationError(
                "User not found.", status.HTTP_404_NOT_FOUND
            )
        if not user.is_active:
            raise AuthenticationError(
                "Inactive user.", status.HTTP_400_BAD_REQUEST
            )

        return AuthCredentials(["authenticated"]), user.email
