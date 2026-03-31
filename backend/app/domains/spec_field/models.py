from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.models import Base, UUIDMixin


class SpecField(Base, UUIDMixin):
    __tablename__ = "spec_fields"

    category: Mapped[str] = mapped_column(String(50), nullable=False)  # company_info / product_info / tech_spec
    field_name: Mapped[str] = mapped_column(String(100), nullable=False)
    field_type: Mapped[str] = mapped_column(String(20), nullable=False)  # text / number / date / url
    is_template: Mapped[bool] = mapped_column(Boolean, default=False)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
