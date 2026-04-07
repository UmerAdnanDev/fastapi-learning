from fastapi import FastAPI
from src.products.routes import product_router
from contextlib import asynccontextmanager
from src.DB.main import init_db

# to decide what is excuted at the start and end of the app
@asynccontextmanager
async def life_span(app:FastAPI):
    print(f"server is starting ...") 
    await init_db()
    # at start of server (executes)
    yield
    print(f"server has been stoped") # at end executes
    
version = "v2"
app = FastAPI(version=version,
              title="An Async Product CRUD with PostgreSQL integration w.t.h of SQLModel",
              description="A RestAPI for product web service",
              lifespan=life_span)

app.include_router(product_router,prefix=f"/api/{version}/products",tags=['products'])
#to run
# cd 4-SQLModel
#uvicorn src.main:app --reload --port 8003

