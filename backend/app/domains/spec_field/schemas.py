import uuid

from pydantic import BaseModel, ConfigDict


class SpecFieldCreate(BaseModel):
    category: str  # company_info / product_info / tech_spec
    field_name: str
    field_type: str  # text / number / date / url
    is_template: bool = False
    sort_order: int = 0


class SpecFieldUpdate(BaseModel):
    category: str | None = None
    field_name: str | None = None
    field_type: str | None = None
    is_template: bool | None = None
    sort_order: int | None = None


class SpecFieldResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    category: str
    field_name: str
    field_type: str
    is_template: bool
    sort_order: int
