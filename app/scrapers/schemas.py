from datetime import datetime
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
    source_id: int
    destination_id: int
    free_seats: int

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda t: t.strftime(format="%Y-%m-%d %H:%M:%S")
        }