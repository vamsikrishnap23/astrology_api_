from app.core.shadbala import compute_shadbala
from app.core.constants import TELUGU_PLANET_SHORT

def get_shadbala_data(params):
    shadbala_result = compute_shadbala(
        params.year, params.month, params.day, params.hour, params.minute, params.second,
        params.lat, params.lon, params.tz_offset
    )
    output = []
    for b in shadbala_result['planets']:
        output.append(
            {
                "planet": TELUGU_PLANET_SHORT.get(b["name"], b["name"]),
                "sthana": b["sthana"],
                "dig": b["dig"],
                "kala": b["kala"],
                "cheshta": b["cheshta"],
                "naisargika": b["naisargika"],
                "drik": b["drik"],
                "total": b["total"],
                "percent": b["percent"],
                "required": b["required"]
            }
        )
    return {"balas": output}
