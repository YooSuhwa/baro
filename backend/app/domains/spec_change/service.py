import uuid
from datetime import datetime, timezone

from app.core.exceptions import NotFoundError, ValidationError
from app.core.schemas import PaginatedResponse
from app.domains.product.repository import ProductRepository
from app.domains.spec_change.repository import SpecChangeRepository
from app.domains.spec_change.schemas import RejectRequest, SpecChangeResponse


class SpecChangeService:
    def __init__(self, repo: SpecChangeRepository, product_repo: ProductRepository):
        self.repo = repo
        self.product_repo = product_repo

    async def list_filtered(
        self,
        status: str | None = None,
        offset: int = 0,
        limit: int = 20,
    ) -> PaginatedResponse[SpecChangeResponse]:
        items, total = await self.repo.list_filtered(status, offset, limit)
        return PaginatedResponse(
            items=[SpecChangeResponse.model_validate(i) for i in items],
            total=total,
            offset=offset,
            limit=limit,
        )

    async def approve(self, request_id: uuid.UUID) -> SpecChangeResponse:
        request = await self.repo.get_by_id(request_id)
        if not request:
            raise NotFoundError("스펙변경요청", str(request_id))
        if request.status != "pending":
            raise ValidationError(f"현재 상태({request.status})에서는 승인할 수 없습니다")

        # Update spec value atomically
        await self.product_repo.upsert_spec_value(request.product_id, request.spec_field_id, request.new_value)

        request.status = "approved"
        request.reviewed_at = datetime.now(timezone.utc)
        request = await self.repo.update(request)
        return SpecChangeResponse.model_validate(request)

    async def reject(self, request_id: uuid.UUID, data: RejectRequest) -> SpecChangeResponse:
        request = await self.repo.get_by_id(request_id)
        if not request:
            raise NotFoundError("스펙변경요청", str(request_id))
        if request.status != "pending":
            raise ValidationError(f"현재 상태({request.status})에서는 거절할 수 없습니다")

        request.status = "rejected"
        request.reject_reason = data.reason
        request.reviewed_at = datetime.now(timezone.utc)
        request = await self.repo.update(request)
        return SpecChangeResponse.model_validate(request)
