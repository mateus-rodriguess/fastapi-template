"""
Initializes app uvicorn
"""

import uvicorn

from app.app import app
from app.core.settings import get_settings
from app.utils.logger import logger

settings = get_settings()
ENVIRONMENT = settings.ENVIRONMENT

if __name__ == "__main__":
    info_app = f"{app.title} - version: {app.version}"
    info_app += f" - debug: {app.debug} - ENV: {ENVIRONMENT}"
    logger.info(info_app)
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
