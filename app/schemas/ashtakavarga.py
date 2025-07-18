from pydantic import BaseModel, Field
from typing import List

class AshtakavargaRequest(BaseModel):
    year: int
    month: int
    day: int
    hour: int
    minute: int
    second: int
    lat: float
    lon: float
    tz_offset: float

class PlanetRekhaRow(BaseModel):
    planet: str
    rekhas: List[int]  # 12 bindus (signs)

class AshtakavargaResponse(BaseModel):
    rekha_table: List[PlanetRekhaRow]   # 8 rows: Sun...Saturn, Ascendant
    sarva: List[int]                    # 12 total bindus per sign
    labels: dict                        # {'planets': List[str], 'signs': List[str]} in Telugu
