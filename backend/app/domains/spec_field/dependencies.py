from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.domains.spec_field.repository import SpecFieldRepository
from app.domains.spec_field.service import SpecFieldService


async def get_spec_field_service(session: AsyncSession = Depends(get_db)) -> SpecFieldService:
    return SpecFieldService(SpecFieldRepository(session))
