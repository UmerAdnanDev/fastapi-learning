from fastapi import APIRouter,status,Depends
from typing import List
from fastapi.exceptions import HTTPException
#from .product_data import products (no longer using in memory database that's why we remove product_data json file)
from .schemas import Product,ProductUpdateModel
from src.DB.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.products.service import ProductService
product_router = APIRouter()
product_service = ProductService()
#get request handler to display intro json
@product_router.get('/intro')
async def intro():
  return {"message":"A FastApi CRUD for products "
  "with modular project structure using Routers" 
  "And using SqlModel for pgsql integration"}
# get request handler to fetch all products
@product_router.get('/',response_model=List[Product]) # pydantic expects dict but we were fetching a list of dict so we imported List module
async def get_all_products(session:AsyncSession=Depends(get_session)):
  products = product_service.get_all_products(session)
  return products

#post request handler to create a product
@product_router.post('/',status_code=status.HTTP_201_CREATED,response_model=Product)
async def create_products(product_data:Product,session:AsyncSession=Depends(get_session))-> dict:
  new_product =await product_service.create_product(product_data,session) # type: ignore
  return new_product # type: ignore

# get request handler to fetch a product by id
@product_router.get('/{product_uid}')
async def get_product(product_uid:int,session:AsyncSession=Depends(get_session)) -> dict:
  product =await product_service.get_product(product_uid,session)  # type: ignore
  if product:
    return product # type: ignore
  else:
   raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Product Not Found OF ID:{product_uid}")

# patch request handler to update a product 
@product_router.patch('/{product_uid}')
async def update_product(product_uid:int,product_update_data:ProductUpdateModel,session:AsyncSession=Depends(get_session))-> dict:
  update_product= await product_service.update_product(product_uid,product_update_data,session) # type: ignore
  if update_product:
    return update_product # type: ignore
  else:
   raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Product Not Found OF ID:{product_uid}")

# delete request handler to delete a product
@product_router.delete('/{product_uid}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_uid:str,session:AsyncSession=Depends(get_session)):
  product_delete = await product_service.delete_product(product_uid,session)
  if product_delete is not None:
    return None
  else:
   raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Product Not Found OF ID:{product_uid}")
