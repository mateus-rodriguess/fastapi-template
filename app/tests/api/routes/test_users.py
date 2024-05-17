import pytest
from fastapi import status
from httpx import AsyncClient

from app.core.settings import get_settings
from app.tests.utils.users import user_date_create_any
from app.tests.utils.utils import random_lower_string, random_password

settings = get_settings()
url_users: str = f"{settings.API_V1_STR}/users"


@pytest.mark.anyio
async def test_user_create(
    client: AsyncClient, superuser_headers: dict[str, str]
) -> None:

    response = await client.post(url_users, json=user_date_create_any)
    data = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert data["uuid"]
    assert data["email"]
    assert data["full_name"]
    assert data["is_active"] is True
    assert data["is_superuser"] is False

    uuid = data["uuid"]
    response = await client.delete(
        f"{url_users}/{uuid}",
        headers=superuser_headers,
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"detail": "User deleted successfully."}


@pytest.mark.anyio
async def test_user_not_authenticated(client: AsyncClient) -> None:
    headers = {"Authorization": "Bearer no_authenticated"}
    respone = await client.get(url=f"{url_users}/me", headers=headers)

    assert respone.json()
    assert respone.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.anyio
async def test_get_all_users(
    client: AsyncClient, headers: dict[str, str]
) -> None:
    response = await client.get(url_users, headers=headers)
    data = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert data
    assert data["page"]
    assert data["items"]
    assert data["size"]
    assert data["pages"]


@pytest.mark.anyio
async def test_get_user(client: AsyncClient, headers: dict[str, str]) -> None:
    resposen_users = await client.get(url_users, headers=headers)

    uuid: str = resposen_users.json()["items"][1]["uuid"]
    response = await client.get(f"{url_users}/{uuid}", headers=headers)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()


@pytest.mark.anyio
async def test_get_user_not_found(
    client: AsyncClient, headers: dict[str, str]
) -> None:
    uuid_any: str = "248ac98f-552e-4b33-aa66-c36e6024cec3"
    response = await client.get(f"{url_users}/{uuid_any}", headers=headers)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Not found."}


@pytest.mark.anyio
async def test_create_user_exists(client: AsyncClient):
    data = {
        "email": settings.FIRST_SUPERUSER_TEST,
        "password": random_password(),
        "full_name": random_lower_string(),
    }
    response = await client.post(url_users, json=data)
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json() == {
        "detail": "The user with this email already exists in the system."
    }


async def test_delete_user_error(
    client: AsyncClient, headers: dict[str, str]
) -> None:

    data = await client.get(url_users, headers=headers)
    uuid = data.json()["items"][0]["uuid"]

    response = await client.delete(f"{url_users}/{uuid}", headers=headers)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "detail": "The user doesn't have enough privileges."
    }
