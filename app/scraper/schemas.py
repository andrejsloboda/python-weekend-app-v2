from datetime import datetime
from typing import List, Optional, Any

from pydantic import BaseModel


class Route(BaseModel):
    origin: str
    destination: str
    departure: datetime
    arrival: datetime
    carrier: str
    vehicle_type: str
    price: float
    currency: str
    source_id: str
    destination_id: str
    free_seats: int

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda t: t.strftime(format="%Y-%m-%d %H:%M:%S")
        }


class FlixbusLocation(BaseModel):
    lon: float
    lat: float


class FlixbusCity(BaseModel):
    score: float
    country: str
    has_train_station: bool
    district: str
    name: str
    legacy_id: int
    location: FlixbusLocation
    timezone_offset_seconds: Optional[int]
    id: str
    is_flixbus_city: Optional[bool]


class FlixbusCityResponse(BaseModel):
    __root__: List[FlixbusCity]


class FlixbusTrip(BaseModel):
    departure_city_id: str
    arrival_city_id: str
    date: datetime
    results: dict
    means_of_transport: list
    departure: dict
    arrival: dict


class FlixbusSearchResponse(BaseModel):
    response_uuid: str
    trips: List[FlixbusTrip]
    operators: dict
    cities: dict
    stations: dict
    no_bikes_period: dict


class RegiojetStation(BaseModel):
    id: int
    name: str
    fullname: str
    aliases: List[str]
    address: str
    stationsTypes: List[str]
    iataCode: str
    stationUrl: str
    stationTimeZoneCode: str
    wheelChairPlatform: Optional[str]
    significance: int
    longitude: float
    latitude: float
    imageUrl: str


class RegiojetCity(BaseModel):
    id: int
    name: str
    aliases: List[str]
    stationsTypes: List[str]
    stations: List[RegiojetStation]


class RegiojetCountry(BaseModel):
    country: str
    code: str
    cities: List[RegiojetCity]


class RegiojetLocationResponse(BaseModel):
    __root__: List[RegiojetCountry]


class RegiojetRoute(BaseModel):
    id: str
    departureStationId: int
    departureTime: str
    arrivalStationId: int
    arrivalTime: str
    vehicleTypes: List[str]
    transfersCount: int
    freeSeatsCount: int
    priceFrom: int
    priceTo: int
    creditPriceFrom: int
    creditPriceTo: int
    pricesCount: int
    actionPrice: bool
    surcharge: bool
    notices: bool
    support: bool
    nationalTrip: bool
    bookable: bool
    delay: Optional[bool]
    travelTime: str
    vehicleStandardKey: str


class RegiojetSearchResponse(BaseModel):
    routes: List[RegiojetRoute]
    routesMessage: Optional[str]
    bannerBubbles: List[Any]
    textBubbles: dict
