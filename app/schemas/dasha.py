from pydantic import BaseModel, Field
from typing import List

class VimshottariDashaRequest(BaseModel):
    year: int
    month: int
    day: int
    hour: int
    minute: int
    second: int
    lat: float
    lon: float
    tz_offset: float

class Antardasha(BaseModel):
    antardasha_lord: str
    start: str
    end: str

class Mahadasha(BaseModel):
    mahadasha_lord: str
    start: str
    end: str
    antardashas: List[Antardasha]

class VimshottariDashaResponse(BaseModel):
    dashas: List[Mahadasha]
