import uuid

from fastapi import APIRouter, Depends, Query

from app.core.schemas import PaginatedResponse
from app.domains.company.dependencies import get_company_service
from app.domains.company.schemas import CompanyCreate, CompanyResponse, CompanyUpdate
from app.domains.company.service import CompanyService

router = APIRouter(prefix="/companies", tags=["companies"])


@router.get("", response_model=PaginatedResponse[CompanyResponse])
async def list_companies(
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    service: CompanyService = Depends(get_company_service),
):
    items, total = await service.list(offset, limit)
    return PaginatedResponse(items=items, total=total, offset=offset, limit=limit)


@router.post("", response_model=CompanyResponse, status_code=201)
async def create_company(
    data: CompanyCreate,
    service: CompanyService = Depends(get_company_service),
):
    return await service.create(data)


@router.get("/{company_id}", response_model=CompanyResponse)
async def get_company(
    company_id: uuid.UUID,
    service: CompanyService = Depends(get_company_service),
):
    return await service.get(company_id)


@router.put("/{company_id}", response_model=CompanyResponse)
async def update_company(
    company_id: uuid.UUID,
    data: CompanyUpdate,
    service: CompanyService = Depends(get_company_service),
):
    return await service.update(company_id, data)


@router.delete("/{company_id}", status_code=204)
async def delete_company(
    company_id: uuid.UUID,
    service: CompanyService = Depends(get_company_service),
):
    await service.delete(company_id)
