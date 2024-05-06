import pytest
from fastapi import status
from httpx import AsyncClient

from app.core.settings import get_settings

settings = get_settings()


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
    response = await client.get(
        f"{settings.API_V1_STR}/users/1", headers=token_headers
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()


@pytest.mark.anyio
async def test_get_user_not_found(
    client: AsyncClient, token_headers: dict[str, str]
) -> None:
    response = await client.get(
        f"{settings.API_V1_STR}/users/999999999999", headers=token_headers
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Not found."}


async def test_delete_user(
    client: AsyncClient, token_headers: dict[str, str]
) -> None:
    response = await client.delete(
        f"{settings.API_V1_STR}/users/1", headers=token_headers
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"detail": "User deleted successfully."}
