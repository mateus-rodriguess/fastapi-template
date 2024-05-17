import pytest
from fastapi import status
from httpx import AsyncClient
from sqlmodel import Session

from app.core.settings import get_settings
from app.db.repositories.users import UserRepository
from app.models.users import UserCreate, Users, UserUpdate
from app.tests.utils.utils import (
    random_email,
    random_lower_string,
    random_password,
)

settings = get_settings()

url_token = settings.URL_ACCESS_TOKEN
user_date_create_any = {
    "email": random_email(),
    "password": random_password(),
    "full_name": random_lower_string(),
}
data_super_user = {
    "username": settings.FIRST_SUPERUSER_TEST,
    "password": settings.FIRST_SUPERUSER_PASSWORD_TEST,
}


def check_status_code(resposne_status: int, status: int) -> None:
    detail = f"Response status ->  {resposne_status} - status -> {status}"
    if resposne_status == status:
        raise Exception(detail)


async def get_superuser_token_headers(client: AsyncClient) -> dict[str, str]:

    response = await client.post(url=url_token, data=data_super_user)
    with pytest.raises(Exception):
        assert check_status_code(response.status_code, status.HTTP_200_OK)

    data: dict = response.json()
    access_token: str | None = data.get("access_token", None)
    return {"Authorization": f"Bearer {access_token}"}


async def user_authentication_headers(
    *, client: AsyncClient, email: str, password: str
) -> dict[str, str]:
    data = {"username": email, "password": password}
    response = await client.post(url=url_token, data=data)
    with pytest.raises(Exception):
        assert check_status_code(response.status_code, status.HTTP_200_OK)
    data: dict = response.json()
    access_token = data.get("access_token", None)
    return {"Authorization": f"Bearer {access_token}"}


async def create_random_user(session: Session) -> Users:
    user_in = UserCreate(
        email=random_email(),
        password=random_password(),
        full_name=random_lower_string(),
    )
    return await UserRepository.create_user(session, user_in)


async def authentication_token_email(
    *, client: AsyncClient, session: Session, email: str
) -> dict[str, str]:
    password = random_password()
    user = await UserRepository.get_user_by_email(session, email)
    if not user:
        user = await UserRepository.create_user(
            session, UserCreate(email=email, password=password)
        )
    else:
        if not user.uuid:
            raise
        user = await UserRepository.update_user_me(
            session, user, UserUpdate(password=password)
        )
    return await user_authentication_headers(
        client=client, email=email, password=password
    )
