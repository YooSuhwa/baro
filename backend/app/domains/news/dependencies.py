from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.domains.company.repository import CompanyRepository
from app.domains.news.repository import NewsRepository
from app.domains.news.service import NewsService


async def get_news_service(session: AsyncSession = Depends(get_db)) -> NewsService:
    return NewsService(NewsRepository(session), CompanyRepository(session))
