from pydantic import BaseModel


class Cell(BaseModel):
    lat_min: float
    lat_max: float
    long_min: float
    long_max: float
