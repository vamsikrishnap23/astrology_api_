from pydantic import BaseModel

class DivChartRequest(BaseModel):
    year: int
    month: int
    day: int
    hour: int
    minute: int
    second: int
    lat: float
    lon: float
    tz_offset: float
    varga_num: int = 1  

class DivChartSVGResponse(BaseModel):
    svg: str 
