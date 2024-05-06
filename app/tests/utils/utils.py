import random
import string

from httpx import AsyncClient

from app.core.settings import get_settings

settings = get_settings()


def random_email() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_password() -> str:
    return ''.join([random.choice(string.ascii_letters + string.digits + string.punctuation ) for n in range(12)])


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


async def get_superuser_token_headers(client: AsyncClient) -> dict[str, str]:
    data = {
        "email": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD
    }
    
    response = await client.post(f"{settings.API_V1_STR}/login/acess-token", json=data).json()
    
    return {"Authorization": f"Bearer {response.get("access_token")}"}
