from pydantic import BaseModel

class SarvaChartRequest(BaseModel):
    year: int
    month: int
    day: int
    hour: int
    minute: int
    second: int
    lat: float
    lon: float
    tz_offset: float

class SarvaChartResponse(BaseModel):
    svg: str  