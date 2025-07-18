from app.core.shadbala import compute_shadbala
from app.core.constants import TELUGU_PLANET_SHORT

def get_shadbala_data(params):
    return compute_shadbala(
        params.year, params.month, params.day,
        params.hour, params.minute, params.second,
        params.lat, params.lon, params.tz_offset
    )
