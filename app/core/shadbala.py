import swisseph as swe
import math
from app.core.calculations import get_julian_day

# These correspond to: Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn
PLANET18 = [
    ("Sun", swe.SUN, 390, 10),
    ("Moon", swe.MOON, 360, 33),
    ("Mars", swe.MARS, 300, 298),
    ("Mercury", swe.MERCURY, 420, 165),
    ("Jupiter", swe.JUPITER, 390, 95),
    ("Venus", swe.VENUS, 330, 357),
    ("Saturn", swe.SATURN, 300, 200),
]

# These should ideally be imported from your constants
EXALTATION_LONGITUDES = {
    "Sun": 10, "Moon": 33, "Mars": 298, "Mercury": 165,
    "Jupiter": 95, "Venus": 357, "Saturn": 200
}
NAISARGIKA_BALA = {"Sun": 60, "Moon": 51, "Venus": 43, "Jupiter": 34,
                   "Mercury": 26, "Mars": 17, "Saturn": 9}

def degree_distance(a, b):
    d = abs(a - b) % 360
    return d if d <= 180 else 360 - d

def reduce_deg(deg):
    return deg % 360

def get_house(lon, asc):
    # House as (0-11), Aries begins at 0
    h = int(((lon - asc)%360)//30)
    return (h+1) if (1 <= (h+1) <= 12) else ((h)%12+1)

def compute_uchcha_bala(planet_long, name):
    a = abs(reduce_deg(EXALTATION_LONGITUDES[name] - planet_long - 180))
    if a > 180: a = 360 - a
    return a/3.0

def compute_dig_bala(house, name):
    # As per actual rules: each planet has a "best" house
    best = {
        "Sun": 10, "Mars": 10,
        "Moon": 4, "Venus": 4,
        "Mercury": 1, "Jupiter": 1,
        "Saturn": 7,
    }
    diff = abs(house - best[name])
    if diff > 6: diff = 12 - diff
    return 60 - 10 * diff  # 60virupa best, min 0

def compute_paksha_bala(sun_long, moon_long, planet_name, is_moon_benefic=True, is_mer_benefic=True):
    diff = degree_distance(sun_long, moon_long)
    # Only Moon/Mercury "benefic" gets special, else it's inverted
    if planet_name == "Moon":
        return diff/3.0 if is_moon_benefic else (60 - diff/3.0)
    elif planet_name == "Mercury":
        return diff/3.0 if is_mer_benefic else (60 - diff/3.0)
    elif planet_name in ["Sun", "Mars", "Saturn"]:
        return 60 - diff/3.0
    elif planet_name in ["Jupiter", "Venus"]:
        return diff/3.0
    else:
        return 0

def compute_kala_bala(sun_long, moon_long, planet_name, is_day):
    # For brevity: only paksha bala and basic nathonnatha
    nathonnatha = 60 if (planet_name in ["Mercury", "Moon", "Mars", "Saturn"] and not is_day) or (planet_name in ["Sun", "Jupiter", "Venus"] and is_day) else 0
    paksha = compute_paksha_bala(sun_long, moon_long, planet_name)
    return paksha + nathonnatha

def compute_naisargika_bala(planet_name):
    return NAISARGIKA_BALA.get(planet_name, 0)

def compute_cheshta_bala(speed, name):
    # Use circulation time for basis, as per Maitreya
    circulation = {
        "Sun":1, "Moon":0.082, "Mars":1.88, "Mercury":0.24, "Jupiter":11.86, "Venus":0.62, "Saturn":29.46
    }
    medium = 1.0 / circulation[name]
    perc = 100*speed/medium
    if speed < 0:   # Vakra
        return 60
    elif perc >= 150:
        return 45  # Chara
    elif perc >= 100:
        return 30  # Sama
    elif perc >= 50:
        return 15  # Manda
    elif abs(perc) < 10:
        return 7.5 # Vikala
    else:
        return 15

def compute_drik_bala(planet_idx, longitudes, malefics, is_benefic):
    # Sum graha drishti; simple: + if benefic, - if malefic
    total = 0.0
    for jdx, lon in enumerate(longitudes):
        if planet_idx == jdx:
            continue
        diff = int(abs(longitudes[jdx] - longitudes[planet_idx]) // 30) + 1  # Rasi diff 1-12
        value = 0
        # Standard 7 planets
        # Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn (0-6)
        name = PLANET18[jdx][0]
        # Aspects per classical rules - 100% on opposing, partial elsewhere
        if diff == 7:
            value = 60.0
        elif diff == 4 and name in ("Jupiter"):
            value = 60.0
        elif diff in (3,8) and name in ("Mars"):
            value = 60.0
        elif diff in (2,12) and name in ("Saturn"):
            value = 60.0

        if name in malefics and value > 0:
            value -= 15.0
        if is_benefic(name) and value > 0:
            value += 15.0
        total += value
    return total

def compute_shadbala(year, month, day, hour, minute, second, lat, lon, tz_offset):
    jd = get_julian_day(year, month, day, hour, minute, second, tz_offset)
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    flag = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED

    planets_long = []
    planets_speed = []
    house1 = None

    for i, (name, pid, required, exalt) in enumerate(PLANET18):
        pos, _ = swe.calc_ut(jd, pid, flag)
        planets_long.append(pos[0] % 360)
        planets_speed.append(pos[3])

    # Ascendant (to assign houses)
    asc = swe.houses(jd, lat, lon.decode() if isinstance(lon, bytes) else lon)[0][0] % 360

    sun_long = planets_long[0]
    moon_long = planets_long[1]
    malefics = {'Sun', 'Mars', 'Saturn'}

    def is_benefic(name):
        # Simplified, user can extend with detailed rules
        return name in {"Moon", "Mercury", "Jupiter", "Venus"}

    is_day = True
    if sun_long and asc:
        diff = (asc - sun_long) % 360
        is_day = diff < 180

    results = []
    for idx, (name, pid, required, exalt) in enumerate(PLANET18):
        plon = planets_long[idx]
        house = get_house(plon, asc)
        speed = planets_speed[idx]

        sthana = compute_uchcha_bala(plon, name)
        dig = compute_dig_bala(house, name)
        kala = compute_kala_bala(sun_long, moon_long, name, is_day)
        cheshta = compute_cheshta_bala(speed, name)
        naisargika = compute_naisargika_bala(name)
        drik = compute_drik_bala(idx, planets_long, malefics, is_benefic)

        total = sthana + dig + kala + cheshta + naisargika + drik
        percent = 100.0 * total / required if required else 0.0

        results.append({
            "name": name,
            "sthana": round(sthana, 2),
            "dig": round(dig, 2),
            "kala": round(kala, 2),
            "cheshta": round(cheshta, 2),
            "naisargika": round(naisargika, 2),
            "drik": round(drik, 2),
            "total": round(total, 2),
            "percent": round(percent, 2),
            "required": required
        })
    return {"planets": results}
