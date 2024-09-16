from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fund_management.infrastructure.database import MongoDB
from fund_management.api.routes import fund_routes, transaction_routes
from fund_management.infrastructure.environment import config

@asynccontextmanager
async def lifespan(app: FastAPI):
    mongo_uri = config.get("mongo_uri")
    await MongoDB.connect_to_database(mongo_uri)
    
    try:
        yield
    finally:
        MongoDB.client.close()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

@app.get("/health")
def health():
    return {"status": 200, "msg": "Api Ok"}

app.include_router(fund_routes.router, prefix="/api")
app.include_router(transaction_routes.router, prefix="/api")
