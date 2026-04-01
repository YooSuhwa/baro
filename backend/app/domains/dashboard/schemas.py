import uuid

from pydantic import BaseModel

from app.domains.news.schemas import NewsResponse


class CompanyCard(BaseModel):
    id: uuid.UUID
    name: str
    is_own_company: bool
    news_count: int
    product_count: int
    sentiment_distribution: dict[str, int]


class DashboardSummaryResponse(BaseModel):
    own_company: CompanyCard | None
    companies: list[CompanyCard]  # competitors only
    recent_news: list[NewsResponse]
    pending_spec_changes_count: int
