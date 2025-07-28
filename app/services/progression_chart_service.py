from datetime import datetime
from app.core.progression_chart import progression_chart
from app.core.constants import TELUGU_PLANET_SHORT, TELUGU_SIGNS, SIGN_NAMES
from app.core.south_chart_svg import draw_south_chart_svg

def get_progression_chart_svg(params):
    nat_dt = datetime(params.nat_year, params.nat_month, params.nat_day,
                      params.nat_hour, params.nat_minute, params.nat_second)
    prg_dt = datetime(params.prg_year, params.prg_month, params.prg_day)

    chart = progression_chart(nat_dt, params.nat_lat, params.nat_lon, params.nat_tz_offset, prg_dt)

    house_data = [[] for _ in range(12)]  # 12 signs/houses

    for planet, info in chart.items():
        label = TELUGU_PLANET_SHORT.get(planet, planet)
        # Find matching sign_num (1-based) for info['sign']
        sign_num = None
        for idx in range(1, len(SIGN_NAMES)):
            if info['sign'] == SIGN_NAMES[idx]:
                sign_num = idx
                break
        if sign_num is None:
            # fallback: try to use Telugu_SIGN if in Telugu
            for idx in range(1, len(TELUGU_SIGNS)):
                if info['sign'] == TELUGU_SIGNS[idx]:
                    sign_num = idx
                    break
        if sign_num is None:
            continue  # if still not found, skip this planet

        deg = info.get('deg_in_sign')
        retro = info.get('retrograde', False)
        house_data[sign_num - 1].append((label, deg, retro))

    svg = draw_south_chart_svg(house_data)
    return {"svg": svg}
