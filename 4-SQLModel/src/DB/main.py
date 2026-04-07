from sqlmodel import create_engine, SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from src.config import Config
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

# FIX: Use create_async_engine directly instead of wrapping
engine = create_async_engine(
    url=Config.DATABASE_URL,
    echo=True,
    future=True
)

async def init_db():
    async with engine.begin() as conn:
        from src.products.models import Product
        await conn.run_sync(SQLModel.metadata.create_all)

# FIX: Make this an async generator properly
async def get_session():
    async_session = sessionmaker(
        engine,  # type: ignore
        class_=AsyncSession, 
        expire_on_commit=False
    ) # type: ignore
    
    async with async_session() as session: # type: ignore
        yield session