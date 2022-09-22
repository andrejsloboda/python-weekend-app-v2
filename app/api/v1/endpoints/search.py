from datetime import date
from typing import Optional, List
import asyncio
from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from app.scraper.schemas import Route, RouteCombination

from app.database import database
from app.search import search as s

from app.scraper import scraper


router = APIRouter()


@router.get("/v1/search")
def search(origin: str, destination: str, departure_date: date, stops: Optional[int] = 0):

    print_out = s.search(origin, destination, departure_date)

    if print_out:
        return print_out
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.get("/v1/search/scraping", response_model=List[Route])
async def search_combination(origin: str, destination: str, departure_date: date, stops: Optional[int] = 0):
    pass
