from typing import Optional
from fastapi import APIRouter
from app import app

api_router = APIRouter()


@app.get("/search", response_model=List[RouteOut])
def search(origin: str, destination: str, departure: datetime.date, stops: Optional[int] = 0):
    pass


@app.get("/search/combinations", response_model=List[RouteCombination])
def combinations(origin: str, destination: str, departure: datetime.date):
    pass
