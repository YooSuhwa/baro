import uuid
from datetime import date

from sqlalchemy import Date, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.models import Base, TimestampMixin, UUIDMixin


class Product(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "products"

    company_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("companies.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    released_at: Mapped[date | None] = mapped_column(Date, nullable=True)
    concept: Mapped[str | None] = mapped_column(Text, nullable=True)
    definition: Mapped[str | None] = mapped_column(Text, nullable=True)

    company: Mapped["Company"] = relationship(back_populates="products")  # type: ignore[name-defined]  # noqa: F821
    spec_values: Mapped[list["SpecValue"]] = relationship(
        back_populates="product",
        cascade="all, delete-orphan",
    )


class SpecValue(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "spec_values"
    __table_args__ = (UniqueConstraint("product_id", "spec_field_id", name="uq_product_spec"),)

    product_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("products.id"), nullable=False)
    spec_field_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("spec_fields.id"), nullable=False)
    value: Mapped[str | None] = mapped_column(Text, nullable=True)

    product: Mapped["Product"] = relationship(back_populates="spec_values")
