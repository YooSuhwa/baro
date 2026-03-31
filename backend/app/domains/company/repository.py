import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domains.company.models import Company


class CompanyRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list(self, offset: int = 0, limit: int = 20) -> tuple[list[Company], int]:
        total = (await self.session.execute(select(func.count(Company.id)))).scalar_one()
        q = (
            select(Company)
            .options(selectinload(Company.keywords))
            .order_by(Company.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        result = await self.session.execute(q)
        return list(result.scalars().all()), total

    async def get_by_id(self, company_id: uuid.UUID) -> Company | None:
        q = select(Company).options(selectinload(Company.keywords)).where(Company.id == company_id)
        return (await self.session.execute(q)).scalar_one_or_none()

    async def get_by_name(self, name: str) -> Company | None:
        return (await self.session.execute(select(Company).where(Company.name == name))).scalar_one_or_none()

    async def create(self, company: Company) -> Company:
        self.session.add(company)
        await self.session.flush()
        await self.session.refresh(company, attribute_names=["keywords"])
        return company

    async def update(self, company: Company) -> Company:
        await self.session.flush()
        await self.session.refresh(company)
        return company

    async def delete(self, company: Company) -> None:
        await self.session.delete(company)
        await self.session.flush()
