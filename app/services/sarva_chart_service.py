from app.core.chart_logic import compute_planets_in_varga
from app.core.ashtakavarga import Ashtakavarga, REKHA
from app.core.constants import TELUGU_SIGNS
from app.core.sarva_chart_generator import draw_south_chart_with_sarva

def get_sarva_chart_svg(params):
    planets_in_sign = compute_planets_in_varga(
        params.year, params.month, params.day,
        params.hour, params.minute, params.second,
        params.lat, params.lon, params.tz_offset, varga_num=1
    )
    planet_order = ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Ascendant"]
    planet_signs = [None] * 8
    for sign_num, planets in planets_in_sign.items():
        for planet in planets:
            if planet in planet_order:
                idx = planet_order.index(planet)
                planet_signs[idx] = (sign_num - 1) % 12
    for i, val in enumerate(planet_signs):
        if val is None:
            planet_signs[i] = 0
    def get_rasi(idx):
        return planet_signs[idx]
    ashta = Ashtakavarga(get_rasi)
    ashta.update()
    # Sarva calculation (exclude Ascendant)
    sarva = [sum(ashta.getItem(REKHA, pidx, rasi) for pidx in range(7)) for rasi in range(12)]
    # Prepare dict for chart generator by sign name (English)
    sign_names = [
        "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
        "Libra", "Scorpio", "Saggitarius", "Capricorn", "Aquarius", "Pisces"
    ]
    sarva_dict = dict(zip(sign_names, sarva))
    svg = draw_south_chart_with_sarva(sarva_dict)
    return {"svg": svg}
