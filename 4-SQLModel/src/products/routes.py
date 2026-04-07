from fastapi import APIRouter, status, Depends
from typing import List
from fastapi.exceptions import HTTPException
from .schemas import Product, ProductCreateModel, ProductUpdateModel  # Added ProductCreateModel
from src.DB.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.products.service import ProductService
import uuid

product_router = APIRouter()
product_service = ProductService()

@product_router.get('/intro')
async def intro():
    return {"message": "A FastApi Async CRUD for products "
            "with modular project structure using Routers "
            "And using SqlModel for pgsql integration"}

@product_router.get('/', response_model=List[Product])
async def get_all_products(session: AsyncSession = Depends(get_session)):
    products = await product_service.get_all_products(session)  # Added await
    return products

@product_router.post('/', status_code=status.HTTP_201_CREATED, response_model=Product)
async def create_products(product_data: ProductCreateModel, session: AsyncSession = Depends(get_session)):
    new_product = await product_service.create_product(product_data, session)
    return new_product

@product_router.get('/{product_uid}', response_model=Product)  # Added response_model
async def get_product(product_uid: str, session: AsyncSession = Depends(get_session)):  # Changed int to str
    product = await product_service.get_product(product_uid, session)
    if product:
        return product
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                          detail=f"Product Not Found OF ID:{product_uid}")

@product_router.patch('/{product_uid}', response_model=Product)
async def update_product(product_uid: str,  # Changed int to str
                        product_update_data: ProductUpdateModel, 
                        session: AsyncSession = Depends(get_session)):
    updated_product = await product_service.update_product(product_uid, product_update_data, session)
    if updated_product:
        return updated_product
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                          detail=f"Product Not Found OF ID:{product_uid}")

@product_router.delete('/{product_uid}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_uid: str, session: AsyncSession = Depends(get_session)):
    product_deleted = await product_service.delete_product(product_uid, session)
    if product_deleted is not None:
        return None
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                          detail=f"Product Not Found OF ID:{product_uid}")