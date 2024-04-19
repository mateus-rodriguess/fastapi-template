import asyncio

from app.db.connection import init_db
from app.utils.logger import logger


async def init_data() -> None:
    logger.info("Creating initial data")
    if not await init_db():
        logger.info("start data is already set.")
    else:
        logger.info("Initial data created.")


if __name__ == "__main__":
    asyncio.run(init_data())
