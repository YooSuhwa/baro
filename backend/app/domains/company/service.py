import uuid

from app.core.exceptions import DuplicateError, NotFoundError
from app.domains.company.models import Company, SearchKeyword
from app.domains.company.repository import CompanyRepository
from app.domains.company.schemas import CompanyCreate, CompanyResponse, CompanyUpdate


class CompanyService:
    def __init__(self, repo: CompanyRepository):
        self.repo = repo

    async def list(self, offset: int = 0, limit: int = 20) -> tuple[list[CompanyResponse], int]:
        companies, total = await self.repo.list(offset, limit)
        return [self._to_response(c) for c in companies], total

    async def get(self, company_id: uuid.UUID) -> CompanyResponse:
        company = await self.repo.get_by_id(company_id)
        if not company:
            raise NotFoundError("회사", str(company_id))
        return self._to_response(company)

    async def create(self, data: CompanyCreate) -> CompanyResponse:
        existing = await self.repo.get_by_name(data.name)
        if existing:
            raise DuplicateError("company", "name", str(existing.id))

        company = Company(
            name=data.name,
            founded_at=data.founded_at,
            employee_count=data.employee_count,
            revenue=data.revenue,
            website_url=data.website_url,
            description=data.description,
            is_own_company=data.is_own_company,
        )
        company.keywords = [SearchKeyword(keyword=kw) for kw in data.search_keywords]
        return self._to_response(await self.repo.create(company))

    async def update(self, company_id: uuid.UUID, data: CompanyUpdate) -> CompanyResponse:
        company = await self.repo.get_by_id(company_id)
        if not company:
            raise NotFoundError("회사", str(company_id))

        update_fields = data.model_fields_set
        if "name" in update_fields and data.name != company.name:
            existing = await self.repo.get_by_name(data.name)
            if existing:
                raise DuplicateError("company", "name", str(existing.id))

        for field in update_fields - {"search_keywords"}:
            setattr(company, field, getattr(data, field))

        if "search_keywords" in update_fields:
            company.keywords = [SearchKeyword(keyword=kw) for kw in (data.search_keywords or [])]

        return self._to_response(await self.repo.update(company))

    async def delete(self, company_id: uuid.UUID) -> None:
        company = await self.repo.get_by_id(company_id)
        if not company:
            raise NotFoundError("회사", str(company_id))
        await self.repo.delete(company)

    def _to_response(self, company: Company) -> CompanyResponse:
        return CompanyResponse(
            id=company.id,
            name=company.name,
            founded_at=company.founded_at,
            employee_count=company.employee_count,
            revenue=company.revenue,
            website_url=company.website_url,
            description=company.description,
            is_own_company=company.is_own_company,
            search_keywords=[kw.keyword for kw in company.keywords],
            created_at=company.created_at,
            updated_at=company.updated_at,
        )
