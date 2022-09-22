from typing import List
from datetime import date
from slugify import slugify
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Row
from sqlalchemy.pool import NullPool
from sqlalchemy.types import Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import cast
from app.settings import settings
from app.database.models import RouteORM, Base


DATABASE_URL = f"postgresql://{settings.db_user}:{settings.db_password}@\
{settings.db_hostname}:{settings.db_port}/{settings.db_database}"

engine = create_engine(DATABASE_URL, echo=True, poolclass=NullPool)
Base.metadata.create_all(engine)
Session = sessionmaker(engine, autocommit=False, autoflush=False)


def add_routes_to_db(routes: List[RouteORM]) -> None:
    if routes:
        with Session() as session:
            for route in routes:
                session.add(RouteORM(**dict(route)))
            session.commit()


def get_distinct_routes_from_db() -> List[Row]:
    with engine.connect() as connection:
        select_query = "SELECT DISTINCT origin, destination FROM public.journeys_asloboda"
        data = connection.execute(text(select_query)).fetchall()
        return data


def get_data_from_db(departure_date: date) -> List[RouteORM]:
    with Session() as session:
        routes = session.query(RouteORM).filter(
            cast(RouteORM.departure, Date) == departure_date,
            RouteORM.free_seats > 0
        ).all()
        return routes


def is_in_db(origin: str, destination: str, departure_date: date) -> bool:
    with Session() as session:
        if session.query(RouteORM).filter(
            RouteORM.origin == slugify(origin),
            RouteORM.destination == slugify(destination),
            cast(RouteORM.departure, Date) == departure_date
        ).all():
            return True
        else:
            return False





