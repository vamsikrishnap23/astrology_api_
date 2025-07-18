from pydantic import BaseModel

class ProgressionChartRequest(BaseModel):
    # Base (natal) details
    nat_year: int
    nat_month: int
    nat_day: int
    nat_hour: int
    nat_minute: int
    nat_second: int
    nat_lat: float
    nat_lon: float
    nat_tz_offset: float

    # Progression/target date (for progressed positions)
    prg_year: int
    prg_month: int
    prg_day: int

class ProgressionChartSVGResponse(BaseModel):
    svg: str
