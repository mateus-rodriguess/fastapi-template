import pytest
from redis import asyncio

from app.db.connection import engine
from app.db.redis_connection import get_redis


@pytest.mark.anyio
async def test_db_connection():
    async with engine.connect() as connection:
        await connection.close()


@pytest.mark.anyio
async def test_redis_connection():
    _: asyncio.Redis = get_redis()
