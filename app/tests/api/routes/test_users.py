import pytest
from fastapi import status
from httpx import AsyncClient

from app.core.settings import get_settings
from app.tests.utils.user import user_date_create

settings = get_settings()


@pytest.mark.anyio
async def test_user_create(client: AsyncClient) -> None:
    response = await client.post(
        f"{settings.API_V1_STR}/users", json=user_date_create
    )
    data = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert data["uuid"]
    assert data["email"]
    assert data["full_name"]
    assert data["is_active"] == True
    assert data["is_superuser"] == False


@pytest.mark.anyio
async def test_user_not_authenticated(client: AsyncClient) -> None:
    respone = await client.get(
        f"{settings.API_V1_STR}/users/me",
        headers={"Authorization": "Bearer no_authenticated"},
    )

    assert respone.json()
    assert respone.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.anyio
async def test_get_all_users(
    client: AsyncClient, token_headers: dict[str, str]
) -> None:
    response = await client.get(
        f"{settings.API_V1_STR}/users", headers=token_headers
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()


@pytest.mark.anyio
async def test_get_user(
    client: AsyncClient, token_headers: dict[str, str]
) -> None:
    resposen_users = await client.get(
        f"{settings.API_V1_STR}/users", headers=token_headers
    )

    uuid: str = resposen_users.json()["items"][1]["uuid"]
    response = await client.get(
        f"{settings.API_V1_STR}/users/{uuid}", headers=token_headers
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()


@pytest.mark.anyio
async def test_get_user_not_found(
    client: AsyncClient, token_headers: dict[str, str]
) -> None:
    response = await client.get(
        f"{settings.API_V1_STR}/users/248ac98f-552e-4b33-aa66-c36e6024cec3",
        headers=token_headers,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Not found."}


async def test_delete_user(
    client: AsyncClient, token_headers: dict[str, str]
) -> None:

    data = await client.get(
        f"{settings.API_V1_STR}/users", headers=token_headers
    )
    uuid = data.json()["items"][0]["uuid"]
    response = await client.delete(
        f"{settings.API_V1_STR}/users/{uuid}", headers=token_headers
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"detail": "User deleted successfully."}
