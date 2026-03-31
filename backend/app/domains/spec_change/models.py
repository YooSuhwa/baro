import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.models import Base, UUIDMixin


class SpecChangeRequest(Base, UUIDMixin):
    __tablename__ = "spec_change_requests"

    product_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("products.id"), nullable=False)
    spec_field_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("spec_fields.id"), nullable=False)
    old_value: Mapped[str | None] = mapped_column(Text, nullable=True)
    new_value: Mapped[str] = mapped_column(Text, nullable=False)
    source_url: Mapped[str] = mapped_column(String(1000), nullable=False)
    source_article_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("news_articles.id"), nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="pending")  # pending / approved / rejected
    reject_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
