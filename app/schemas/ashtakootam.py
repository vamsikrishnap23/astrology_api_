from pydantic import BaseModel

class AshtakootamRequest(BaseModel):
    bride_year: int
    bride_month: int
    bride_day: int
    bride_hour: int
    bride_minute: int
    bride_second: int
    bride_lat: float
    bride_lon: float
    bride_tz_offset: float
    groom_year: int
    groom_month: int
    groom_day: int
    groom_hour: int
    groom_minute: int
    groom_second: int
    groom_lat: float
    groom_lon: float
    groom_tz_offset: float

class AshtakootamResponse(BaseModel):
    koota: dict
