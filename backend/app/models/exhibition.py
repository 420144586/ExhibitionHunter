"""Exhibition ORM model."""
from datetime import datetime

from sqlalchemy import String, Text, DateTime, Index
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.core.database import Base


class Exhibition(Base):
    __tablename__ = "exhibitions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Source identity
    source_site: Mapped[str] = mapped_column(String(64), index=True)
    source_id: Mapped[str] = mapped_column(String(128), index=True)
    source_url: Mapped[str] = mapped_column(String(512))

    # Content
    title: Mapped[str] = mapped_column(String(256))
    city: Mapped[str | None] = mapped_column(String(64), nullable=True)
    venue: Mapped[str | None] = mapped_column(String(256), nullable=True)
    industry: Mapped[str | None] = mapped_column(String(128), nullable=True)
    start_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    end_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    cover_image: Mapped[str | None] = mapped_column(String(512), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    organizer: Mapped[str | None] = mapped_column(String(256), nullable=True)

    # Audit
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    __table_args__ = (
        # Dedup: one record per (source_site, source_id)
        Index("ux_exhibitions_source", "source_site", "source_id", unique=True),
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Exhibition {self.source_site}:{self.source_id} {self.title!r}>"
