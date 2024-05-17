from typing import Any

from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.orm import sessionmaker
from sqlmodel import create_engine, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.settings import get_settings
from app.db.repositories.users import UserRepository
from app.models.users import UserCreate, Users

settings = get_settings()

engine = AsyncEngine(create_engine(settings.DATABASE_URI, future=True))


async def init_db() -> Any:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        user = await session.exec(
            select(Users).where(Users.email == settings.FIRST_SUPERUSER)
        )
        if not user.first():
            user_in = UserCreate(
                email=settings.FIRST_SUPERUSER,
                password=settings.FIRST_SUPERUSER_PASSWORD,
                is_superuser=True,
                full_name=settings.FIRST_FULL_NAME,
            )
            return await UserRepository.create_user(
                session=session, user_create=user_in
            )
