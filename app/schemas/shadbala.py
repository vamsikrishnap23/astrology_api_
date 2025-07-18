from pydantic import BaseModel
from typing import List

class ShadBalaRequest(BaseModel):
    year: int
    month: int
    day: int
    hour: int
    minute: int
    second: int
    lat: float
    lon: float
    tz_offset: float

class PlanetShadBala(BaseModel):
    planet: str
    sthana: float
    dig: float
    kala: float
    cheshta: float
    naisargika: float
    drik: float
    total: float
    percent: float
    required: float

class ShadBalaResponse(BaseModel):
    balas: List[PlanetShadBala]
