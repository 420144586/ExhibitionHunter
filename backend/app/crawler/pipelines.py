"""Pipeline: clean, dedup, persist crawled items to the database."""
from collections.abc import AsyncIterator
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import AsyncSessionLocal
from app.models.exhibition import Exhibition
from app.schemas.exhibition import ExhibitionCreate
from app.crawler.base import BaseSpider


async def _upsert(session: AsyncSession, item: ExhibitionCreate) -> bool:
    """Insert-or-update by (source_site, source_id). Returns True if new row."""
    stmt = select(Exhibition.id).where(
        Exhibition.source_site == item.source_site,
        Exhibition.source_id == item.source_id,
    )
    existing = (await session.execute(stmt)).scalar_one_or_none()
    if existing is None:
        session.add(Exhibition(**item.model_dump()))
        return True
    # Update fields
    await session.execute(
        Exhibition.__table__.update()
        .where(Exhibition.id == existing)
        .values(**item.model_dump(exclude={"source_site", "source_id"}))
    )
    return False


async def run_spider(spider: BaseSpider) -> dict:
    """Run a spider end-to-end: crawl -> clean -> upsert. Returns stats."""
    stats = {"site": spider.name, "fetched": 0, "new": 0, "updated": 0}
    async with AsyncSessionLocal() as session:
        async for item in spider.run():
            stats["fetched"] += 1
            try:
                is_new = await _upsert(session, item)
                stats["new" if is_new else "updated"] += 1
            except Exception:
                await session.rollback()
                raise
        await session.commit()
    return stats


async def run_all(spider_classes: list[type[BaseSpider]]) -> list[dict]:
    """Run multiple spiders sequentially. Returns per-spider stats."""
    results = []
    for cls in spider_classes:
        spider = cls()
        stats = await run_spider(spider)
        results.append(stats)
    return results
