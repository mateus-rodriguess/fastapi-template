import pytest
from httpx import AsyncClient
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, delete
from sqlmodel.ext.asyncio.session import AsyncSession

from app.app import app
from app.core.settings import get_settings
from app.db.connection import engine, init_db
from app.models.user import User
from app.tests.utils.user import authentication_token_email
from app.tests.utils.utils import get_superuser_token_headers

settings = get_settings()


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session", autouse=True)
async def session() -> AsyncSession:  # type: ignore
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False, autoflush=False)
    async with async_session() as session:
        await init_db()
        yield session
        statement = delete(User)
        await session.exec(statement)
        await session.commit()
        
@pytest.fixture(scope="session")
async def client():
    async with AsyncClient(app=app, base_url="http://0.0.0.0") as client:
        yield client


@pytest.mark.asyncio(scope="module")
async def superuser_token_headers(client: AsyncClient) -> dict[str, str]:
    return await get_superuser_token_headers(client)


@pytest.fixture(scope="session")
async def token_headers(
    client: AsyncClient, session: Session
) -> dict[str, str]:
    return await authentication_token_email(
        client=client, email=settings.FIRST_SUPERUSER, session=session
    )