import swisseph as swe
from app.core.calculations import get_julian_day, get_rasi
from app.core.chart_logic import get_varga_longitude

def get_planet_degrees_and_retro(year, month, day, hour, minute, second, lat, lon, tz_offset, varga_num):
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    jd = get_julian_day(year, month, day, hour, minute, second, tz_offset)
    flag = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED
    deg_retro = {}
    # Classical planets and nodes
    PLANETS = {
        "Sun": swe.SUN, "Moon": swe.MOON, "Mars": swe.MARS,
        "Mercury": swe.MERCURY, "Jupiter": swe.JUPITER, "Venus": swe.VENUS,
        "Saturn": swe.SATURN, "Uranus": swe.URANUS,
        "Neptune": swe.NEPTUNE, "Pluto": swe.PLUTO
    }
    for planet, pid in PLANETS.items():
        lon_arr, _ = swe.calc_ut(jd, pid, flag)
        longitude = lon_arr[0] % 360
        speed = lon_arr[3]
        varga_long = get_varga_longitude(longitude, varga_num) % 360
        sign = get_rasi(varga_long)
        deg_in_sign = varga_long % 30
        retro = speed < 0
        deg_retro[(planet, sign)] = (deg_in_sign, retro)
    # Rahu
    rahu_arr, _ = swe.calc_ut(jd, swe.MEAN_NODE, flag)
    rahu_long = rahu_arr[0] % 360
    rahu_speed = rahu_arr[3]
    rahu_varga_long = get_varga_longitude(rahu_long, varga_num) % 360
    rahu_sign = get_rasi(rahu_varga_long)
    rahu_deg_in_sign = rahu_varga_long % 30
    deg_retro[("Rahu", rahu_sign)] = (rahu_deg_in_sign, True)
    # Ketu
    ketu_long = (rahu_long + 180) % 360
    ketu_speed = -rahu_speed
    ketu_varga_long = get_varga_longitude(ketu_long, varga_num) % 360
    ketu_sign = get_rasi(ketu_varga_long)
    ketu_deg_in_sign = ketu_varga_long % 30
    deg_retro[("Ketu", ketu_sign)] = (ketu_deg_in_sign, True)
    return deg_retro
