from pydantic import BaseModel, Field

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
    padam: int
    rasi: str
    vaaram: str
