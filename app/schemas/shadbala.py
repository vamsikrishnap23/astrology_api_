from pydantic import BaseModel
from typing import Dict, List

class BalaDetail(BaseModel):
    value: float
    detail: Dict[str, float]

class PlanetShadBala(BaseModel):
    planet: str
    min_required: float
    total: float
    percent: float
    rank: int
    sthana: BalaDetail
    dig: BalaDetail
    kala: BalaDetail
    cheshta: BalaDetail
    naisargika: float
    drik: BalaDetail
    rupa: float
    ishta_phala: float
    kashta_phala: float

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

class ShadBalaResponse(BaseModel):
    balas: List[PlanetShadBala]
