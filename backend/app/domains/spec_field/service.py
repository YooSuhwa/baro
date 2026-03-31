import uuid

from app.core.exceptions import NotFoundError
from app.domains.spec_field.models import SpecField
from app.domains.spec_field.repository import SpecFieldRepository
from app.domains.spec_field.schemas import SpecFieldCreate, SpecFieldResponse, SpecFieldUpdate


class SpecFieldService:
    def __init__(self, repo: SpecFieldRepository):
        self.repo = repo

    async def list_all(self) -> list[SpecFieldResponse]:
        fields = await self.repo.list_all()
        return [SpecFieldResponse.model_validate(f) for f in fields]

    async def create(self, data: SpecFieldCreate) -> SpecFieldResponse:
        field = SpecField(
            category=data.category,
            field_name=data.field_name,
            field_type=data.field_type,
            is_template=data.is_template,
            sort_order=data.sort_order,
        )
        field = await self.repo.create(field)
        return SpecFieldResponse.model_validate(field)

    async def update(self, field_id: uuid.UUID, data: SpecFieldUpdate) -> SpecFieldResponse:
        field = await self.repo.get_by_id(field_id)
        if not field:
            raise NotFoundError("비교항목", str(field_id))

        for attr in data.model_fields_set:
            setattr(field, attr, getattr(data, attr))

        field = await self.repo.update(field)
        return SpecFieldResponse.model_validate(field)

    async def delete(self, field_id: uuid.UUID) -> None:
        field = await self.repo.get_by_id(field_id)
        if not field:
            raise NotFoundError("비교항목", str(field_id))
        await self.repo.delete(field)
