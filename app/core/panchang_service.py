from app.core.panchang import get_panchang_telugu
from app.core.calculations import get_julian_day

def get_panchang_details(params):
    jd = get_julian_day(
        params.year, params.month, params.day,
        params.hour, params.minute, params.second,
        params.tz_offset
    )
    # You can pass lat/lon/tz for further development (sunrise, etc), but not used directly here
    return get_panchang_telugu(jd, params.lat, params.lon, params.tz_offset)
