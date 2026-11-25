"""Pydantic schemas for Exhibition."""
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class ExhibitionBase(BaseModel):
    title: str
    city: str | None = None
    venue: str | None = None
    industry: str | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    cover_image: str | None = None
    description: str | None = None
    organizer: str | None = None


class ExhibitionCreate(ExhibitionBase):
    source_site: str
    source_id: str
    source_url: str


class ExhibitionOut(ExhibitionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    source_site: str
    source_id: str
    source_url: str
    created_at: datetime
    updated_at: datetime


class ExhibitionPage(BaseModel):
    """Paginated list response."""
    items: list[ExhibitionOut]
    total: int
    page: int
    page_size: int
