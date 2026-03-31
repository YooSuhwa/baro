import uuid
from datetime import datetime

from sqlalchemy import JSON, DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.models import Base, UUIDMixin


class NewsArticle(Base, UUIDMixin):
    __tablename__ = "news_articles"

    company_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("companies.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    content: Mapped[str | None] = mapped_column(Text, nullable=True)
    url: Mapped[str] = mapped_column(String(1000), unique=True, nullable=False)
    source: Mapped[str] = mapped_column(String(50), nullable=False)  # naver / google / blog
    sentiment: Mapped[str] = mapped_column(String(10), default="unknown")  # positive/negative/neutral/unknown
    summary: Mapped[str | None] = mapped_column(String(200), nullable=True)
    tags: Mapped[list | None] = mapped_column(JSON, nullable=True)  # AI-generated keyword tags
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    collected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    company: Mapped["Company"] = relationship(back_populates="news_articles")  # type: ignore[name-defined]  # noqa: F821
