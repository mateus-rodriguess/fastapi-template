import uvicorn

from app.app import DEBUG, app
from app.utils.logger import logger

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=DEBUG)
