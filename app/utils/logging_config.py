import logging
import sys

from colorlog import ColoredFormatter

from app.core.settings import get_settings
from app.middlewares.request_context import request_id_ctx

LOG_FORMAT = (
    "%(log_color)s%(asctime)s | "
    "%(levelname)s | "
    "req=%(request_id)s | "
    "%(name)s:%(lineno)d | "
    "%(message)s"
)

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


class RequestIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id_ctx.get() or "-"
        return True


def setup_logging(log_level: str = "INFO") -> logging.Logger:
    settings = get_settings()
    formatter = ColoredFormatter(
        fmt=LOG_FORMAT,
        datefmt=DATE_FORMAT,
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        },
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    handler.addFilter(RequestIdFilter())

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.handlers.clear()
    root_logger.addHandler(handler)

    if settings.ENVIRONMENT == "production":
        logging.getLogger("urllib3").setLevel(logging.WARNING)

    for name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
        logger = logging.getLogger(name)
        logger.handlers.clear()
        logger.propagate = True
        logger.setLevel(logging.INFO)

    return root_logger


logger = setup_logging()
