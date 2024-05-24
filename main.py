"""
Initializes app uvicorn
"""

import uvicorn

from app.app import app
from app.core.settings import get_settings
from app.utils.logger import logger

settings = get_settings()
ENVIRONMENT = settings.ENVIRONMENT
VERION = settings.VERSION
DEBUG = settings.DEBUG
TITLE = settings.APP_NAME

info_app = f"""
    {TITLE} - VERSION: {VERION} - DEBUG: {DEBUG} - ENV: {ENVIRONMENT}
    OpenAPI: {app.openapi_url}
"""

if __name__ == "__main__":
    logger.info(info_app)
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
