"""FastAPI application entry point."""
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.exhibitions import router as exhibitions_router
from app.core.config import settings
from app.core.database import init_db
from app.core.logging import logger, setup_logging
from app.crawler.scheduler import start_scheduler, stop_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    logger.info(f"Starting {settings.app_name}")
    await init_db()
    scheduler = start_scheduler()
    yield
    await stop_scheduler()
    logger.info("Shutdown complete")


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    lifespan=lifespan,
)

api_prefix = settings.api_v1_prefix
app.include_router(exhibitions_router, prefix=api_prefix)


@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "name": settings.app_name}


@app.get("/")
async def root() -> dict:
    return {
        "name": settings.app_name,
        "docs": "/docs",
        "api": api_prefix,
    }
