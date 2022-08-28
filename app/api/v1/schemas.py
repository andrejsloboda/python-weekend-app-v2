from datetime import datetime
from pydantic import BaseModel


class RouteOut(BaseModel):
    origin: str
    destination: str
    departure: datetime
    arrival: datetime
    carrier: str

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda t: t.strftime(format="%Y-%m-%d %H:%M:%S")
        }
