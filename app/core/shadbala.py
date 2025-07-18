import swisseph as swe
import math
from app.core.calculations import get_julian_day

# === Classical Constants ===
PLANET_ORDER = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']
EXALTATION = dict(Sun=10, Moon=33, Mars=298, Mercury=165, Jupiter=95, Venus=357, Saturn=200)
REQUIRED_SHADBALA = dict(Sun=390, Moon=360, Mars=300, Mercury=420, Jupiter=390, Venus=330, Saturn=300)
NAISARGIKA_BALA = dict(Sun=60, Moon=51, Venus=43, Jupiter=34, Mercury=26, Mars=17, Saturn=9)
CIRCULATION_YEARS = dict(Sun=1, Moon=0.082, Mercury=0.24, Venus=0.62, Mars=1.88, Jupiter=11.86, Saturn=29.46)

# === Utility Routines ===
def deg_norm(deg): return deg % 360

def varga_sign(plon, varga_div):
    if varga_div == 1:
        return int(plon // 30) + 1
    elif varga_div == 2:
        z = int(plon // 30)
        return 1 if ((z % 2 == 0 and (plon % 30) < 15) or (z % 2 == 1 and (plon % 30) >= 15)) else 2
    elif varga_div == 3:
        return int((plon % 30) // 10) + 1
    elif varga_div == 9:
        return int((plon % 30) // (30.0 / 9)) + 1
    elif varga_div == 7:
        return int((plon % 30) // (30.0 / 7)) + 1
    elif varga_div == 12:
        return int((plon % 30) // (30.0 / 12)) + 1
    elif varga_div == 30:
        part = plon % 30
        if part < 5: return 1
        elif part < 10: return 2
        elif part < 18: return 3
        elif part < 25: return 4
        else: return 5
    else:
        raise NotImplementedError

def planet_distance(lon1, lon2):
    d = abs(lon1 - lon2) % 360
    return d if d <= 180 else 360 - d

def is_day_birth(sun_long, asc_long):
    # Sun above horizon at birth = day birth
    sun_az = (sun_long - asc_long) % 360
    return sun_az < 180

def weekday(jd):
    # Returns 0=Sunday ... 6=Saturday
    return int(jd + 2) % 7

def get_varsha_lord(jd):
    lords = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']
    return lords[weekday(jd) % 7]

def get_masa_lord(month):
    lords = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']
    return lords[(month - 1) % 7]

def get_dina_lord(jd):
    lords = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']
    return lords[weekday(jd) % 7]

def get_hora_lord(jd, hour):
    # Cycle lords starting from weekday lord, each hora 1 hour after sunrise
    lords = ['Sun', 'Venus', 'Mercury', 'Moon', 'Saturn', 'Jupiter', 'Mars']
    weekday_idx = weekday(jd) % 7
    return lords[(weekday_idx + int(hour)) % 7]

def get_sunrise(year, month, day, lat, lon, tz_offset):
    jd = swe.julday(year, month, day, 0) - tz_offset / 24.0
    # All args positional, types: float, int, float, float, int
    srise = swe.rise_trans(jd, swe.SUN, float(lon), float(lat), int(swe.CALC_RISE | swe.BIT_DISC_CENTER))[1][0]
    return srise

def get_sunset(year, month, day, lat, lon, tz_offset):
    jd = swe.julday(year, month, day, 0) - tz_offset / 24.0
    sset = swe.rise_trans(jd, swe.SUN, float(lon), float(lat), int(swe.CALC_SET | swe.BIT_DISC_CENTER))[1][0]
    return sset

# === Shadbala Component Calculations ===
def compute_uchcha_bala(plon, planet):
    a = abs(EXALTATION[planet] - plon - 180) % 360
    if a > 180: a = 360 - a
    return a / 3

def compute_saptavargaja_bala(var_signs):
    return sum(20 if s == 1 else 0 for s in var_signs)

def compute_ojayugma_bala(planet, rasi, navamsa):
    b = 0
    if planet in ['Venus', 'Moon']:
        if rasi % 2 == 1: b += 15
        if navamsa % 2 == 1: b += 15
    else:
        if rasi % 2 == 0: b += 15
        if navamsa % 2 == 0: b += 15
    return b

def compute_kendradi_bala(rasi):
    t = (rasi-1) % 3
    return 60 if t == 0 else (30 if t == 1 else 15)

def compute_drekkana_bala(planet, plon):
    drekkana = int((plon % 30) // 10)
    if planet in ['Sun','Mars','Jupiter'] and drekkana == 0: return 15
    if planet in ['Venus','Moon'] and drekkana == 1: return 15
    if planet in ['Saturn','Mercury'] and drekkana == 2: return 15
    return 0

def compute_dig_bala(house, planet):
    best = dict(Sun=10, Mars=10, Jupiter=1, Mercury=1, Moon=4, Venus=4, Saturn=7)
    diff = (house - best[planet]) % 12
    diff = diff if diff <=6 else 12-diff
    return 60 - diff*10

def compute_nathonnata_bala(planet, is_day_birth):
    if planet == 'Mercury':
        return 60
    elif planet in ['Moon', 'Mars', 'Saturn']:
        return 60 if not is_day_birth else 0
    elif planet in ['Sun', 'Jupiter', 'Venus']:
        return 60 if is_day_birth else 0
    return 0

def compute_paksha_bala(moon_long, sun_long, planet):
    diff = planet_distance(sun_long, moon_long)
    if planet in ['Sun', 'Mars', 'Saturn']:
        return 60 - diff/3.0
    elif planet in ['Moon', 'Mercury', 'Jupiter', 'Venus']:
        return diff / 3.0
    else:
        return 0

def compute_tribhaga_bala(planet, jd, sunrise, sunset):
    if not sunrise or not sunset: return 0
    if planet == 'Jupiter': return 60
    day = sunrise < jd < sunset
    if day:
        d = (jd - sunrise) / (sunset - sunrise)
        part = int(d * 3)
        if planet == 'Mercury' and part == 0: return 60
        if planet == 'Sun' and part == 1: return 60
        if planet == 'Saturn' and part == 2: return 60
    else:
        d = (jd - sunset) / (sunrise - sunset)
        part = int(d * 3)
        if planet == 'Moon' and part == 0: return 60
        if planet == 'Venus' and part == 1: return 60
        if planet == 'Mars' and part == 2: return 60
    return 0

def compute_varsha_masa_dina_hora_bala(planet, varsha_lord, masa_lord, dina_lord, hora_lord):
    b = 0
    if planet == varsha_lord: b += 15
    if planet == masa_lord: b += 30
    if planet == dina_lord: b += 45
    if planet == hora_lord: b += 60
    return b

def compute_ayana_bala(planet, tropical_long, latitude, ayanamsa):
    kranti = latitude + ayanamsa * math.sin(math.radians(tropical_long))
    if planet == 'Mercury': val = ayanamsa + abs(kranti)
    elif planet in ['Moon', 'Saturn']: val = ayanamsa - kranti
    else: val = ayanamsa + kranti
    return max(val * 1.2793, 0)

def compute_cheshta_bala(planet, speed):
    circulation = CIRCULATION_YEARS[planet]
    mean_speed = 1.0 / circulation if circulation else 1.0
    perc = 100. * speed / mean_speed if mean_speed else 0
    if speed < 0: return 60
    elif perc < 10: return 15
    elif perc < 50: return 15
    elif perc < 100: return 30
    elif perc < 150: return 7.5
    elif perc >= 150: return 45
    return 30

def compute_drik_bala(planet_idx, longitudes):
    drik_sum = 0.0
    PLANET_NAMES = PLANET_ORDER
    plon = longitudes[planet_idx]
    for jdx, other in enumerate(PLANET_NAMES):
        if jdx == planet_idx: continue
        olon = longitudes[jdx]
        rasidiff = int(((olon-plon+360)%360)//30) + 1
        v = 0
        # Classical aspects
        if rasidiff == 7: v = 60
        if PLANET_NAMES[planet_idx] == 'Jupiter' and rasidiff in [5,9]: v = 60
        if PLANET_NAMES[planet_idx] == 'Mars' and rasidiff in [4,8]: v = 60
        if PLANET_NAMES[planet_idx] == 'Saturn' and rasidiff in [3,10]: v = 60
        malefics = ['Sun','Mars','Saturn']
        benefics = ['Moon','Mercury','Jupiter','Venus']
        if other in malefics: v -= 15
        if other in benefics: v += 15
        drik_sum += v
    return drik_sum

def compute_shadbala(year, month, day, hour, minute, second, lat, lon, tz_offset):
    jd = get_julian_day(year, month, day, hour, minute, second, tz_offset)
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    flag = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED
    positions, speeds = {}, {}

    for pname in PLANET_ORDER:
        idx = getattr(swe, pname.upper())
        pos, _ = swe.calc_ut(jd, idx, flag)
        positions[pname], speeds[pname] = pos[0] % 360, pos[3]

    sun_long = positions['Sun']
    moon_long = positions['Moon']
    asc = swe.houses(jd, lat, lon)[0][0] % 360

    # Compute true ayanamsa for this JD (Lahiri)
    ayanamsa = swe.get_ayanamsa(jd)

    # Accurate sunrise/sunset
    sunrise = get_sunrise(year, month, day, lat, lon, tz_offset)
    sunset = get_sunset(year, month, day, lat, lon, tz_offset)
    day_birth = is_day_birth(sun_long, asc)

    # Lords for varsha/masa/dina/hora
    varsha_lord = get_varsha_lord(jd)
    masa_lord = get_masa_lord(month)
    dina_lord = get_dina_lord(jd)
    hora_lord = get_hora_lord(jd, hour)
    
    balas = []
    for idx, pname in enumerate(PLANET_ORDER):
        plon = positions[pname]
        speed = speeds[pname]
        house = int(((plon - asc) % 360) // 30) + 1
        navamsa = varga_sign(plon, 9)
        drekkana = varga_sign(plon, 3)
        saptamsa = varga_sign(plon, 7)
        dwadasamsa = varga_sign(plon, 12)
        trimsamsa = varga_sign(plon, 30)
        var_signs = [navamsa, drekkana, saptamsa, dwadasamsa, trimsamsa]
        rasi = varga_sign(plon, 1)
        uchcha = compute_uchcha_bala(plon, pname)
        saptavargaja = compute_saptavargaja_bala(var_signs)
        oja_yugma = compute_ojayugma_bala(pname, rasi, navamsa)
        kendradi = compute_kendradi_bala(rasi)
        drekkana_val = compute_drekkana_bala(pname, plon)
        sthana = uchcha + saptavargaja + oja_yugma + kendradi + drekkana_val
        dig = compute_dig_bala(house, pname)
        nathonnata = compute_nathonnata_bala(pname, day_birth)
        pkb = compute_paksha_bala(moon_long, sun_long, pname)
        tribhaga = compute_tribhaga_bala(pname, jd, sunrise, sunset)
        vmdh = compute_varsha_masa_dina_hora_bala(pname, varsha_lord, masa_lord, dina_lord, hora_lord)
        ayana = compute_ayana_bala(pname, plon, lat, ayanamsa)
        yuddha = 0  # Not implemented (dueling planets)
        kala = nathonnata + pkb + tribhaga + vmdh + ayana + yuddha
        cheshta = compute_cheshta_bala(pname, speed)
        naisargika = NAISARGIKA_BALA[pname]
        drik = compute_drik_bala(idx, [positions[p] for p in PLANET_ORDER])
        total = sthana + dig + kala + cheshta + naisargika + drik
        req = REQUIRED_SHADBALA[pname]
        percent = total/req * 100
        balas.append({
            "planet": pname,
            "min_required": req,
            "total": total,
            "percent": percent,
            "sthana": {
                'value': sthana,
                'uchcha': uchcha,
                'saptavargaja': saptavargaja,
                'oja-yugma': oja_yugma,
                'kendradi': kendradi,
                'drekkana': drekkana_val
            },
            "dig": { "value": dig },
            "kala": {
                "value": kala,
                "nathonnata": nathonnata,
                "paksha": pkb,
                "tribhaga": tribhaga,
                "varsha-masa-dina-hora": vmdh,
                "ayana": ayana,
                "yuddha": yuddha
            },
            "cheshta": {"value": cheshta},
            "naisargika": naisargika,
            "drik": {"value": drik},
            "rupa": total/60,
            "ishta_phala": max(0, min(12, total/req*12)),
            "kashta_phala": max(0, min(12, (req-total)/req*12)),
        })
    # Assign strength ranks
    balas = sorted(balas, key=lambda b: -b['total'])
    for idx, b in enumerate(balas):
        b['rank'] = idx+1
    return {"balas": balas}
