"""Async SQLAlchemy engine & session factory."""
from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


class Base(DeclarativeBase):
    """Declarative base for all ORM models."""


def _database_url() -> str:
    """Return the engine URL, resolving SQLite paths to absolute form.

    ``settings.db_path`` already resolves relative SQLite paths against the
    backend root, so the database location no longer depends on the process
    working directory. Windows absolute paths are converted to the URL form
    (forward slashes plus a ``sqlite+aiosqlite:///`` drive-letter prefix);
    non-SQLite URLs are returned unchanged.
    """
    url = settings.database_url
    if url.startswith("sqlite"):
        return f"sqlite+aiosqlite:///{settings.db_path.as_posix()}"
    return url


engine = create_async_engine(
    _database_url(),
    echo=settings.debug,
    future=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency: yields an async DB session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def init_db() -> None:
    """Create all tables. Call on app startup."""
    # Import models so they register with Base.metadata
    from app import models  # noqa: F401

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
