from fastapi import APIRouter
from .endpoints import search, whisper, health


v1_api_router = APIRouter()
v1_api_router.include_router(search.api_router)
v1_api_router.include_router(whisper.api_router)
v1_api_router.include_router(health.api_router)
