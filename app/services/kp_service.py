from app.core.calculations import get_julian_day
from app.core.kp import get_kp_system_full

def get_kp_details_service(params):
    jd = get_julian_day(
        params.year, params.month, params.day,
        params.hour, params.minute, params.second,
        params.tz_offset
    )
    return get_kp_system_full(jd, params.lat, params.lon, params.tz_offset)
