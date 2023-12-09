from pydantic import BaseModel


class Boundary(BaseModel):
    lat_min: float
    lat_max: float
    long_min: float
    long_max: float


class Config(BaseModel):
    name: str
    boundaries: Boundary
    cell_size: float
