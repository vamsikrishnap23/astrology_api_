from datetime import datetime
from app.core.transit_chart import transit_chart

# Telugu short symbols (as used everywhere in your files)
TELUGU_PLANET_SHORT = {
    "Sun": "సూ", "Moon": "చం", "Mars": "కు", "Mercury": "బు",
    "Jupiter": "గు", "Venus": "శు", "Saturn": "శ",
    "Uranus": "యు", "Neptune": "నె", "Pluto": "పు",
    "Rahu": "రా", "Ketu": "కే", "Ascendant": "ల"
}

def get_transit_chart_svg(params):
    # Build datetime
    dt = datetime(
        params.year, params.month, params.day,
        params.hour, params.minute, params.second
    )
    lat, lon, tz = params.lat, params.lon, params.tz_offset

    # Maitreya-logic: get all planets in their signs, including degree and retro!
    chart = transit_chart(dt, lat, lon, tz)

    # Prepare house-wise array (12 signs) for SVG
    # Each entry: [ (label, deg, retro), ... ]
    house_data = [[] for _ in range(12)]
    for planet, info in chart.items():
        label = TELUGU_PLANET_SHORT.get(planet, planet)
        sign_num = None
        if 'sign' in info:
            # Use sign name to number, but easier: match against constants or use a reverse map
            from app.core.constants import SIGN_NAMES
            for k, v in SIGN_NAMES.items():
                if v == info['sign']:
                    sign_num = k
                    break
        if sign_num is None:
            continue
        deg = info.get('deg_in_sign')
        retro = info.get('retrograde', False)
        # lagna, planets, rahu, ketu all included
        house_data[sign_num-1].append((label, deg, retro))

    from app.core.south_chart_svg import draw_south_chart_svg
    svg = draw_south_chart_svg(house_data)
    return {"svg": svg}
