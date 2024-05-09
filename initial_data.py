"""
    This function initializes the data for the application. It connects to the bank
    data and checks if the initial data is already configured. If not,
    creates the initial data.
"""
import asyncio

from app.db.connection import init_db
from app.utils.logger import logger


async def init_data() -> None:
    """Initializes the data for the application"""
    logger.info("Creating initial data")
    if not await init_db():
        logger.info("start data is already set.")
    else:
        logger.info("Initial data created.")


if __name__ == "__main__":
    asyncio.run(init_data())
