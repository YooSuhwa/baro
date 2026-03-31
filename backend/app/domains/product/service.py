import uuid

from app.core.exceptions import NotFoundError
from app.domains.company.repository import CompanyRepository
from app.domains.product.models import Product
from app.domains.product.repository import ProductRepository
from app.domains.product.schemas import (
    BulkSpecUpdate,
    ProductCreate,
    ProductResponse,
    ProductUpdate,
)


class ProductService:
    def __init__(self, repo: ProductRepository, company_repo: CompanyRepository):
        self.repo = repo
        self.company_repo = company_repo

    async def list_by_company(self, company_id: uuid.UUID) -> list[ProductResponse]:
        products = await self.repo.list_by_company(company_id)
        return [self._to_response(p) for p in products]

    async def get(self, product_id: uuid.UUID) -> ProductResponse:
        product = await self.repo.get_by_id(product_id)
        if not product:
            raise NotFoundError("제품", str(product_id))
        return self._to_response(product)

    async def create(self, data: ProductCreate) -> ProductResponse:
        company = await self.company_repo.get_by_id(data.company_id)
        if not company:
            raise NotFoundError("회사", str(data.company_id))

        product = Product(
            company_id=data.company_id,
            name=data.name,
            released_at=data.released_at,
            concept=data.concept,
            definition=data.definition,
        )
        product = await self.repo.create(product)
        return self._to_response(product)

    async def update(self, product_id: uuid.UUID, data: ProductUpdate) -> ProductResponse:
        product = await self.repo.get_by_id(product_id)
        if not product:
            raise NotFoundError("제품", str(product_id))

        for field in data.model_fields_set:
            setattr(product, field, getattr(data, field))

        product = await self.repo.update(product)
        return self._to_response(product)

    async def delete(self, product_id: uuid.UUID) -> None:
        product = await self.repo.get_by_id(product_id)
        if not product:
            raise NotFoundError("제품", str(product_id))
        await self.repo.delete(product)

    async def bulk_update_specs(self, product_id: uuid.UUID, data: BulkSpecUpdate) -> ProductResponse:
        product = await self.repo.get_by_id(product_id)
        if not product:
            raise NotFoundError("제품", str(product_id))

        for spec in data.specs:
            await self.repo.upsert_spec_value(product_id, spec.spec_field_id, spec.value)

        # re-fetch with updated specs
        product = await self.repo.get_by_id(product_id)
        return self._to_response(product)

    def _to_response(self, product: Product) -> ProductResponse:
        return ProductResponse.model_validate(product)
