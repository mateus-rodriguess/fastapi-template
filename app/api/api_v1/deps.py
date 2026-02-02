from collections.abc import AsyncGenerator, AsyncIterator
from contextlib import asynccontextmanager
from typing import Annotated

import redis.asyncio as redis
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.orm import sessionmaker
from sqlmodel import create_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.settings import get_settings
from app.models.users import TokenPayload, Users

settings = get_settings()

engine = AsyncEngine(create_engine(settings.DATABASE_URL, future=True))

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=settings.URL_ACCESS_TOKEN,
    scheme_name="JWT",
    description=settings.DESCRIPTION_AUTH,
)

TokenDep = Annotated[str, Depends(reusable_oauth2)]


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async_session = sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
    )
    async with async_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]


async def get_current_user(session: SessionDep, token: TokenDep) -> Users:
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError) as exception:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials.",
        ) from exception
    user = await session.get(Users, token_data.sub)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user."
        )
    return user


CurrentUser = Annotated[Users, Depends(dependency=get_current_user)]


async def get_current_active_superuser(current_user: CurrentUser) -> Users:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user doesn't have enough privileges.",
        )
    return current_user


CurrentSuperUser = Annotated[Users, Depends(dependency=get_current_active_superuser)]


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis.from_url(
        url=settings.REDIS_URL,
        encoding="utf-8",
    )
    yield
