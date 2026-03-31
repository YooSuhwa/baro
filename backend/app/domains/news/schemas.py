import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class NewsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    company_id: uuid.UUID
    title: str
    content: str | None = None
    url: str
    source: str
    sentiment: str
    summary: str | None = None
    tags: list[str] | None = None
    published_at: datetime | None = None
    collected_at: datetime


class NewsFilter(BaseModel):
    company_id: uuid.UUID | None = None
    sentiment: str | None = None
    period: str | None = None  # 1w / 1m / 3m


class CompanyNewsComparison(BaseModel):
    company_id: uuid.UUID
    company_name: str
    sentiment_distribution: dict[str, int]  # {"positive": 60, "negative": 15, "neutral": 25}
    total_count: int
    articles: list[NewsResponse]


class NewsCompareResponse(BaseModel):
    companies: list[CompanyNewsComparison]
    period: str


class CollectRequest(BaseModel):
    company_id: uuid.UUID | None = None  # None = collect all


class CollectResponse(BaseModel):
    message: str
    company_id: uuid.UUID | None = None
