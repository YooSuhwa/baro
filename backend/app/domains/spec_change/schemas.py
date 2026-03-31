import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SpecChangeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    product_id: uuid.UUID
    spec_field_id: uuid.UUID
    old_value: str | None = None
    new_value: str
    source_url: str
    source_article_id: uuid.UUID | None = None
    status: str
    reject_reason: str | None = None
    created_at: datetime
    reviewed_at: datetime | None = None


class RejectRequest(BaseModel):
    reason: str
