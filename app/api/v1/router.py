from fastapi import APIRouter
from .endpoints import search, whisper, health

v1_api_router = APIRouter()
v1_api_router.include_router(search.router)
v1_api_router.include_router(whisper.router)
v1_api_router.include_router(health.router)


