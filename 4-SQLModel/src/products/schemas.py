from pydantic import BaseModel 
import uuid
from datetime import datetime
class Product(BaseModel):
    uid: uuid.UUID  # Changed from 'uuid' to 'uid' to match model
    name: str
    price: float
    publish_date: datetime  # Changed from str to datetime
    created_at: datetime
    updated_at: datetime

class ProductCreateModel(BaseModel):
    name: str
    price: float
    publish_date: str  # Keep as str for input, will convert in service

class ProductUpdateModel(BaseModel):
    name: str | None = None  # Make optional for partial updates
    price: float | None = None
    publish_date: str | None = None