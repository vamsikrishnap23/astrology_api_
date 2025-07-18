from pydantic import BaseModel

class TransitChartRequest(BaseModel):
    year: int
    month: int
    day: int
    hour: int
    minute: int
    second: int
    lat: float
    lon: float
    tz_offset: float

class TransitChartSVGResponse(BaseModel):
    svg: str
