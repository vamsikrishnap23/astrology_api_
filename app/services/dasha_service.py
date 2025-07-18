from app.core.vimshottari_dashas import compute_vimsottari_dashas
from app.core.constants import TELUGU_PLANETS
from app.core.calculations import get_julian_day
import swisseph as swe

def get_vimshottari_dashas(params):
    jd = get_julian_day(
        params.year, params.month, params.day,
        params.hour, params.minute, params.second, params.tz_offset
    )
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    flag = swe.FLG_SWIEPH | swe.FLG_SIDEREAL
    moon_long = swe.calc_ut(jd, swe.MOON, flag)[0][0] % 360
    # Use use_telugu=False here, do mapping below for full control.
    dashas = compute_vimsottari_dashas(moon_long, jd)
    all_dashas = []
    for maha in dashas:
        # --- Fix: map key and translate to Telugu
        maha_lord = maha.get("lord") or maha.get("mahadasha_lord")
        maha_lord_te = TELUGU_PLANETS.get(maha_lord, maha_lord)
        antars = []
        for antar in maha["antardashas"]:
            antar_lord = antar.get("antardasha_lord") or antar.get("lord")
            antar_lord_te = TELUGU_PLANETS.get(antar_lord, antar_lord)
            antars.append({
                "antardasha_lord": antar_lord_te,
                "start": jd_to_str(antar["start_jd"]),
                "end": jd_to_str(antar["end_jd"])
            })
        all_dashas.append({
            "mahadasha_lord": maha_lord_te,
            "start": jd_to_str(maha["start_jd"]),
            "end": jd_to_str(maha["end_jd"]),
            "antardashas": antars
        })
    return {"dashas": all_dashas}

def jd_to_str(jd):
    import swisseph as swe
    y, m, d, frac = swe.revjul(jd, swe.GREG_CAL)
    total_seconds = int(round(frac * 86400))
    h = total_seconds // 3600
    mi = (total_seconds % 3600) // 60
    s = total_seconds % 60
    return f"{d:02}-{m:02}-{y} {h:02}:{mi:02}:{s:02}"
