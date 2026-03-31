import uuid
from datetime import date

from sqlalchemy import Boolean, Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.models import Base, TimestampMixin, UUIDMixin


class Company(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "companies"

    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    founded_at: Mapped[date | None] = mapped_column(Date, nullable=True)
    employee_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    revenue: Mapped[str | None] = mapped_column(String(50), nullable=True)
    website_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_own_company: Mapped[bool] = mapped_column(Boolean, default=False)

    keywords: Mapped[list["SearchKeyword"]] = relationship(
        back_populates="company",
        cascade="all, delete-orphan",
    )


class SearchKeyword(Base, UUIDMixin):
    __tablename__ = "search_keywords"

    company_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("companies.id"), nullable=False)
    keyword: Mapped[str] = mapped_column(String(100), nullable=False)

    company: Mapped["Company"] = relationship(back_populates="keywords")
