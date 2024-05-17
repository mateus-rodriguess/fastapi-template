import pytest
from asgi_lifespan import LifespanManager
from httpx import ASGITransport, AsyncClient
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.app import app
from app.core.settings import get_settings
from app.db.connection import engine
from app.db.repositories.users import UserRepository
from app.models.users import UserCreate, Users
from app.tests.utils.users import (
    authentication_token_email,
    get_superuser_token_headers,
)

settings = get_settings()


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


async def create_super_user_test(session: Session) -> None:
    user = await session.exec(
        select(Users).where(Users.email == settings.FIRST_SUPERUSER_TEST)
    )
    if not user.first():
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER_TEST,
            password=settings.FIRST_SUPERUSER_PASSWORD_TEST,
            is_superuser=True,
            is_active=True,
            full_name=settings.FIRST_FULL_NAME_TEST,
        )
        return await UserRepository.create_user(
            session=session, user_create=user_in
        )


@pytest.fixture(scope="session", autouse=True)
async def session() -> AsyncSession:  # type: ignore
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
    )
    async with async_session() as session:
        await create_super_user_test(session)
        yield session


@pytest.fixture(scope="session")
async def client():
    async with LifespanManager(app):
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url=settings.BASE_URL
        ) as client:
            yield client


@pytest.fixture(scope="session")
async def superuser_headers(client: AsyncClient) -> dict[str, str]:
    return await get_superuser_token_headers(client=client)


@pytest.fixture(scope="session")
async def headers(client: AsyncClient, session: Session) -> dict[str, str]:
    email = settings.EMAIL_ANY_TEST
    return await authentication_token_email(
        client=client, session=session, email=email
    )
