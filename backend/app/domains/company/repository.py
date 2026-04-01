import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domains.company.models import Company


class CompanyRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list(
        self, offset: int = 0, limit: int = 20, is_own_company: bool | None = None
    ) -> tuple[list[Company], int]:
        base = select(Company)
        count_q = select(func.count(Company.id))

        if is_own_company is not None:
            base = base.where(Company.is_own_company == is_own_company)
            count_q = count_q.where(Company.is_own_company == is_own_company)

        total = (await self.session.execute(count_q)).scalar_one()
        q = base.options(selectinload(Company.keywords)).order_by(Company.created_at.desc()).offset(offset).limit(limit)
        result = await self.session.execute(q)
        return list(result.scalars().all()), total

    async def get_own_company(self) -> Company | None:
        q = select(Company).options(selectinload(Company.keywords)).where(Company.is_own_company.is_(True))
        return (await self.session.execute(q)).scalar_one_or_none()

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
