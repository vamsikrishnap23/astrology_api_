import swisseph as swe
from app.core.calculations import get_rasi, get_nakshatra, get_pada
from app.core.constants import TELUGU_PLANETS, TELUGU_SIGNS, TELUGU_NAKSHATRAS, PLANETS_ORDER

def deg_to_dms_string(degrees):
    d = int(degrees)
    m = int((degrees - d) * 60)
    s = int(round((degrees - d) * 60 % 1 * 60))
    return f"{d}:{m}:{s}"

KP_LORD_SEQUENCE = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]

def kp_lord_chain(longitude):
    nak_idx = int(longitude // (360 / 27))
    pada_idx = int((longitude % (360 / 27)) // (360 / 108))
    star_lord = KP_LORD_SEQUENCE[nak_idx // 3]
    sub_lord = KP_LORD_SEQUENCE[(KP_LORD_SEQUENCE.index(star_lord) + pada_idx) % 9]
    ss_lord = KP_LORD_SEQUENCE[(KP_LORD_SEQUENCE.index(sub_lord) + pada_idx) % 9]
    sss_lord = KP_LORD_SEQUENCE[(KP_LORD_SEQUENCE.index(ss_lord) + pada_idx) % 9]
    return star_lord, sub_lord, ss_lord, sss_lord

def find_house_num(cusps, long_deg):
    """
    Safely returns the 1-based house number for a longitude.
    For i=12 (last house), next_cusp wraps to house 1 + 360.
    """
    for i in range(1, 13):
        this_cusp = cusps[i]
        if i < 12:
            next_cusp = cusps[i+1]
        else:
            next_cusp = cusps[1] + 360  # Wrap for the last house

        if next_cusp < this_cusp:
            next_cusp += 360
        if this_cusp <= long_deg < next_cusp:
            return i
        # Catch the edge case of 360 == 0 at zodiac start
        if i == 12 and long_deg == (next_cusp % 360):
            return 12
    return 1  # fallback, should never hit


def get_significators(houses, planets):
    house_sig = {h["House_Id"]: {"A": [], "B": [], "C": [], "D": []} for h in houses}
    planet_sig = {p["Planet"]: {"A": [], "B": [], "C": [], "D": []} for p in planets}
    # Dummy logic for demo
    for h in houses:
        house_sig[h["House_Id"]]["A"].append(h["Sign_Lord"])
        house_sig[h["House_Id"]]["B"].append(h["Star_Lord"])
        house_sig[h["House_Id"]]["C"].append(h["Sub_Lord"])
        house_sig[h["House_Id"]]["D"].append(h["SS_Lord"])
    for p in planets:
        planet_sig[p["Planet"]]["A"].append(str(p["House"]))
        planet_sig[p["Planet"]]["B"].append(p["Star_Lord"])
        planet_sig[p["Planet"]]["C"].append(p["Sub_Lord"])
        planet_sig[p["Planet"]]["D"].append(p["SS_Lord"])
    return house_sig, planet_sig

def get_kp_system_full(jd, lat, lon, tz_offset):
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    flag = swe.FLG_SWIEPH | swe.FLG_SIDEREAL
    cusps, ascmc = swe.houses_ex(jd, lat, lon, b'P', flag)
    lagna_long = ascmc[0] % 360
    planet_positions = {}
    for name in PLANETS_ORDER:
        if name == "Ascendant":
            planet_positions[name] = lagna_long
        else:
            swid = getattr(swe, name.upper(), None)
            if swid is not None:
                planet_positions[name] = swe.calc_ut(jd, swid, flag)[0][0] % 360

    houses = []
    for i, cusp in enumerate(cusps[1:], start=1):
        long_deg = cusp % 360
        rasi_num = get_rasi(long_deg)
        nak_num = get_nakshatra(long_deg)
        pada_num = get_pada(long_deg)
        star_lord, sub_lord, ss_lord, sss_lord = kp_lord_chain(long_deg)
        houses.append({
            "House_Id": i,
            "Sign": TELUGU_SIGNS[rasi_num],
            "Position": deg_to_dms_string(long_deg % 30),
            "Star": f"{TELUGU_NAKSHATRAS[nak_num-1]}- {pada_num}",
            "Sign_Lord": TELUGU_PLANETS.get(KP_LORD_SEQUENCE[(rasi_num-1) % 9], KP_LORD_SEQUENCE[(rasi_num-1) % 9]),
            "Star_Lord": TELUGU_PLANETS.get(star_lord, star_lord),
            "Sub_Lord": TELUGU_PLANETS.get(sub_lord, sub_lord),
            "SS_Lord": TELUGU_PLANETS.get(ss_lord, ss_lord),
            "SSS_Lord": TELUGU_PLANETS.get(sss_lord, sss_lord),
        })

    planets = []
    for name in PLANETS_ORDER:
        long_deg = planet_positions.get(name)
        rasi_num = get_rasi(long_deg)
        nak_num = get_nakshatra(long_deg)
        pada_num = get_pada(long_deg)
        star_lord, sub_lord, ss_lord, sss_lord = kp_lord_chain(long_deg)
        house_num = find_house_num(cusps, long_deg)
        planets.append({
            "Planet": TELUGU_PLANETS.get(name, name),
            "Sign": TELUGU_SIGNS[rasi_num],
            "Position": deg_to_dms_string(long_deg % 30),
            "House": house_num,
            "Star": f"{TELUGU_NAKSHATRAS[nak_num-1]} - {pada_num}",
            "Sign_Lord": TELUGU_PLANETS.get(KP_LORD_SEQUENCE[(rasi_num-1) % 9], KP_LORD_SEQUENCE[(rasi_num-1) % 9]),
            "Star_Lord": TELUGU_PLANETS.get(star_lord, star_lord),
            "Sub_Lord": TELUGU_PLANETS.get(sub_lord, sub_lord),
            "SS_Lord": TELUGU_PLANETS.get(ss_lord, ss_lord),
            "SSS_Lord": TELUGU_PLANETS.get(sss_lord, sss_lord),
        })

    house_sig, planet_sig = get_significators(houses, planets)
    return {
        "houses": houses,
        "planets": planets,
        "house_significators": house_sig,
        "planet_significators": planet_sig
    }
