# app/core/transit_chart.py

import swisseph as swe
from datetime import datetime
from .constants import SIGN_NAMES, NAKSHATRA_NAMES, PLANETS
from .calculations import get_julian_day, get_ascendant, get_rasi, get_nakshatra, get_pada

def get_planet_longitude_and_speed(jd, planet_id):
    # For all planets except nodes, MEAN_NODE for Rahu
    flag = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED
    lon, lat, dist, speed_long, *_ = swe.calc_ut(jd, planet_id, flag)[0]
    return lon % 360, speed_long

def get_retrograde(speed):
    return speed < 0

def transit_chart(dt, lat, lon, tz_offset=0.0):
    """
    Compute the transit chart for a given datetime and location.
    Returns a dict with all planets, nodes, and lagna:
      {
        "Sun": {
            "longitude": ..., "sign": ..., "deg_in_sign": ...,
            "nakshatra": ..., "pada": ..., "retrograde": ..., "speed": ...
        },
        ...
      }
    """
    jd = get_julian_day(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, tz_offset)
    chart = {}
    rahu_longi = rahu_speed = None

    # Main planets (and outer planets if PLANETS contains them)
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    for planet_name, planet_id in PLANETS.items():
        if planet_name == "Ketu":
            continue  # Ketu is handled with Rahu
        longi, speed = get_planet_longitude_and_speed(jd, planet_id)
        sign = get_rasi(longi)
        nak = get_nakshatra(longi)
        pada = get_pada(longi)
        retro = get_retrograde(speed)
        chart[planet_name] = {
            "longitude": longi,
            "sign": SIGN_NAMES[sign],
            "deg_in_sign": longi % 30,
            "nakshatra": NAKSHATRA_NAMES[nak - 1],
            "pada": pada,
            "retrograde": retro,
            "speed": speed
        }
        if planet_name == "Rahu":
            rahu_longi = longi
            rahu_speed = speed

    # Ketu (always opposite Rahu)
    if rahu_longi is not None and rahu_speed is not None:
        ketu_longi = (rahu_longi + 180) % 360
        ketu_speed = -rahu_speed
        sign = get_rasi(ketu_longi)
        nak = get_nakshatra(ketu_longi)
        pada = get_pada(ketu_longi)
        retro = get_retrograde(ketu_speed)
        chart["Ketu"] = {
            "longitude": ketu_longi,
            "sign": SIGN_NAMES[sign],
            "deg_in_sign": ketu_longi % 30,
            "nakshatra": NAKSHATRA_NAMES[nak - 1],
            "pada": pada,
            "retrograde": retro,
            "speed": ketu_speed
        }

    # Ascendant (Lagna)
    asc = get_ascendant(jd, lat, lon)
    sign = get_rasi(asc)
    nak = get_nakshatra(asc)
    pada = get_pada(asc)
    chart["Ascendant"] = {
        "longitude": asc,
        "sign": SIGN_NAMES[sign],
        "deg_in_sign": asc % 30,
        "nakshatra": NAKSHATRA_NAMES[nak - 1],
        "pada": pada,
        "retrograde": False,
        "speed": 0.0
    }
    return chart