from app.core.chart_logic import compute_planets_in_varga
from app.core.constants import PLANETS
from app.core.south_chart_svg import draw_south_chart_svg

TELUGU_PLANET_SHORT = {
    "Sun":      "సూ",
    "Moon":     "చం",
    "Mars":     "కు",
    "Mercury":  "బు",
    "Jupiter":  "గు",
    "Venus":    "శు",
    "Saturn":   "శ",
    "Uranus":   "యు",
    "Neptune":  "నె",
    "Pluto":    "ఫ్లూ",
    "Rahu":     "రా",
    "Ketu":     "కే",
    "Ascendant": "ల"
}

def get_planet_degrees_and_retro(year, month, day, hour, minute, second, lat, lon, tz_offset, varga_num):
    import swisseph as swe
    from app.core.calculations import get_julian_day, get_rasi, get_ascendant
    from app.core.chart_logic import get_varga_longitude
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    jd = get_julian_day(year, month, day, hour, minute, second, tz_offset)
    flag = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED

    deg_retro = {}

    # Classical planets + Uranus/Neptune/Pluto
    for planet, pid in PLANETS.items():
        lon_arr, _ = swe.calc_ut(jd, pid, flag)
        longitude = lon_arr[0] % 360
        speed = lon_arr[3]
        varga_long = get_varga_longitude(longitude, varga_num) % 360
        sign = get_rasi(varga_long)
        deg_in_sign = varga_long % 30
        retro = speed < 0
        deg_retro[(planet, sign)] = (deg_in_sign, retro)

    # Rahu and Ketu: explicit calculation for both
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
    # Retrograde must always be True for Ketu
    deg_retro[("Ketu", ketu_sign)] = (ketu_deg_in_sign, True)

    # Lagna (Ascendant)
    asc = get_ascendant(jd, lat, lon) % 360
    varga_long = get_varga_longitude(asc, varga_num) % 360
    sign = get_rasi(varga_long)
    deg_in_sign = varga_long % 30
    deg_retro[("Ascendant", sign)] = (deg_in_sign, False)
    return deg_retro

def get_div_chart_svg(params):
    planets_in_sign = compute_planets_in_varga(
        params.year, params.month, params.day, params.hour, params.minute, params.second,
        params.lat, params.lon, params.tz_offset, params.varga_num
    )
    deg_retro = get_planet_degrees_and_retro(
        params.year, params.month, params.day, params.hour, params.minute, params.second,
        params.lat, params.lon, params.tz_offset, params.varga_num
    )

    house_data = []
    for sign in range(1, 13):
        entries = []
        seen_planets = set()
        for planet in planets_in_sign.get(sign, []):
            if planet not in TELUGU_PLANET_SHORT:
                continue
            # Prevent Rahu/Ketu duplication
            if planet in seen_planets:
                continue
            seen_planets.add(planet)
            label = TELUGU_PLANET_SHORT[planet]
            deg, retro = deg_retro.get((planet, sign), (None, False))
            entries.append((label, deg, retro))
        # Add Lagna if not already present
        if ("Ascendant", sign) in deg_retro and not any(e[0] == TELUGU_PLANET_SHORT["Ascendant"] for e in entries):
            deg, retro = deg_retro[("Ascendant", sign)]
            entries.append((TELUGU_PLANET_SHORT["Ascendant"], deg, retro))
        # Ensure Ketu is shown with degree/retro if not duplicated in sign
        if ("Ketu", sign) in deg_retro and not any(e[0] == TELUGU_PLANET_SHORT["Ketu"] for e in entries):
            deg, retro = deg_retro[("Ketu", sign)]
            entries.append((TELUGU_PLANET_SHORT["Ketu"], deg, retro))
        house_data.append(entries)
    svg = draw_south_chart_svg(house_data)
    return {"svg": svg}
