from fastapi import APIRouter
from app import app


api_router = APIRouter()


@app.get('/ping')
def ping():
    return 'pong'
