from pydantic import BaseModel

class PanchangRequest(BaseModel):
    year: int
    month: int
    day: int
    hour: int
    minute: int
    second: int
    lat: float
    lon: float
    tz_offset: float

class PanchangResponse(BaseModel):
    nakshatram: str
    padam: str
    rasi: str
    varam: str
    tithi: str
    yoga: str
    karanam: str
