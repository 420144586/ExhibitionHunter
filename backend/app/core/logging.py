"""Loguru logging setup."""
import sys
from loguru import logger

from app.core.config import settings


def setup_logging() -> None:
    logger.remove()
    logger.add(
        sys.stderr,
        level=settings.log_level,
        enqueue=True,
        backtrace=settings.debug,
        diagnose=settings.debug,
    )
    logger.add(
        settings.log_dir + "/app_{time:YYYY-MM-DD}.log",
        level=settings.log_level,
        rotation="10 MB",
        retention="14 days",
        encoding="utf-8",
        enqueue=True,
    )


__all__ = ["logger", "setup_logging"]
