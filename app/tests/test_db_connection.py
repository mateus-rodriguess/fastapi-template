import pytest

from app.db.connection import engine


@pytest.mark.anyio
async def test_db_connection():
    async with engine.connect() as connection:
        await connection.close()
