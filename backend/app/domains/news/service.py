import uuid

from app.core.schemas import PaginatedResponse
from app.domains.company.repository import CompanyRepository
from app.domains.news.repository import NewsRepository
from app.domains.news.schemas import (
    CollectResponse,
    CompanyNewsComparison,
    NewsCompareResponse,
    NewsResponse,
)


class NewsService:
    def __init__(self, repo: NewsRepository, company_repo: CompanyRepository):
        self.repo = repo
        self.company_repo = company_repo

    async def list_filtered(
        self,
        company_id: uuid.UUID | None = None,
        sentiment: str | None = None,
        period: str | None = None,
        offset: int = 0,
        limit: int = 20,
    ) -> PaginatedResponse[NewsResponse]:
        articles, total = await self.repo.list_filtered(company_id, sentiment, period, offset, limit)
        items = [NewsResponse.model_validate(a) for a in articles]
        return PaginatedResponse(items=items, total=total, offset=offset, limit=limit)

    async def compare(self, company_ids: list[uuid.UUID], period: str = "1w") -> NewsCompareResponse:
        comparisons = []
        for cid in company_ids:
            company = await self.company_repo.get_by_id(cid)
            company_name = company.name if company else ""

            articles = await self.repo.get_by_company(cid, period=period, limit=20)
            sentiment_dist = await self.repo.get_sentiment_distribution(cid, period=period)

            comparisons.append(
                CompanyNewsComparison(
                    company_id=cid,
                    company_name=company_name,
                    sentiment_distribution=sentiment_dist,
                    total_count=sum(sentiment_dist.values()),
                    articles=[NewsResponse.model_validate(a) for a in articles],
                )
            )

        return NewsCompareResponse(companies=comparisons, period=period)

    async def trigger_collect(self, company_id: uuid.UUID | None = None) -> CollectResponse:
        # In MVP, this triggers a BackgroundTask (handled in router)
        # Here we just return the response
        return CollectResponse(
            message="수집이 시작되었습니다",
            company_id=company_id,
        )
