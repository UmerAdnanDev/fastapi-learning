from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import ProductCreateModel, ProductUpdateModel
from sqlmodel import select, desc
from .models import Product
from datetime import datetime
from fastapi import HTTPException, status
import uuid

class ProductService:
    # method to fetch all products
    async def get_all_products(self, session: AsyncSession):
        statement = select(Product).order_by(desc(Product.created_at))
        result = await session.exec(statement)
        return result.all()
    
    # method to fetch single product by id
    async def get_product(self, product_uuid: str, session: AsyncSession):
        # Convert string UUID to UUID object for comparison
        try:
            uuid_obj = uuid.UUID(product_uuid) if isinstance(product_uuid, str) else product_uuid
            statement = select(Product).where(Product.uid == uuid_obj)
            result = await session.exec(statement)
            product = result.first()
            return product if product is not None else None
        except ValueError:
            return None
    
    # method to create a product
    async def create_product(self, product_data: ProductCreateModel, session: AsyncSession):
        product_data_dict = product_data.model_dump()
        
        # Fix: Use 'publish_date' not 'published_date'
        new_product = Product(
            name=product_data_dict['name'],
            price=product_data_dict['price'],
            publish_date=datetime.strptime(product_data_dict['publish_date'], "%Y-%m-%d"),
            created_at=datetime.now(),
            updated_at=datetime.now()
        ) # type: ignore
        
        session.add(new_product)
        await session.commit()
        await session.refresh(new_product)  # Refresh to get generated values
        return new_product
    
    # method to update a product by id
    async def update_product(self, product_uuid: str, update_data: ProductUpdateModel, session: AsyncSession):
        # FIX: Added await here
        product_to_update = await self.get_product(product_uuid, session)
        
        if product_to_update is None:
            return None
        
        update_data_dict = update_data.model_dump(exclude_unset=True)  # Only include provided fields
        
        for k, v in update_data_dict.items():
            if k == 'publish_date' and v is not None:
                setattr(product_to_update, k, datetime.strptime(v, "%Y-%m-%d"))
            elif v is not None:
                setattr(product_to_update, k, v)
        
        product_to_update.updated_at = datetime.now()
        await session.commit()
        await session.refresh(product_to_update)
        return product_to_update
    
    # method to delete a product by id
    async def delete_product(self, product_uuid: str, session: AsyncSession):
        # FIX: Added await here
        product_to_delete = await self.get_product(product_uuid, session)
        
        if product_to_delete is None:
            return None
        
        await session.delete(product_to_delete)
        await session.commit()
        return True