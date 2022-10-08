from datetime import date
from typing import List
from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from app.api.v1 import RouteOutCombination
from app.search import search as s

router = APIRouter()


@router.get("/v1/search", response_model=List[RouteOutCombination])
def search(origin: str, destination: str, departure_date: date):

    print_out = s.search(origin, destination, departure_date)

    if print_out:
        return print_out
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

