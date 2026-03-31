from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.domains.company.repository import CompanyRepository
from app.domains.dashboard.service import DashboardService
from app.domains.news.repository import NewsRepository
from app.domains.product.repository import ProductRepository
from app.domains.spec_change.repository import SpecChangeRepository


async def get_dashboard_service(session: AsyncSession = Depends(get_db)) -> DashboardService:
    return DashboardService(
        CompanyRepository(session),
        NewsRepository(session),
        SpecChangeRepository(session),
        ProductRepository(session),
    )
