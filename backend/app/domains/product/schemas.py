import uuid
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class SpecValueItem(BaseModel):
    spec_field_id: uuid.UUID
    value: str | None = None


class SpecValueResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    spec_field_id: uuid.UUID
    value: str | None = None


class ProductCreate(BaseModel):
    company_id: uuid.UUID
    name: str
    released_at: date | None = None
    concept: str | None = None
    definition: str | None = None


class ProductUpdate(BaseModel):
    name: str | None = None
    released_at: date | None = None
    concept: str | None = None
    definition: str | None = None


class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    company_id: uuid.UUID
    name: str
    released_at: date | None = None
    concept: str | None = None
    definition: str | None = None
    spec_values: list[SpecValueResponse] = []
    created_at: datetime
    updated_at: datetime


class BulkSpecUpdate(BaseModel):
    specs: list[SpecValueItem]


# --- Compare schemas (PRD section 6.2) ---


class CompareProductInfo(BaseModel):
    id: uuid.UUID
    name: str
    company: str


class CompareFieldValues(BaseModel):
    field_id: uuid.UUID
    field_name: str
    values: dict[str, str | None]  # product_id -> value


class CompareCategory(BaseModel):
    name: str
    fields: list[CompareFieldValues]


class CompareResponse(BaseModel):
    products: list[CompareProductInfo]
    categories: list[CompareCategory]
