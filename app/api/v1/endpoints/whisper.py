from app.database import database
from fastapi import APIRouter
from rapidfuzz.distance import Levenshtein as Ls

router = APIRouter()


@router.get("/v1/whisper")
async def whisper(text: str):
    cities = database.load_cities()
    return [city for city in cities if Ls.normalized_similarity(text, city) > 0.5]








