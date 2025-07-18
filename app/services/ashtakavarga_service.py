from app.core.chart_logic import compute_planets_in_varga
from app.core.ashtakavarga import Ashtakavarga, OSUN, OMOON, OMERCURY, OVENUS, OMARS, OJUPITER, OSATURN, OASCENDANT, REKHA
from app.core.constants import TELUGU_PLANETS, TELUGU_SIGNS

def get_ashtakavarga(params):
    # Get planetary positions in signs for D1 (Rasi)
    planets_in_sign = compute_planets_in_varga(
        params.year, params.month, params.day,
        params.hour, params.minute, params.second,
        params.lat, params.lon, params.tz_offset, varga_num=1
    )

    # Prepare mapping: Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Ascendant
    planet_order = ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Ascendant"]
    planet_signs = [None] * 8
    for sign_num, planets in planets_in_sign.items():
        for planet in planets:
            if planet in planet_order:
                idx = planet_order.index(planet)
                planet_signs[idx] = (sign_num - 1) % 12
    # Fallback: If any planet not found, fill as 0
    for i, val in enumerate(planet_signs):
        if val is None:
            planet_signs[i] = 0

    def get_rasi(idx):
        return planet_signs[idx]
    ashta = Ashtakavarga(get_rasi)
    ashta.update()

    # Prepare table: Telugu labels and rekha points
    telugu_planet_labels = [TELUGU_PLANETS.get(name, name) for name in planet_order]
    telugu_sign_labels = [TELUGU_SIGNS[i + 1] for i in range(12)]
    rekha_table = []
    for pidx, plabel in enumerate(telugu_planet_labels):
        rekhas = [ashta.getItem(REKHA, pidx, rasi) for rasi in range(12)]
        rekha_table.append({"planet": plabel, "rekhas": rekhas})
    # Add Sarva
    sarva = [ashta.getSarva(REKHA, rasi) for rasi in range(12)]
    return {
        "rekha_table": rekha_table,
        "sarva": sarva,
        "labels": {
            "planets": telugu_planet_labels,
            "signs": telugu_sign_labels
        }
    }
