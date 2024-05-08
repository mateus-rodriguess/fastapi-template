"""
Initializes app uvicorn
"""
import uvicorn

from app.app import DEBUG, app
from app.utils.logger import logger

if __name__ == "__main__":
    logger.info(f"Starting: {app.title} - version: {app.version}")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=DEBUG)
