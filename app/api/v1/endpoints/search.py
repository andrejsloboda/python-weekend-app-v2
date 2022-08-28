from datetime import date
from typing import Optional, List

from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException

from ....scraper import scraper
from ....scraper.schemas import Route

router = APIRouter()


@router.get("/v1/search", response_model=List[Route])
async def search(origin: str, destination: str, departure_date: date, stops: Optional[int] = 0):
    scraped_data = scraper.scrape(origin, destination, departure_date)

    if scraped_data:
        return scraped_data
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

