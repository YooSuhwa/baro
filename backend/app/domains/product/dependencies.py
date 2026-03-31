from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.domains.company.repository import CompanyRepository
from app.domains.product.repository import ProductRepository
from app.domains.product.service import ProductService


async def get_product_service(session: AsyncSession = Depends(get_db)) -> ProductService:
    return ProductService(ProductRepository(session), CompanyRepository(session))
