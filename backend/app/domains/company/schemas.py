import uuid
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class CompanyCreate(BaseModel):
    name: str
    founded_at: date | None = None
    employee_count: int | None = None
    revenue: str | None = None
    website_url: str | None = None
    description: str | None = None
    is_own_company: bool = False
    search_keywords: list[str] = []


class CompanyUpdate(BaseModel):
    name: str | None = None
    founded_at: date | None = None
    employee_count: int | None = None
    revenue: str | None = None
    website_url: str | None = None
    description: str | None = None
    is_own_company: bool | None = None
    search_keywords: list[str] | None = None


class CompanyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    founded_at: date | None = None
    employee_count: int | None = None
    revenue: str | None = None
    website_url: str | None = None
    description: str | None = None
    is_own_company: bool
    search_keywords: list[str] = []
    created_at: datetime
    updated_at: datetime
