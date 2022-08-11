from fastapi import APIRouter
from app import app


api_router = APIRouter()


@app.get("/whisper")
def whisper(text: str):
    return [city for city in scraper.cities if ls.normalized_similarity(text, city) > 0.5]







