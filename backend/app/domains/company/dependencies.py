from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.domains.company.repository import CompanyRepository
from app.domains.company.service import CompanyService


async def get_company_service(session: AsyncSession = Depends(get_db)) -> CompanyService:
    return CompanyService(CompanyRepository(session))
