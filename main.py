"""
Initializes app uvicorn
"""

import uvicorn

from app.app import DEBUG, app
from app.utils.logger import logger

if __name__ == "__main__":
    info_app = f"{app.title} - version: {app.version} - debug: {app.debug}"
    logger.info(info_app)
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=DEBUG)
