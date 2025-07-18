from datetime import datetime
from app.core.progression_chart import progression_chart
from app.core.constants import TELUGU_PLANET_SHORT, SIGN_NAMES
from app.core.south_chart_svg import draw_south_chart_svg

def get_progression_chart_svg(params):
    nat_dt = datetime(params.nat_year, params.nat_month, params.nat_day, params.nat_hour, params.nat_minute, params.nat_second)
    prg_dt = datetime(params.prg_year, params.prg_month, params.prg_day)
    chart = progression_chart(nat_dt, params.nat_lat, params.nat_lon, params.nat_tz_offset, prg_dt)
    house_data = [[] for _ in range(12)]
    for planet, info in chart.items():
        label = TELUGU_PLANET_SHORT.get(planet, planet)
        sign_num = None
        for k, v in SIGN_NAMES.items():
            if info['sign'] == v:
                sign_num = k
                break
        if sign_num is None:
            continue
        deg = info.get('deg_in_sign')
        retro = info.get('retrograde', False)
        house_data[sign_num - 1].append((label, deg, retro))
    svg = draw_south_chart_svg(house_data)
    return {"svg": svg}
