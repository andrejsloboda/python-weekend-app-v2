from typing import List
from datetime import date
from slugify import slugify
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Row
from sqlalchemy.types import Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import cast
from app.settings import settings
from app.database.models import Route, Base, City


DATABASE_URL = f"postgresql://{settings.db_user}:{settings.db_password}@\
{settings.db_hostname}:{settings.db_port}/{settings.db_database}"
engine = create_engine(DATABASE_URL, echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(engine, autocommit=False, autoflush=True)


def get_city_id(city_name: str) -> str:
    with Session() as session:
        result = session.query(City).filter(
            City.city == city_name
        ).first()
    return result.city_id


def get_city_name(city_id: str) -> str:
    with Session() as session:
        result = session.query(City).filter(
            City.city_id == city_id,
        ).first()
    return result.city


def load_cities():
    raw_query = 'SELECT DISTINCT city FROM public.cities'
    with engine.connect() as con:
        result = con.execute(text(raw_query))
        return result


def add_routes_to_db(routes: List[Route]) -> None:
    if routes:
        with Session() as session:
            for route in routes:
                session.add(route)
            session.commit()


def get_distinct_routes_from_db() -> List[Row]:
    with engine.connect() as connection:
        select_query = "SELECT DISTINCT origin, destination FROM public.journeys_asloboda"
        data = connection.execute(text(select_query)).fetchall()
        return data


def get_data_from_db(departure_date: date) -> List[Route]:
    with Session() as session:
        routes = session.query(Route).filter(
            cast(Route.departure, Date) == departure_date,
            Route.free_seats > 0
        ).all()
        return routes


def is_in_db(origin: str, destination: str, departure_date: date) -> bool:
    with Session() as session:
        if session.query(Route).filter(
            Route.origin == slugify(origin),
            Route.destination == slugify(destination),
            cast(Route.departure, Date) == departure_date
        ).all():
            return True
        else:
            return False





