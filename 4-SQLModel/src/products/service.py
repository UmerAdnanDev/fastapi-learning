from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import ProductCreateModel,ProductUpdateModel
from sqlmodel import select,desc #or asc
from .models import Product
class ProductService:
   # method to fetch all products
   async def get_all_products(self,session:AsyncSession):
      statement = select(Product).order_by(desc(Product.created_at))
      result = await session.exec(statement)
      return result.all()
   #method to fetch single product by id
   async def get_product(self,product_uuid: str,session:AsyncSession):
      statement = select(Product).where(Product.uid == product_uuid)
      result = await session.exec(statement)
      product = result.first()
      return product if product is not None else None 
   #method to create a product
   async def create_product(self,product_data:ProductCreateModel,session:AsyncSession):
      product_data_dict = product_data.model_dump()
      new_product = Product(
            **product_data_dict
      )
      session.add(new_product)
      await session.commit()
      return new_product
   #method to update a product by id
   async def update_product(self,product_uuid: str,update_data:ProductUpdateModel,session:AsyncSession):
      product_to_update = self.get_product(product_uuid,session)
      update_data_dict = update_data.model_dump()
      if product_to_update is not None: #
       for k , v in update_data_dict.items():
         setattr(product_to_update,k,v)
       await session.commit()
       return product_to_update
      else:
         return None
   #method to delete a product by id
   async def delete_product(self,product_uuid: str,session:AsyncSession):
      product_to_delete = self.get_product(product_uuid,session)
      if product_to_delete is not None:
         await session.delete(product_to_delete)
         await session.commit()
      else:
         return None