import uuid
from collections import defaultdict

from app.core.exceptions import NotFoundError, ValidationError
from app.domains.company.repository import CompanyRepository
from app.domains.product.models import Product
from app.domains.product.repository import ProductRepository
from app.domains.product.schemas import (
    BulkSpecUpdate,
    CompareCategory,
    CompareFieldValues,
    CompareProductInfo,
    CompareResponse,
    ProductCreate,
    ProductResponse,
    ProductUpdate,
)
from app.domains.spec_field.repository import SpecFieldRepository


class ProductService:
    def __init__(
        self,
        repo: ProductRepository,
        company_repo: CompanyRepository,
        spec_field_repo: SpecFieldRepository | None = None,
    ):
        self.repo = repo
        self.company_repo = company_repo
        self.spec_field_repo = spec_field_repo

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

    async def compare(self, product_ids: list[uuid.UUID]) -> CompareResponse:
        if len(product_ids) < 2:
            raise ValidationError("비교하려면 2개 이상 선택하세요")
        if len(product_ids) > 6:
            raise ValidationError("최대 6개까지 비교 가능합니다")

        products = await self.repo.get_products_by_ids(product_ids)
        if not products:
            raise NotFoundError("제품", str(product_ids))

        # build product info with company names
        company_ids = {p.company_id for p in products}
        companies = {}
        for cid in company_ids:
            c = await self.company_repo.get_by_id(cid)
            if c:
                companies[cid] = c.name

        product_infos = [
            CompareProductInfo(id=p.id, name=p.name, company=companies.get(p.company_id, "")) for p in products
        ]

        # get all spec fields
        spec_fields = await self.spec_field_repo.list_all() if self.spec_field_repo else []

        # build spec value lookup: (product_id, spec_field_id) -> value
        value_map: dict[tuple[uuid.UUID, uuid.UUID], str | None] = {}
        for p in products:
            for sv in p.spec_values:
                value_map[(p.id, sv.spec_field_id)] = sv.value

        # group fields by category
        categories_map: dict[str, list[CompareFieldValues]] = defaultdict(list)

        for sf in spec_fields:
            values = {}
            for p in products:
                values[str(p.id)] = value_map.get((p.id, sf.id))
            categories_map[sf.category].append(
                CompareFieldValues(field_id=sf.id, field_name=sf.field_name, values=values)
            )

        categories = [CompareCategory(name=cat, fields=fields) for cat, fields in categories_map.items()]

        return CompareResponse(products=product_infos, categories=categories)

    def _to_response(self, product: Product) -> ProductResponse:
        return ProductResponse.model_validate(product)
