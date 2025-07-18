# app/core/panchang.py

import swisseph as swe
from .constants import (
    NAKSHATRA_NAMES, TELUGU_NAKSHATRAS,
    SIGN_NAMES, TELUGU_SIGNS,
    ENGLISH_WEEKDAYS, TELUGU_VAARAM
)

def get_ayanamsa(jd):
    return swe.get_ayanamsa(jd)

def get_sidereal_longitude(jd, planet):
    flag = swe.FLG_SWIEPH | swe.FLG_SIDEREAL
    lon, _ = swe.calc_ut(jd, planet, flag)
    return lon[0] % 360

def get_panchang(jd, lat, lon, tz_offset, language='te'):
    """
    Returns a dict with full Panchangam details (nakshatra, pada, rasi, tithi, yoga, karana, vara) in selected language.
    """
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    # Sidereal Moon and Sun longitude
    moon_long = get_sidereal_longitude(jd, swe.MOON)
    sun_long = get_sidereal_longitude(jd, swe.SUN)

    # Nakshatra (27-fold, 13°20')
    nakshatra_span = 360/27
    nak_num = int(moon_long // nakshatra_span)
    nak_deg = moon_long % nakshatra_span
    nak_name = NAKSHATRA_NAMES[nak_num]
    telugu_nak = TELUGU_NAKSHATRAS[nak_num]

    # Pada (each pada is 3°20')
    pada = int((moon_long % nakshatra_span) // (360/108)) + 1

    # Rasi (sign)
    sign_num = int(moon_long // 30) + 1
    sign_name = SIGN_NAMES[sign_num]
    telugu_sign = TELUGU_SIGNS[sign_num]
    deg_in_rasi = moon_long % 30

    # Vara (weekday)
    weekday_num = int((jd + 1.5) % 7)
    weekday_eng = ENGLISH_WEEKDAYS[weekday_num]
    weekday_te = TELUGU_VAARAM[weekday_eng]

    # Output as per requested language
    if language == "te":
        return {
            "nakshatram": telugu_nak,
            "padam": pada,
            "rasi": telugu_sign,
            "vaaram": weekday_te
        }
    else:
        return {
            "nakshatram": nak_name,
            "padam": pada,
            "rasi": sign_name,
            "vaaram": weekday_eng
        }

def get_panchang_minimal(jd, lat, lon, tz_offset):
    """
    Returns a dict: {
        'Nakshatram': <name in Telugu>,
        'Padam': <pada>,
        'Rasi': <Telugu sign name>,
        'Vaaram': <Telugu weekday>
    }
    Used for the minimal API Panchangam endpoint.
    """
    details = get_panchang(jd, lat, lon, tz_offset, language='te')
    # For frontend/table compatibility, capitalize keys
    return {
        "Nakshatram": details["nakshatram"],
        "Padam": details["padam"],
        "Rasi": details["rasi"],
        "Vaaram": details["vaaram"]
    }
