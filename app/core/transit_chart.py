import swisseph as swe
from datetime import datetime
from .constants import TELUGU_PLANETS, TELUGU_SIGNS, TELUGU_NAKSHATRAS, PLANETS
from .calculations import get_julian_day, get_ascendant, get_rasi, get_nakshatra, get_pada

def get_planet_longitude_and_speed(jd, planet_id):
    flag = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED
    lon, lat, dist, speed_long, *_ = swe.calc_ut(jd, planet_id, flag)[0]
    return lon % 360, speed_long

def get_retrograde(speed):
    return speed < 0

def transit_chart(dt, lat, lon, tz_offset=0.0):
    """
    Compute the transit chart for a given datetime and location.
    Returns a dict with all planets/nodes/lagna—all values in Telugu.
    """
    jd = get_julian_day(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, tz_offset)
    chart = {}
    rahu_longi = rahu_speed = None

    swe.set_sid_mode(swe.SIDM_LAHIRI)

    for planet_name, planet_id in PLANETS.items():
        if planet_name == "Ketu":
            continue  # Handled after Rahu
        longi, speed = get_planet_longitude_and_speed(jd, planet_id)
        sign_num = get_rasi(longi)
        nak_num = get_nakshatra(longi)
        pada_num = get_pada(longi)
        retro = get_retrograde(speed)
        chart[planet_name] = {
            "graham": TELUGU_PLANETS.get(planet_name, planet_name),
            "rasi": TELUGU_SIGNS[sign_num],
            "deg_in_rasi": round(longi % 30, 2),
            "nakshatram": TELUGU_NAKSHATRAS[nak_num - 1],
            "padam": str(pada_num),
            "vakragathi": "వక్ర" if retro else "సామన్య",
            "vegamu": round(speed, 5)
        }
        if planet_name == "Rahu":
            rahu_longi = longi
            rahu_speed = speed

    # Ketu: always 180 deg opposite Rahu
    if rahu_longi is not None and rahu_speed is not None:
        ketu_longi = (rahu_longi + 180) % 360
        ketu_speed = -rahu_speed
        sign_num = get_rasi(ketu_longi)
        nak_num = get_nakshatra(ketu_longi)
        pada_num = get_pada(ketu_longi)
        retro = get_retrograde(ketu_speed)
        chart["Ketu"] = {
            "graham": TELUGU_PLANETS["Ketu"],
            "rasi": TELUGU_SIGNS[sign_num],
            "deg_in_rasi": round(ketu_longi % 30, 2),
            "nakshatram": TELUGU_NAKSHATRAS[nak_num - 1],
            "padam": str(pada_num),
            "vakragathi": "వక్ర" if retro else "సామన్య",
            "vegamu": round(ketu_speed, 5)
        }

    # Ascendant (Lagna)
    asc = get_ascendant(jd, lat, lon)
    sign_num = get_rasi(asc)
    nak_num = get_nakshatra(asc)
    pada_num = get_pada(asc)
    chart["Ascendant"] = {
        "graham": "లగ్నం",
        "rasi": TELUGU_SIGNS[sign_num],
        "deg_in_rasi": round(asc % 30, 2),
        "nakshatram": TELUGU_NAKSHATRAS[nak_num - 1],
        "padam": str(pada_num),
        "vakragathi": "సామన్య",
        "vegamu": 0.0
    }

    return chart
