import swisseph as swe
from datetime import datetime
from .constants import SIGN_NAMES, NAKSHATRA_NAMES, PLANETS
from .calculations import get_julian_day, get_ascendant, get_rasi, get_nakshatra, get_pada

def get_planet_longitude_and_speed(jd, planet_id):
    flag = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED
    lon, lat, dist, speed_long, *_ = swe.calc_ut(jd, planet_id, flag)[0]
    return lon % 360, speed_long

def get_retrograde(speed):
    return speed < 0

def progression_chart(nat_dt, nat_lat, nat_lon, nat_tz_offset, prg_dt):
    # 1 day after birth = 1 year progressed (secondary progression)
    years_passed = (prg_dt - nat_dt.replace(hour=0, minute=0, second=0, microsecond=0)).days
    natal_jd = get_julian_day(
        nat_dt.year, nat_dt.month, nat_dt.day,
        nat_dt.hour, nat_dt.minute, nat_dt.second, nat_tz_offset
    )
    progressed_jd = natal_jd + years_passed  # 1 day per year

    swe.set_sid_mode(swe.SIDM_LAHIRI)
    flag = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED
    chart = {}
    rahu_longi = None
    rahu_speed = None

    # All planets except Ketu (handled below)
    for planet_name, planet_id in PLANETS.items():
        if planet_name == "Ketu":
            continue
        lon_arr, _ = swe.calc_ut(progressed_jd, planet_id, flag)
        longi = lon_arr[0] % 360
        speed = lon_arr[3]
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

    # Ketu (opposite Rahu, always retrograde)
    if rahu_longi is not None and rahu_speed is not None:
        ketu_longi = (rahu_longi + 180) % 360
        ketu_speed = -rahu_speed
        ketu_sign = get_rasi(ketu_longi)
        ketu_nak = get_nakshatra(ketu_longi)
        ketu_pada = get_pada(ketu_longi)
        chart["Ketu"] = {
            "longitude": ketu_longi,
            "sign": SIGN_NAMES[ketu_sign],
            "deg_in_sign": ketu_longi % 30,
            "nakshatra": NAKSHATRA_NAMES[ketu_nak - 1],
            "pada": ketu_pada,
            "retrograde": True,
            "speed": ketu_speed
        }

    # Ascendant (Lagna) at natal place on progression day
    asc = get_ascendant(progressed_jd, nat_lat, nat_lon)
    asc_sign = get_rasi(asc)
    asc_nak = get_nakshatra(asc)
    asc_pada = get_pada(asc)
    chart["Ascendant"] = {
        "longitude": asc,
        "sign": SIGN_NAMES[asc_sign],
        "deg_in_sign": asc % 30,
        "nakshatra": NAKSHATRA_NAMES[asc_nak - 1],
        "pada": asc_pada,
        "retrograde": False,
        "speed": 0.0
    }
    return chart
