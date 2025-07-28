from datetime import datetime
from app.core.transit_chart import transit_chart
from app.core.constants import TELUGU_PLANET_SHORT, TELUGU_SIGNS

def get_transit_chart_svg(params):
    dt = datetime(params.year, params.month, params.day,
                  params.hour, params.minute, params.second)
    lat, lon, tz = params.lat, params.lon, params.tz_offset

    chart = transit_chart(dt, lat, lon, tz)
    house_data = [[] for _ in range(12)]  # 12 rasis

    for planet, info in chart.items():
        label = TELUGU_PLANET_SHORT.get(planet, planet)
        # Find sign_num by TELUGU_SIGNS value (never use .items() on a list)
        sign_num = None
        for i in range(1, 13):
            if TELUGU_SIGNS[i] == info['rasi']:
                sign_num = i
                break
        if sign_num is None:
            continue
        deg = info.get('deg_in_rasi')
        retro = info.get('vakragathi', 'సామన్య') == 'వక్ర'
        house_data[sign_num-1].append((label, deg, retro))

    # SVG generation
    from app.core.south_chart_svg import draw_south_chart_svg
    svg = draw_south_chart_svg(house_data)
    return {"svg": svg}
