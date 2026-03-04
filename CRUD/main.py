#uvicorn CRUD.main:app --reload --port 8001
from fastapi import FastAPI,status
from pydantic import BaseModel # to create model layer for crud operations
from typing import List # to create a list of dicts(json data)
from fastapi.exceptions import HTTPException
app = FastAPI()
# an in memory database
products = [ 
  {
  "id" : 1 , "name" : "product_1" , "price" : 12.8
  },
  {
  "id" : 2 , "name" : "product_2" , "price" : 18
  },
  {
  "id" : 3 , "name" : "product_3" , "price" : 14.12
  }
]
class Product(BaseModel):
  id: int
  name: str
  price: float
class ProductUpdateModel(BaseModel):
  name: str
  price: float
@app.get('/')
async def intro():
  return {"message":"A FastApi CRUD for products"}
@app.get('/products',response_model=List[Product]) # pydantic expects dict but we were fetching a list of dict so we imported List module
async def get_all_products():
  return products
@app.post('/products',status_code=status.HTTP_201_CREATED)
async def create_products(product_data:Product)-> dict:
   new_product = product_data.model_dump() #coverts product_data into dict
   products.append(new_product)
   return new_product
@app.get('/products/{product_id}')
async def get_product(product_id:int) -> dict:
  for product in products:
    if product['id'] == product_id:
       return product
  raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Product Not Found OF ID:{product_id}")
@app.patch('/products/{product_id}')
async def update_product(product_id:int,product_update_data:ProductUpdateModel)-> dict:
  for product in products:
    if product['id'] == product_id:
      product['name'] = product_update_data.name
      product['price'] = product_update_data.price
      return product
  raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Product Not Found OF ID:{product_id}")
@app.get('/products/{product_id}')
async def delete_product(product_id:int):
  pass

