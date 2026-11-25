"""APScheduler integration: scheduled crawling jobs."""
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from loguru import logger

from app.core.config import settings
from app.crawler.pipelines import run_all
from app.crawler.sites import ALL_SPIDERS

_scheduler: AsyncIOScheduler | None = None


async def _crawl_job() -> None:
    logger.info("Scheduled crawl starting")
    try:
        results = await run_all(ALL_SPIDERS)
        for r in results:
            logger.info(f"Crawl done: {r}")
    except Exception as e:  # noqa: BLE001
        logger.exception(f"Scheduled crawl failed: {e}")


def start_scheduler() -> AsyncIOScheduler:
    global _scheduler
    if _scheduler is not None:
        return _scheduler
    _scheduler = AsyncIOScheduler()
    if settings.scheduler_enabled and settings.scheduler_crawl_cron:
        trigger = CronTrigger.from_crontab(settings.scheduler_crawl_cron)
        _scheduler.add_job(_crawl_job, trigger, id="crawl_all", coalesce=True)
        logger.info(f"Scheduler enabled, cron='{settings.scheduler_crawl_cron}'")
    else:
        logger.info("Scheduler disabled")
    _scheduler.start()
    return _scheduler


async def stop_scheduler() -> None:
    global _scheduler
    if _scheduler is not None:
        await _scheduler.shutdown(wait=False)
        _scheduler = None
