import jyotichart

from app.core.constants import TELUGU_SIGNS, TELUGU_PLANETS

def create_rasi_chart_svg(planets_in_sign, planet_deg_retro):
    # Prepare data per sign for chart
    chart_data = []
    # The jyotichart South Indian box order (counter-clockwise from Aries)
    sign_order = [1,2,3,4,5,6,7,8,9,10,11,12]
    for sign in sign_order:
        # Telugu label for sign
        sign_label = TELUGU_SIGNS.get(sign, str(sign))
        planets = []
        for planet in planets_in_sign.get(sign, []):
            # Label with deg & retro info
            deg, retro = planet_deg_retro.get((planet, sign), ("--", False))
            label = TELUGU_PLANETS.get(planet, planet)
            if retro:
                planets.append(f"{label} {deg}° (వ)")
            else:
                planets.append(f"{label} {deg}°")
        chart_data.append({
            "sign": sign_label,
            "planets": planets
        })
    # Generate SVG using jyotichart
    svg = jyotichart.draw_south_chart_full(chart_data)
    # If jyotichart returns UTF-16 string, convert to UTF-8 for web compatibility
    if isinstance(svg, bytes):
        svg = svg.decode("utf-8")
    elif "utf-16" in svg[:100].lower():
        svg = svg.encode("utf-16").decode("utf-8", errors="replace")
    return svg
