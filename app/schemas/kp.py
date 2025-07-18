from pydantic import BaseModel
from typing import List, Dict

class HouseKPItem(BaseModel):
    House_Id: int
    Sign: str
    Position: str
    Star: str
    Sign_Lord: str
    Star_Lord: str
    Sub_Lord: str
    SS_Lord: str
    SSS_Lord: str

class PlanetKPItem(BaseModel):
    Planet: str
    Sign: str
    Position: str
    House: int
    Star: str
    Sign_Lord: str
    Star_Lord: str
    Sub_Lord: str
    SS_Lord: str
    SSS_Lord: str

class KpSystemRequest(BaseModel):
    year: int
    month: int
    day: int
    hour: int
    minute: int
    second: int
    lat: float
    lon: float
    tz_offset: float

class KpSystemResponse(BaseModel):
    houses: List[HouseKPItem]
    planets: List[PlanetKPItem]
    house_significators: Dict[int, Dict[str, List[str]]]
    planet_significators: Dict[str, Dict[str, List[str]]]
