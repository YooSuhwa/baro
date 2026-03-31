import uuid

from fastapi import APIRouter, Depends

from app.domains.spec_field.dependencies import get_spec_field_service
from app.domains.spec_field.schemas import SpecFieldCreate, SpecFieldResponse, SpecFieldUpdate
from app.domains.spec_field.service import SpecFieldService

router = APIRouter(prefix="/spec-fields", tags=["spec-fields"])


@router.get("", response_model=list[SpecFieldResponse])
async def list_spec_fields(service: SpecFieldService = Depends(get_spec_field_service)):
    return await service.list_all()


@router.post("", response_model=SpecFieldResponse, status_code=201)
async def create_spec_field(data: SpecFieldCreate, service: SpecFieldService = Depends(get_spec_field_service)):
    return await service.create(data)


@router.put("/{field_id}", response_model=SpecFieldResponse)
async def update_spec_field(
    field_id: uuid.UUID,
    data: SpecFieldUpdate,
    service: SpecFieldService = Depends(get_spec_field_service),
):
    return await service.update(field_id, data)


@router.delete("/{field_id}", status_code=204)
async def delete_spec_field(field_id: uuid.UUID, service: SpecFieldService = Depends(get_spec_field_service)):
    await service.delete(field_id)
