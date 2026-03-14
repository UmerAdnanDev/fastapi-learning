from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import ProductCreateModel,ProductUpdateModel
class ProductService:
   async def get_all_products(self,session:AsyncSession):
      pass
   async def get_product(self,product_uuid: str,session:AsyncSession):
      pass
   async def create_product(self,product_data:ProductCreateModel,session:AsyncSession):
      pass
   async def update_product(self,product_uuid: str,update_data:ProductUpdateModel,session:AsyncSession):
      pass
   async def delete_product(self,product_uuid: str,session:AsyncSession):
      pass
