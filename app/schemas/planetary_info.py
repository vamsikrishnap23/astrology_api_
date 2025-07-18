from pydantic import BaseModel, Field
from typing import List

class PlanetaryInfoRequest(BaseModel):
    year: int
    month: int
    day: int
    hour: int
    minute: int
    second: int
    lat: float
    lon: float
    tz_offset: float
    varga_num: int = Field(1, description="Divisional chart number (1=D1 Rasi, 9=Navamsa, etc.)")

class PlanetInfo(BaseModel):
    planet: str
    degrees: str
    rasi: str
    rasi_adhipathi: str
    nakshatram: str
    padam: int
    retrogration: str
    speed: str

class PlanetaryInfoResponse(BaseModel):
    info: List[PlanetInfo]
