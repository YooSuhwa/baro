import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domains.product.models import Product, SpecValue


class ProductRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_by_company(self, company_id: uuid.UUID) -> list[Product]:
        q = (
            select(Product)
            .options(selectinload(Product.spec_values))
            .where(Product.company_id == company_id)
            .order_by(Product.created_at.desc())
        )
        result = await self.session.execute(q)
        return list(result.scalars().all())

    async def get_by_id(self, product_id: uuid.UUID) -> Product | None:
        q = select(Product).options(selectinload(Product.spec_values)).where(Product.id == product_id)
        return (await self.session.execute(q)).scalar_one_or_none()

    async def create(self, product: Product) -> Product:
        self.session.add(product)
        await self.session.flush()
        # re-fetch with eager loading to avoid lazy loading issues
        return await self.get_by_id(product.id)  # type: ignore[return-value]

    async def update(self, product: Product) -> Product:
        await self.session.flush()
        return await self.get_by_id(product.id)  # type: ignore[return-value]

    async def delete(self, product: Product) -> None:
        await self.session.delete(product)
        await self.session.flush()

    async def get_spec_value(self, product_id: uuid.UUID, spec_field_id: uuid.UUID) -> SpecValue | None:
        q = select(SpecValue).where(
            SpecValue.product_id == product_id,
            SpecValue.spec_field_id == spec_field_id,
        )
        return (await self.session.execute(q)).scalar_one_or_none()

    async def upsert_spec_value(self, product_id: uuid.UUID, spec_field_id: uuid.UUID, value: str | None) -> None:
        existing = await self.get_spec_value(product_id, spec_field_id)
        if existing:
            existing.value = value
        else:
            sv = SpecValue(product_id=product_id, spec_field_id=spec_field_id, value=value)
            self.session.add(sv)
        await self.session.flush()

    async def get_products_by_ids(self, product_ids: list[uuid.UUID]) -> list[Product]:
        q = select(Product).options(selectinload(Product.spec_values)).where(Product.id.in_(product_ids))
        result = await self.session.execute(q)
        return list(result.scalars().all())
