import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.spec_change.models import SpecChangeRequest


class SpecChangeRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_filtered(
        self,
        status: str | None = None,
        offset: int = 0,
        limit: int = 20,
    ) -> tuple[list[SpecChangeRequest], int]:
        q = select(SpecChangeRequest)
        count_q = select(func.count(SpecChangeRequest.id))

        if status:
            q = q.where(SpecChangeRequest.status == status)
            count_q = count_q.where(SpecChangeRequest.status == status)

        total = (await self.session.execute(count_q)).scalar_one()
        q = q.order_by(SpecChangeRequest.created_at.desc()).offset(offset).limit(limit)
        result = await self.session.execute(q)
        return list(result.scalars().all()), total

    async def get_by_id(self, request_id: uuid.UUID) -> SpecChangeRequest | None:
        q = select(SpecChangeRequest).where(SpecChangeRequest.id == request_id)
        return (await self.session.execute(q)).scalar_one_or_none()

    async def update(self, request: SpecChangeRequest) -> SpecChangeRequest:
        await self.session.flush()
        await self.session.refresh(request)
        return request

    async def count_pending(self) -> int:
        q = select(func.count(SpecChangeRequest.id)).where(SpecChangeRequest.status == "pending")
        return (await self.session.execute(q)).scalar_one()

    async def create(self, request: SpecChangeRequest) -> SpecChangeRequest:
        self.session.add(request)
        await self.session.flush()
        await self.session.refresh(request)
        return request
