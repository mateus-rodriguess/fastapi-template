from typing import AsyncIterator

import redis.asyncio as aredis
from redis import Redis

from app.core.settings import get_settings

settings = get_settings()

HOST = settings.REDIS_HOST
PORT = settings.REDIS_PORT
PASSWORD = settings.REDIS_PASSWORD


def create_redis_pool():
    return aredis.ConnectionPool.from_url(settings.REDIS_URL, encoding="utf-8")


async def get_redis() -> AsyncIterator[Redis]:
    pool = create_redis_pool()
    session = await aredis.Redis(connection_pool=pool, decode_responses=True)
    try:
        yield session
    finally:
        await session.close()
