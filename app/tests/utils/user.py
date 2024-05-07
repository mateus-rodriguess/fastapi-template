from httpx import AsyncClient
from sqlmodel import Session

from app.core.settings import get_settings
from app.db.repositories.user import UserRepository
from app.models.user import User, UserCreate, UserUpdate
from app.tests.utils.utils import (random_email, random_lower_string,
                                   random_password)

settings = get_settings()

user_date_create = {
    "email": "user@example.com",
    "password": "insecure!secret@KEY",
    "full_name": "string",

}


async def user_authentication_headers(*, client: AsyncClient, email: str, password: str) -> dict[str, str]:
    data = {"username": email, "password": password}
    response = await client.post(f"{settings.API_V1_STR}/login/access-token", data=data)
    data = response.json()
    return {"Authorization": f"Bearer {data.get("access_token")}"}


async def create_random_user(session: Session) -> User:
    user_in = UserCreate(email=random_email(
    ), password=random_password(), full_name=random_lower_string())
    return await UserRepository.create_user(session, user_in)


async def authentication_token_email(*, client: AsyncClient, session: Session, email: str) -> dict[str, str]:

    user = await UserRepository.get_user_by_email(session, email)
    password = random_password()
    if not user:
        user = await UserRepository.create_user(session, UserCreate(email=email, password=password))
    else:
        if not user.uuid:
            raise Exception("User uuid not set")
        user = await UserRepository.update_user_me(session, user, UserUpdate(password=password))
    return await user_authentication_headers(client=client, email=email, password=password)
