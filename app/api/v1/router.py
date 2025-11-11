from fastapi import APIRouter
from app.api.v1.endpoints import compliance, goods

api_router = APIRouter()

api_router.include_router(compliance.router)
api_router.include_router(goods.router)