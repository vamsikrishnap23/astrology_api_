import swisseph as swe
from app.core.ashtakootam import ashtakootam_full
from app.core.calculations import get_julian_day
from app.core.constants import PLANETS

def get_moon_longitude_and_jd(year, month, day, hour, minute, second, lat, lon, tz_offset):
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    jd = get_julian_day(year, month, day, hour, minute, second, tz_offset)
    flag = swe.FLG_SWIEPH | swe.FLG_SIDEREAL
    moon_long, _ = swe.calc_ut(jd, PLANETS['Moon'], flag)
    return moon_long[0] % 360, jd

def get_ashtakootam_data(params):
    # Bride: get Moon longitude (sidereal) and JD
    bride_moon_long, bride_jd = get_moon_longitude_and_jd(
        params.bride_year, params.bride_month, params.bride_day,
        params.bride_hour, params.bride_minute, params.bride_second,
        params.bride_lat, params.bride_lon, params.bride_tz_offset
    )
    # Groom: get Moon longitude (sidereal) and JD
    groom_moon_long, groom_jd = get_moon_longitude_and_jd(
        params.groom_year, params.groom_month, params.groom_day,
        params.groom_hour, params.groom_minute, params.groom_second,
        params.groom_lat, params.groom_lon, params.groom_tz_offset
    )
    # Run Maitreya-style Ashtakoota logic
    koota_result = ashtakootam_full(bride_moon_long, groom_moon_long, bride_jd, groom_jd)
    return {"koota": koota_result}
