import uuid

from fastapi import APIRouter, Depends, Query

from app.core.schemas import PaginatedResponse
from app.domains.spec_change.dependencies import get_spec_change_service
from app.domains.spec_change.schemas import RejectRequest, SpecChangeResponse
from app.domains.spec_change.service import SpecChangeService

router = APIRouter(prefix="/spec-changes", tags=["spec-changes"])


@router.get("", response_model=PaginatedResponse[SpecChangeResponse])
async def list_spec_changes(
    status: str | None = Query(None),
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    service: SpecChangeService = Depends(get_spec_change_service),
):
    return await service.list_filtered(status, offset, limit)


@router.put("/{request_id}/approve", response_model=SpecChangeResponse)
async def approve_spec_change(
    request_id: uuid.UUID,
    service: SpecChangeService = Depends(get_spec_change_service),
):
    return await service.approve(request_id)


@router.put("/{request_id}/reject", response_model=SpecChangeResponse)
async def reject_spec_change(
    request_id: uuid.UUID,
    data: RejectRequest,
    service: SpecChangeService = Depends(get_spec_change_service),
):
    return await service.reject(request_id, data)
