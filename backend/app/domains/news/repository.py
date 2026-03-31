import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.news.models import NewsArticle


class NewsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_filtered(
        self,
        company_id: uuid.UUID | None = None,
        sentiment: str | None = None,
        period: str | None = None,
        offset: int = 0,
        limit: int = 20,
    ) -> tuple[list[NewsArticle], int]:
        q = select(NewsArticle)
        count_q = select(func.count(NewsArticle.id))

        if company_id:
            q = q.where(NewsArticle.company_id == company_id)
            count_q = count_q.where(NewsArticle.company_id == company_id)
        if sentiment:
            q = q.where(NewsArticle.sentiment == sentiment)
            count_q = count_q.where(NewsArticle.sentiment == sentiment)
        if period:
            cutoff = self._period_to_cutoff(period)
            if cutoff:
                q = q.where(NewsArticle.collected_at >= cutoff)
                count_q = count_q.where(NewsArticle.collected_at >= cutoff)

        total = (await self.session.execute(count_q)).scalar_one()
        q = q.order_by(NewsArticle.collected_at.desc()).offset(offset).limit(limit)
        result = await self.session.execute(q)
        return list(result.scalars().all()), total

    async def get_by_company(
        self,
        company_id: uuid.UUID,
        period: str | None = None,
        limit: int = 20,
    ) -> list[NewsArticle]:
        q = select(NewsArticle).where(NewsArticle.company_id == company_id)
        if period:
            cutoff = self._period_to_cutoff(period)
            if cutoff:
                q = q.where(NewsArticle.collected_at >= cutoff)
        q = q.order_by(NewsArticle.collected_at.desc()).limit(limit)
        result = await self.session.execute(q)
        return list(result.scalars().all())

    async def get_sentiment_distribution(self, company_id: uuid.UUID, period: str | None = None) -> dict[str, int]:
        q = select(NewsArticle.sentiment, func.count(NewsArticle.id)).where(NewsArticle.company_id == company_id)
        if period:
            cutoff = self._period_to_cutoff(period)
            if cutoff:
                q = q.where(NewsArticle.collected_at >= cutoff)
        q = q.group_by(NewsArticle.sentiment)
        result = await self.session.execute(q)
        return {row[0]: row[1] for row in result.all()}

    async def exists_by_url(self, url: str) -> bool:
        q = select(func.count(NewsArticle.id)).where(NewsArticle.url == url)
        return (await self.session.execute(q)).scalar_one() > 0

    async def bulk_create(self, articles: list[NewsArticle]) -> list[NewsArticle]:
        self.session.add_all(articles)
        await self.session.flush()
        return articles

    async def get_recent(self, limit: int = 10) -> list[NewsArticle]:
        q = select(NewsArticle).order_by(NewsArticle.collected_at.desc()).limit(limit)
        result = await self.session.execute(q)
        return list(result.scalars().all())

    async def count_by_company(self, company_id: uuid.UUID) -> int:
        q = select(func.count(NewsArticle.id)).where(NewsArticle.company_id == company_id)
        return (await self.session.execute(q)).scalar_one()

    def _period_to_cutoff(self, period: str) -> datetime | None:
        now = datetime.now(timezone.utc)
        match period:
            case "1w":
                return now - timedelta(weeks=1)
            case "1m":
                return now - timedelta(days=30)
            case "3m":
                return now - timedelta(days=90)
            case _:
                return None
