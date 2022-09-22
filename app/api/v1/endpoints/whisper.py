from fastapi import APIRouter



router = APIRouter()


@router.get("/v1/whisper")
def whisper(text: str):
    return [city for city in scraper.cities if ls.normalized_similarity(text, city) > 0.5]







