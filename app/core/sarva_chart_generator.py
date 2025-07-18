# app/core/sarva_chart_generator.py

# Telugu short names for Rasi (signs) - Aries to Pisces
TELUGU_SIGN_SHORT = [
    "మే", "వృష", "మిథు", "కర్క", "సింహ", "కన్య", "తుల", "వృశ్చ", "ధను", "మకర", "కుంభ", "మీన"
]

SIGN_NAMES = [
    "Aries", "Taurus", "Gemini", "Cancer",
    "Leo", "Virgo", "Libra", "Scorpio",
    "Saggitarius", "Capricorn", "Aquarius", "Pisces"
]

# Coordinates for the 12 Rasi boxes (custom South Indian chart style)
BOX_COORDS = {
    "aries": (123, 10), "taurus": (243, 10), "gemini": (363, 10), "cancer": (363, 90),
    "leo": (363, 170), "virgo": (363, 250), "libra": (243, 250), "scorpio": (123, 250),
    "saggitarius": (3, 250), "capricorn": (3, 170), "aquarius": (3, 90), "pisces": (3, 10)
}

# Where to print Sarva value for each sign
SARVA_COORDS = {
    "aries":   (180, 55), "taurus":   (300, 55), "gemini": (420, 55), "cancer": (420, 135),
    "leo":     (420, 215), "virgo":   (420, 295), "libra": (300, 295), "scorpio": (180, 295),
    "saggitarius": (60, 295), "capricorn": (60, 215), "aquarius": (60, 135), "pisces": (60, 55)
}

def draw_south_chart_with_sarva(sarva_dict):
    svg = []
    svg.append('<?xml version="1.0" encoding="UTF-8"?>')
    svg.append('<svg width="540" height="360" viewBox="0 0 540 360" xmlns="http://www.w3.org/2000/svg">')

    # Draw 12 sign rectangles (no outer boundary)
    for idx, sign in enumerate(SIGN_NAMES):
        lower = sign.lower()
        x, y = BOX_COORDS[lower]
        # Individual house box
        svg.append(f'<rect x="{x}" y="{y}" width="120" height="80" fill="none" stroke="black" stroke-width="2"/>')
        # Telugu short name in each box (top left)
        svg.append(f'<text x="{x+10}" y="{y+25}" font-size="18" fill="#546e7a">{TELUGU_SIGN_SHORT[idx]}</text>')
    # Draw Sarva value in each sign box (centered)
    for idx, sign in enumerate(SIGN_NAMES):
        lower = sign.lower()
        val = sarva_dict.get(sign, "")
        x, y = SARVA_COORDS[lower]
        svg.append(f'<text x="{x}" y="{y}" font-size="32" fill="black" text-anchor="middle" alignment-baseline="middle">{val}</text>')
    svg.append("</svg>")
    return '\n'.join(svg)
