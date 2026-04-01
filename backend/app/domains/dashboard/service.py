from app.domains.company.repository import CompanyRepository
from app.domains.dashboard.schemas import CompanyCard, DashboardSummaryResponse
from app.domains.news.repository import NewsRepository
from app.domains.news.schemas import NewsResponse
from app.domains.product.repository import ProductRepository
from app.domains.spec_change.repository import SpecChangeRepository


class DashboardService:
    def __init__(
        self,
        company_repo: CompanyRepository,
        news_repo: NewsRepository,
        spec_change_repo: SpecChangeRepository,
        product_repo: ProductRepository,
    ):
        self.company_repo = company_repo
        self.news_repo = news_repo
        self.spec_change_repo = spec_change_repo
        self.product_repo = product_repo

    async def get_summary(self) -> DashboardSummaryResponse:
        companies, _ = await self.company_repo.list(offset=0, limit=100)

        own_company_card: CompanyCard | None = None
        competitor_cards: list[CompanyCard] = []

        for c in companies:
            news_count = await self.news_repo.count_by_company(c.id)
            sentiment_dist = await self.news_repo.get_sentiment_distribution(c.id)
            products = await self.product_repo.list_by_company(c.id)

            card = CompanyCard(
                id=c.id,
                name=c.name,
                is_own_company=c.is_own_company,
                news_count=news_count,
                product_count=len(products),
                sentiment_distribution=sentiment_dist,
            )

            if c.is_own_company:
                own_company_card = card
            else:
                competitor_cards.append(card)

        recent_news = await self.news_repo.get_recent(limit=10)
        pending_count = await self.spec_change_repo.count_pending()

        return DashboardSummaryResponse(
            own_company=own_company_card,
            companies=competitor_cards,
            recent_news=[NewsResponse.model_validate(n) for n in recent_news],
            pending_spec_changes_count=pending_count,
        )
