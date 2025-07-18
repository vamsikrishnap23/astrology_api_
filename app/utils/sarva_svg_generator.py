# This function generates a South Indian chart SVG with Sarva values per house
def draw_south_chart_with_sarva(sarva_list):
    # The order of signs is: Aries, Taurus, Gemini, ... Pisces
    # Lay them out according to South Indian chart geometry
    import svgwrite
    size = 400
    dwg = svgwrite.Drawing(size=(size, size))
    # Draw outer border
    dwg.add(dwg.rect(insert=(0,0), size=(size, size), fill='white', stroke='black', stroke_width=3))
    # Coordinates for the 12 boxes (simple arrangement)
    box_coords = [
        (10,10), (140,10), (270,10),
        (270,140), (270,270), (140,270), (10,270), (10,140),
        (75,75), (205,75), (205,205), (75,205)
    ]
    # The house positions (per South Indian chart counter-clockwise from top-left)
    house_order = [0,1,2,3,4,5,6,7,8,9,10,11]
    for i, (x,y) in enumerate(box_coords):
        s = sarva_list[i] if i < len(sarva_list) else ""
        dwg.add(dwg.rect(insert=(x,y), size=(120,120), fill='none', stroke='black', stroke_width=2))
        dwg.add(dwg.text(str(s), insert=(x+60, y+65), text_anchor="middle", font_size="32px", fill="#1a237e"))
    return dwg.tostring()
