import uuid

from pydantic import BaseModel

from app.domains.news.schemas import NewsResponse


class CompanyCard(BaseModel):
    id: uuid.UUID
    name: str
    news_count: int
    product_count: int
    sentiment_distribution: dict[str, int]


class DashboardSummaryResponse(BaseModel):
    companies: list[CompanyCard]
    recent_news: list[NewsResponse]
    pending_spec_changes_count: int
