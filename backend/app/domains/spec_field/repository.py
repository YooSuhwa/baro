import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.spec_field.models import SpecField


class SpecFieldRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_all(self) -> list[SpecField]:
        q = select(SpecField).order_by(SpecField.category, SpecField.sort_order)
        result = await self.session.execute(q)
        return list(result.scalars().all())

    async def get_by_id(self, field_id: uuid.UUID) -> SpecField | None:
        return (await self.session.execute(select(SpecField).where(SpecField.id == field_id))).scalar_one_or_none()

    async def create(self, field: SpecField) -> SpecField:
        self.session.add(field)
        await self.session.flush()
        await self.session.refresh(field)
        return field

    async def update(self, field: SpecField) -> SpecField:
        await self.session.flush()
        await self.session.refresh(field)
        return field

    async def delete(self, field: SpecField) -> None:
        await self.session.delete(field)
        await self.session.flush()
