# app/core/south_chart_svg.py

BOX_COORDS = [
    (123, 10), (243, 10), (363, 10), (363, 90), (363, 170), (363, 250),
    (243, 250), (123, 250), (3, 250), (3, 170), (3, 90), (3, 10)
]
RETRO_SYMBOL = "℞"

# Telugu short symbols for all planets
TELUGU_PLANET_SHORT = {
    "Sun":      "సూ",
    "Moon":     "చం",
    "Mars":     "కు",
    "Mercury":  "బు",
    "Jupiter":  "గు",
    "Venus":    "శు",
    "Saturn":   "శ",
    "Rahu":     "రా",
    "Ketu":     "కే",
    "Uranus":   "యు",   # యు = Uranus
    "Neptune":  "నె",   # నె = Neptune
    "Pluto":    "ఫ్లూ",   # పు = Pluto
    "Ascendant": "ల"    # ల = Lagna
}

def draw_south_chart_svg(house_planets):
    """
    house_planets: list of 12 lists, each containing (label, deg, retro) tuples,
                   index 0=Aries, ..., 11=Pisces, counter-clockwise
    """
    svg = []
    svg.append('<?xml version="1.0" encoding="UTF-8"?>')
    svg.append('<svg width="540" height="360" viewBox="0 0 540 360" xmlns="http://www.w3.org/2000/svg">')
    # Draw boxes
    for idx, (x, y) in enumerate(BOX_COORDS):
        svg.append(f'<rect x="{x}" y="{y}" width="120" height="80" fill="none" stroke="black" stroke-width="2"/>')
    # Render planet symbols/deg/retro, stacked, in black
    for idx, (x, y) in enumerate(BOX_COORDS):
        seen = set()
        for pidx, (label, deg, retro) in enumerate(house_planets[idx]):
            # Skip repeated planets in this sign
            dedup_key = (label, deg, retro)
            if dedup_key in seen:
                continue
            seen.add(dedup_key)
            txt = label
            if deg is not None:
                txt += f" {float(deg):.2f}°"
            if retro:
                txt += f" {RETRO_SYMBOL}"
            px = x + 16
            py = y + 36 + 18 * pidx
            svg.append(f'<text x="{px}" y="{py}" font-size="14" fill="black">{txt}</text>')
    svg.append("</svg>")
    return "\n".join(svg)



def draw_transit_chart_svg(natal_data, transit_data):
    """
    Renders a South Indian transit chart SVG.
    - natal_data: List of lists: planets for each sign (black).
    - transit_data: List of lists: planets for each sign (blue).
    Adds a center legend explaining the two colors.
    """
    svg = []
    svg.append('<?xml version="1.0" encoding="UTF-8"?>')
    svg.append('<svg width="540" height="360" viewBox="0 0 540 360" xmlns="http://www.w3.org/2000/svg">')
    # House boxes
    for idx, (x, y) in enumerate(BOX_COORDS):
        svg.append(f'<rect x="{x}" y="{y}" width="120" height="80" fill="none" stroke="black" stroke-width="2"/>')
    # Natal chart planets (black)
    for idx, (x, y) in enumerate(BOX_COORDS):
        for pidx, (label, deg, retro) in enumerate(natal_data[idx]):
            txt = label
            if deg is not None:
                txt += f" {float(deg):.2f}°"
            if retro:
                txt += f" {RETRO_SYMBOL}"
            px = x + 18
            py = y + 35 + 15 * pidx
            svg.append(f'<text x="{px}" y="{py}" font-size="13" fill="black">{txt}</text>')
        # Space for transit
        natal_len = len(natal_data[idx])
        for t_pidx, (t_label, t_deg, t_retro) in enumerate(transit_data[idx]):
            t_txt = t_label
            if t_deg is not None:
                t_txt += f" {float(t_deg):.2f}°"
            if t_retro:
                t_txt += f" {RETRO_SYMBOL}"
            t_px = x + 18
            t_py = y + 35 + 15 * (natal_len + 1 + t_pidx)
            svg.append(f'<text x="{t_px}" y="{t_py}" font-size="13" fill="#1976d2">{t_txt}</text>')
    # Legend in the middle
    legend_x = 240
    legend_y = 160
    svg.append(
        f'<rect x="{legend_x}" y="{legend_y}" width="60" height="40" fill="white" stroke="black" stroke-width="1"/>'
    )
    svg.append(
        f'<text x="{legend_x+6}" y="{legend_y+17}" font-size="13" fill="black">●</text><text x="{legend_x+30}" y="{legend_y+17}" font-size="13" fill="black">Natal</text>'
    )
    svg.append(
        f'<text x="{legend_x+6}" y="{legend_y+33}" font-size="13" fill="#1976d2">●</text><text x="{legend_x+30}" y="{legend_y+33}" font-size="13" fill="#1976d2">Transit</text>'
    )
    svg.append('</svg>')
    return "\n".join(svg)
