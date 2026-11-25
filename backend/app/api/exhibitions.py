"""Exhibitions API: list (paginated) and manual crawl trigger."""
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.crawler.pipelines import run_all
from app.crawler.sites import ALL_SPIDERS
from app.models.exhibition import Exhibition
from app.schemas.exhibition import ExhibitionOut, ExhibitionPage

router = APIRouter(prefix="/exhibitions", tags=["exhibitions"])


@router.get("", response_model=ExhibitionPage)
async def list_exhibitions(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: str = Query("all", pattern="^(ongoing|upcoming|all)$"),
    city: str | None = None,
    industry: str | None = None,
    keyword: str | None = None,
    db: AsyncSession = Depends(get_db),
) -> ExhibitionPage:
    now = datetime.now()
    stmt = select(Exhibition)
    count_stmt = select(func.count()).select_from(Exhibition)

    # Status filter:
    #   ongoing  -> start_date <= now <= end_date
    #   upcoming -> start_date > now
    #   all      -> end_date >= now  (ongoing + upcoming, excludes ended)
    if status == "ongoing":
        cond = (Exhibition.start_date <= now) & (Exhibition.end_date >= now)
        stmt = stmt.where(cond)
        count_stmt = count_stmt.where(cond)
    elif status == "upcoming":
        cond = Exhibition.start_date > now
        stmt = stmt.where(cond)
        count_stmt = count_stmt.where(cond)
    else:  # all
        cond = Exhibition.end_date >= now
        stmt = stmt.where(cond)
        count_stmt = count_stmt.where(cond)

    if city:
        stmt = stmt.where(Exhibition.city == city)
        count_stmt = count_stmt.where(Exhibition.city == city)
    if industry:
        stmt = stmt.where(Exhibition.industry == industry)
        count_stmt = count_stmt.where(Exhibition.industry == industry)
    if keyword:
        like = f"%{keyword}%"
        stmt = stmt.where(Exhibition.title.like(like))
        count_stmt = count_stmt.where(Exhibition.title.like(like))

    total = (await db.execute(count_stmt)).scalar_one()
    rows = (
        await db.execute(
            stmt.order_by(Exhibition.start_date.asc().nullslast())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
    ).scalars().all()

    return ExhibitionPage(
        items=[ExhibitionOut.model_validate(r) for r in rows],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.post("/crawl", response_model=list[dict])
async def trigger_crawl() -> list[dict]:
    """Manually trigger a full crawl of all registered spiders."""
    try:
        return await run_all(ALL_SPIDERS)
    except Exception as e:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(e)) from e
