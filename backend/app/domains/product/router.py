import uuid

from fastapi import APIRouter, Depends

from app.domains.product.dependencies import get_product_service
from app.domains.product.schemas import BulkSpecUpdate, ProductCreate, ProductResponse, ProductUpdate
from app.domains.product.service import ProductService

router = APIRouter(tags=["products"])


@router.post("/products", response_model=ProductResponse, status_code=201)
async def create_product(data: ProductCreate, service: ProductService = Depends(get_product_service)):
    return await service.create(data)


@router.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: uuid.UUID, service: ProductService = Depends(get_product_service)):
    return await service.get(product_id)


@router.put("/products/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: uuid.UUID,
    data: ProductUpdate,
    service: ProductService = Depends(get_product_service),
):
    return await service.update(product_id, data)


@router.delete("/products/{product_id}", status_code=204)
async def delete_product(product_id: uuid.UUID, service: ProductService = Depends(get_product_service)):
    await service.delete(product_id)


@router.get("/companies/{company_id}/products", response_model=list[ProductResponse])
async def list_company_products(company_id: uuid.UUID, service: ProductService = Depends(get_product_service)):
    return await service.list_by_company(company_id)


@router.put("/products/{product_id}/specs", response_model=ProductResponse)
async def bulk_update_specs(
    product_id: uuid.UUID,
    data: BulkSpecUpdate,
    service: ProductService = Depends(get_product_service),
):
    return await service.bulk_update_specs(product_id, data)
