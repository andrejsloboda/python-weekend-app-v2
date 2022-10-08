from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy import Column, Integer, String, DECIMAL

Base = declarative_base()


class City(Base):
    __tablename__ = 'cities'
    id = Column(Integer, primary_key=True)
    city = Column(String)
    slug = Column(String)
    language = Column(String)
    city_id = Column(UUID)
    lat = Column(DECIMAL)
    lon = Column(DECIMAL)


class Route(Base):
    __tablename__ = "journeys"
    id = Column(Integer, primary_key=True)
    origin = Column(String(255))
    destination = Column(String(255))
    departure = Column(TIMESTAMP)
    arrival = Column(TIMESTAMP)
    carrier = Column(String(255))
    vehicle_type = Column(String(255))
    price = Column(DECIMAL(10,2))
    currency = Column(String(3))
    source_id = Column(String(255))
    destination_id = Column(String(255))
    free_seats = Column(Integer)



