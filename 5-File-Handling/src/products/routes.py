from fastapi import APIRouter, status
from typing import List
from fastapi.exceptions import HTTPException
from .schemas import Product, ProductCreate, ProductUpdateModel
from .product_data import read_products, write_products

product_router = APIRouter()


@product_router.get('/intro')
async def intro():
    return {
        "message": "A FastApi CRUD for products with modular project structure using routers with file handling"
    }


@product_router.get('/', response_model=List[Product])
async def get_all_products():
    return read_products()


@product_router.post('/', status_code=status.HTTP_201_CREATED)
async def create_products(product_data: ProductCreate) -> dict:
    products = read_products()

    new_product = product_data.model_dump()

    # auto increment id
    new_id = 1 if not products else products[-1]["id"] + 1
    new_product["id"] = new_id

    products.append(new_product)
    write_products(products)

    return new_product


@product_router.get('/{product_id}')
async def get_product(product_id: int) -> dict:
    products = read_products()

    for product in products:
        if product['id'] == product_id:
            return product

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Product Not Found OF ID:{product_id}"
    )


@product_router.patch('/{product_id}')
async def update_product(product_id: int, product_update_data: ProductUpdateModel) -> dict:
    products = read_products()

    for product in products:
        if product['id'] == product_id:
            product['name'] = product_update_data.name
            product['price'] = product_update_data.price

            write_products(products)
            return product

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Product Not Found OF ID:{product_id}"
    )


@product_router.delete('/{product_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int):
    products = read_products()

    for product in products:
        if product['id'] == product_id:
            products.remove(product)
            write_products(products)
            return None

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Product Not Found OF ID:{product_id}"
    )