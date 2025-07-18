# app/core/calculations.py

import datetime
import swisseph as swe

from .constants import SIGN_NAMES

def get_julian_day(year, month, day, hour, minute, second, tz_offset):
    """
    Returns the Julian Day number (UT) for given date, time, and timezone offset.
    """
    dt = datetime.datetime(year, month, day, hour, minute, second)
    dt_utc = dt - datetime.timedelta(hours=tz_offset)
    return swe.julday(
        dt_utc.year, dt_utc.month, dt_utc.day,
        dt_utc.hour + dt_utc.minute / 60.0 + dt_utc.second / 3600.0
    )

def get_rasi(longitude):
    """
    Given celestial longitude (deg), returns 1-based sign number (1=Aries ... 12=Pisces).
    """
    lon = longitude % 360
    return int(lon // 30) + 1

def get_ayanamsa(jd):
    """
    Returns Lahiri ayanamsa for a Julian Day.
    """
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    return swe.get_ayanamsa(jd)

def get_ascendant(jd, lat, lon):
    """
    Returns sidereal longitude of the Ascendant (Lagna), in degrees.
    """
    flag = swe.FLG_SWIEPH | swe.FLG_SIDEREAL
    cusps, ascmc = swe.houses_ex(jd, lat, lon, b'P', flag)
    return ascmc[0]

def get_tropical_ascendant(jd, lat, lon):
    """
    Returns tropical longitude of the Ascendant, in degrees.
    """
    flag = swe.FLG_SWIEPH
    cusps, ascmc = swe.houses_ex(jd, lat, lon, b'P', flag)
    return ascmc[0]

def get_navamsa_start_sign(rasi):
    """
    For a given Rasi (sign, 1-based), returns the starting sign for Navamsa calculation.
    """
    if rasi in [1, 4, 7, 10]:       # Movable: Aries, Cancer, Libra, Capricorn
        return rasi
    elif rasi in [2, 5, 8, 11]:     # Fixed: Taurus, Leo, Scorpio, Aquarius
        return (rasi + 8 - 1) % 12 + 1
    elif rasi in [3, 6, 9, 12]:     # Dual: Gemini, Virgo, Sagittarius, Pisces
        return (rasi + 4 - 1) % 12 + 1
    else:
        raise ValueError("Invalid sign number")

def get_d9_sign(longitude):
    """
    Returns Navamsa (D9) sign number (1-based) for longitude in degrees.
    """
    rasi = int(longitude // 30) + 1
    offset = longitude % 30
    navamsa_no = int(offset // (30 / 9))  # 0 to 8
    start_sign = get_navamsa_start_sign(rasi)
    navamsa_sign = ((start_sign + navamsa_no - 1) % 12) + 1
    return navamsa_sign

def get_nakshatra(longitude):
    """
    Given longitude (deg), returns 1-based Nakshatra number (1=Ashwini ... 27=Revati).
    """
    return int(longitude // (360 / 27)) + 1

def get_pada(longitude):
    """
    Given longitude (deg), returns 1-based Pada number (1-4 per Nakshatra; 108 for full zodiac).
    """
    return int((longitude % (360 / 27)) // (360 / 108)) + 1
