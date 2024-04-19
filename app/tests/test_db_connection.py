from app.db.connection import engine


async def test_db_connection():
    async with engine.connect() as connection:
        await connection.close()
