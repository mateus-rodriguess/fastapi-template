import pytest
from fastapi import status
from httpx import AsyncClient

from app.core.settings import get_settings

settings = get_settings()


@pytest.mark.anyio
async def test_health(client: AsyncClient, headers: dict[str, str]) -> None:
    url = f"{settings.API_V1_STR}/health"
    response = await client.get(url=url, headers=headers)

    data = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert data == {"detail": "OK"}

    assert response.headers["x-process-time"]
    assert response.headers["x-request-id"]
    assert response.headers["user-agent"]
