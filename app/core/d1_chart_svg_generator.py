from app.core.constants import TELUGU_SIGNS, TELUGU_PLANETS

# Telugu short symbols for planets (incl. retrograde marker)
PLANET_SYMBOLS = {
    "Sun": "సూ", "Moon": "చం", "Mars": "కు", "Mercury": "బు",
    "Jupiter": "గు", "Venus": "శు", "Saturn": "శ", "Rahu": "రా",
    "Ketu": "కే", "Ascendant": "ల"
}

# Retrograde marker (use a Unicode 'R' for retrograde, or a circle/back arrow)
RETRO_SYMBOL = "℞"

# Chart box coordinates (same as previous South Indian chart)
BOX_COORDS = [
    (123, 10), (243, 10), (363, 10), (363, 90),
    (363, 170), (363, 250), (243, 250), (123, 250),
    (3, 250), (3, 170), (3, 90), (3, 10)
]

def draw_d1_south_chart(planets_in_sign, deg_lookup, retro_lookup):
    svg = []
    svg.append('<?xml version="1.0" encoding="UTF-8"?>')
    svg.append('<svg width="540" height="360" viewBox="0 0 540 360" xmlns="http://www.w3.org/2000/svg">')

    # Draw house boxes and Telugu sign name
    for sign_idx in range(12):
        x, y = BOX_COORDS[sign_idx]
        svg.append(f'<rect x="{x}" y="{y}" width="120" height="80" fill="none" stroke="black" stroke-width="2"/>')
        # Telugu sign name (top left corner)
        svg.append(f'<text x="{x+8}" y="{y+22}" font-size="18" fill="#4B636E">{TELUGU_SIGNS[sign_idx+1]}</text>')
    # Place planets (and ascendant) with degree and retrograde
    for sign_idx in range(12):
        x, y = BOX_COORDS[sign_idx]
        planets = planets_in_sign.get(sign_idx+1, [])
        if not planets:
            continue
        vspace = 26
        for i, planet in enumerate(planets):
            p_x = x + 25 + (i//4)*60
            p_y = y + 40 + (i%4)*vspace
            symbol = PLANET_SYMBOLS.get(planet, planet)
            deg = deg_lookup.get(planet)
            retro = retro_lookup.get(planet, False)

            if deg is None:
                extra = ""
            else:
                try:
                    extra = f"{float(deg):.2f}°"
                except Exception:
                    extra = ""

            label = symbol
            if extra:
                label += f" {extra}"
            if retro:
                label += f" {RETRO_SYMBOL}"

            svg.append(f'<text x="{p_x}" y="{p_y}" font-size="20" fill="#1a237e">{label}</text>')

    svg.append("</svg>")
    return '\n'.join(svg)
