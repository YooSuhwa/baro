from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.domains.product.repository import ProductRepository
from app.domains.spec_change.repository import SpecChangeRepository
from app.domains.spec_change.service import SpecChangeService


async def get_spec_change_service(session: AsyncSession = Depends(get_db)) -> SpecChangeService:
    return SpecChangeService(SpecChangeRepository(session), ProductRepository(session))
