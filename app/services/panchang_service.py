from app.core.panchang import get_panchang_minimal
from app.core.calculations import get_julian_day

def get_panchang_details(params):
    jd = get_julian_day(
        params.year, params.month, params.day,
        params.hour, params.minute, params.second,
        params.tz_offset
    )
    details = get_panchang_minimal(jd, params.lat, params.lon, params.tz_offset)
    return {
        "nakshatram": details["Nakshatram"],
        "padam": details["Padam"],
        "rasi": details["Rasi"],
        "vaaram": details["Vaaram"]
    }
