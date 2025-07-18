# app/core/ashtakootam.py

from app.core.constants import SIGN_NAMES, NAKSHATRA_NAMES, TELUGU_SIGNS, TELUGU_NAKSHATRAS, TELUGU_VAARAM
from app.core.calculations import get_rasi, get_nakshatra, get_pada
import datetime

VARNA_NAMES = ["Shudra", "Vaishya", "Kshatriya", "Brahmin"]
VARNA_TELUGU = ["శూద్రుడు", "వైశ్యుడు", "క్షత్రియుడు", "బ్రాహ్మణుడు"]
VASHYA_NAMES = ["Quadruped", "Human", "Jalachara", "Leo", "Scorpio"]
VASHYA_TELUGU = ["చతుష్పాదం", "మానవం", "జలచరం", "సింహం", "వృశ్చికం"]
GANA_NAMES = ["Deva", "Manushya", "Rakshasa"]
GANA_TELUGU = ["దేవ", "మానవ", "రాక్షస"]
NADI_NAMES = ["Adi", "Madhya", "Antya"]
NADI_TELUGU = ["ఆది", "మధ్య", "అంత్య"]
YONI_NAMES = [
    "గుఱ్ఱం", "ఎద్దు", "సింహం", "ఏనుగు", "మేక", "కొంగ", "మంగూస్",
    "పాము", "జింక", "కుక్క", "పిల్లి", "ఎలుక", "పులి", "ఆవు"
]

YONI_MAP_28 = [0, 3, 4, 7, 7, 9, 10, 4, 10, 11, 11, 13, 1, 12, 1, 12, 8, 8, 9, 5, 6, 6, 5, 2, 0, 2, 13, 3]
GANA_NAKSHATRA_MAP = [0, 1, 2, 1, 0, 1, 0, 0, 2, 2, 1, 1, 0, 2, 0, 2, 0, 2, 2, 1, 1, 0, 2, 2, 1, 1, 0]
GANA_MAP = [
    [6, 5, 1],
    [6, 6, 0],
    [0, 0, 6]
]
NADI_MAP = [
    0, 1, 2, 2, 1, 0, 0, 1, 2,
    2, 1, 0, 0, 1, 2, 2, 1, 0,
    0, 1, 2, 2, 1, 0, 0, 1, 2
]
YONI_SCORE_MATRIX = [
    [4, 0, 1, 2, 3, 2, 2, 1, 3, 2, 3, 3, 1, 3],
    [0, 4, 1, 2, 3, 2, 2, 2, 3, 2, 2, 2, 1, 3],
    [1, 1, 4, 0, 1, 2, 2, 2, 1, 1, 2, 1, 2, 1],
    [2, 3, 0, 4, 2, 2, 2, 2, 2, 2, 3, 2, 1, 2],
    [3, 3, 1, 2, 4, 0, 3, 1, 3, 2, 3, 2, 1, 3],
    [2, 2, 2, 2, 0, 4, 2, 1, 2, 2, 2, 2, 1, 2],
    [2, 2, 2, 2, 3, 2, 4, 0, 2, 1, 2, 2, 2, 2],
    [1, 2, 2, 2, 1, 1, 0, 4, 1, 1, 1, 1, 2, 1],
    [3, 2, 1, 2, 3, 2, 2, 1, 4, 0, 2, 2, 1, 2],
    [2, 2, 1, 2, 2, 2, 1, 1, 0, 4, 1, 1, 1, 1],
    [3, 2, 2, 3, 3, 2, 2, 1, 2, 1, 4, 0, 2, 2],
    [3, 2, 1, 2, 2, 2, 2, 1, 2, 1, 0, 4, 2, 2],
    [1, 1, 2, 1, 1, 1, 2, 2, 1, 1, 2, 2, 4, 0],
    [3, 3, 1, 2, 3, 2, 2, 1, 2, 1, 2, 2, 0, 4]
]
VASHYA_MAP = [
    [2, 1, 0.5, 0, 1],
    [0, 2, 1, 0, 1],
    [0, 1, 2, 0, 1],
    [0.5, 0.5, 1, 2, 0],
    [0, 1, 1, 0, 2]
]
BHAKOOTA_GOOD_DIFFS = {0, 3, 4, 7, 10, 11}

PLANET_FRIENDSHIP = [
    [1, 1, 0, -1, 1, 1, -1], # Sun
    [1, 1, 1, 0, 0, 0, 0],   # Moon
    [1, -1, 1, 1, 0, 0, 0],  # Mars
    [-1, -1, 1, 1, 0, 0, 1], # Mercury
    [1, 1, -1, 0, 1, 1, 0],  # Jupiter
    [1, 1, -1, -1, 1, 1, 0], # Venus
    [-1, -1, 1, 1, -1, 0, 1] # Saturn
]
FRIEND, NEUTRAL, ENEMY = 1, 0, -1

def get_rasi_py(longitude):
    return int(longitude // 30) + 1  # 1-based

def get_nakshatra27(longitude):
    return int((longitude % 360) // (360 / 27))

def get_varna(longitude):
    v = get_rasi_py(longitude) % 4
    if v == 0: return 2  # Kshatriya
    if v == 1: return 1  # Vaishya
    if v == 2: return 0  # Shudra
    if v == 3: return 3  # Brahmin

def get_vashya(longitude):
    rasi = get_rasi_py(longitude)
    deg_in_sign = longitude % 30
    if rasi in [1, 2]: return 0  # Quadruped
    elif rasi in [3, 6, 7, 11]: return 1  # Human
    elif rasi in [4, 12]: return 2  # Jalachara
    elif rasi == 5: return 3  # Leo
    elif rasi == 8: return 4  # Scorpio
    elif rasi == 9: return 1 if deg_in_sign < 15 else 0
    elif rasi == 10: return 0 if deg_in_sign < 15 else 2

def get_yoni(longitude):
    nakshatra = int((longitude % 360) // (360 / 28))
    yoni_id = YONI_MAP_28[nakshatra]
    return yoni_id, YONI_NAMES[yoni_id]

def get_gana(longitude):
    nakshatra = get_nakshatra27(longitude)
    gana = GANA_NAKSHATRA_MAP[nakshatra]
    return gana, GANA_NAMES[gana]

def get_nadi(longitude):
    nakshatra = get_nakshatra27(longitude)
    nadi = NADI_MAP[nakshatra]
    return nadi, NADI_NAMES[nadi]

def get_tara(nak1, nak2):
    dnak1 = (nak2 - nak1)
    if dnak1 < 0: dnak1 += 27
    dnak1 += 1
    tara1 = dnak1 % 9
    dnak2 = (nak1 - nak2)
    if dnak2 < 0: dnak2 += 27
    dnak2 += 1
    tara2 = dnak2 % 9
    return tara1, tara2

def get_rajju(nakshatra):
    n1 = nakshatra % 9
    if n1 < 4:
        return 0, n1 # Aroha
    elif n1 == 4:
        return 1, 4 # Siro
    elif n1 > 4 and n1 < 9:
        return 2, 8 - n1 # Avaroha

def calc_rajju_score(rajju1, rajju2):
    aroha1, type1 = rajju1
    aroha2, type2 = rajju2
    if type1 != type2:
        if aroha1 == 0 and aroha2 == 0: return 4
        elif aroha1 != 2 or aroha2 != 2: return 3
        elif aroha1 != aroha2: return 2
        elif aroha1 == 2 and aroha2 == 2: return 1
    elif type1 == type2: return 0

def get_lord(rasi):
    if rasi == 1 or rasi == 8: return 2  # Mars
    elif rasi == 2 or rasi == 7: return 5  # Venus
    elif rasi == 3 or rasi == 6: return 3  # Mercury
    elif rasi == 4: return 1  # Moon
    elif rasi == 5: return 0  # Sun
    elif rasi == 9 or rasi == 12: return 4  # Jupiter
    elif rasi == 10 or rasi == 11: return 6  # Saturn

def get_planetary_friendship(lord1, lord2):
    return PLANET_FRIENDSHIP[lord1][lord2]

def calc_maitri_score(lord1, lord2):
    mitra1 = get_planetary_friendship(lord1, lord2)
    mitra2 = get_planetary_friendship(lord2, lord1)
    if mitra1 == FRIEND and mitra2 == FRIEND: return 5
    elif (mitra1 == FRIEND and mitra2 == NEUTRAL) or (mitra2 == FRIEND and mitra1 == NEUTRAL): return 4
    elif (mitra1 == NEUTRAL and mitra2 == NEUTRAL) or \
            (mitra1 == FRIEND and mitra2 == ENEMY) or (mitra1 == ENEMY and mitra2 == FRIEND): return 2
    elif (mitra1 == ENEMY and mitra2 == NEUTRAL) or (mitra2 == ENEMY and mitra1 == NEUTRAL): return 1
    elif mitra1 == ENEMY and mitra2 == ENEMY: return 0

def calc_bhakoota_score(rasi1, rasi2):
    diff = abs(rasi1 - rasi2)
    diff = diff if diff <= 6 else 12 - diff
    if diff in BHAKOOTA_GOOD_DIFFS: return 7
    else: return 0

def calc_nadi_score(nadi1, nadi2):
    return 8 if nadi1 != nadi2 else 0

def calc_tara_score(tara1, tara2):
    score = 0
    if tara1 not in [3, 5, 7]: score += 1.5
    if tara2 not in [3, 5, 7]: score += 1.5
    return score

def calc_yoni_score(yoni1, yoni2):
    return YONI_SCORE_MATRIX[yoni1][yoni2]

def get_weekday_from_jd(jd):
    # 0=Monday, 6=Sunday (Python weekday)
    weekday = datetime.datetime.fromordinal(int(jd + 0.5) - 1721425).weekday()
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return days[weekday]

def ashtakootam_full(bride_moon_long, groom_moon_long, bride_jd, groom_jd):
    rasi1 = get_rasi_py(bride_moon_long)
    rasi2 = get_rasi_py(groom_moon_long)
    nak1 = get_nakshatra27(bride_moon_long)
    nak2 = get_nakshatra27(groom_moon_long)
    pada1 = get_pada(bride_moon_long)
    pada2 = get_pada(groom_moon_long)
    day1 = get_weekday_from_jd(bride_jd)
    day2 = get_weekday_from_jd(groom_jd)

    varna1 = get_varna(bride_moon_long)
    varna2 = get_varna(groom_moon_long)
    pvarna = 1 if varna1 >= varna2 else 0

    vashya1 = get_vashya(bride_moon_long)
    vashya2 = get_vashya(groom_moon_long)
    pvashya = VASHYA_MAP[vashya1][vashya2]

    tara1, tara2 = get_tara(nak1, nak2)
    ptara = calc_tara_score(tara1, tara2)

    yoni1, yoni1name = get_yoni(bride_moon_long)
    yoni2, yoni2name = get_yoni(groom_moon_long)
    pyoni = calc_yoni_score(yoni1, yoni2)

    lord1 = get_lord(rasi1)
    lord2 = get_lord(rasi2)
    pmaitri = calc_maitri_score(lord1, lord2)

    gana1, gana1name = get_gana(bride_moon_long)
    gana2, gana2name = get_gana(groom_moon_long)
    pgana = GANA_MAP[gana1][gana2]

    prasi = calc_bhakoota_score(rasi1, rasi2)
    nadi1, nadi1name = get_nadi(bride_moon_long)
    nadi2, nadi2name = get_nadi(groom_moon_long)
    pnadi = calc_nadi_score(nadi1, nadi2)
    rajju1 = get_rajju(nak1)
    rajju2 = get_rajju(nak2)
    prajju = calc_rajju_score(rajju1, rajju2)
    ptotal = pvarna + pvashya + ptara + pyoni + pmaitri + pgana + prasi + pnadi + prajju

    bride_details = {
        "Rasi": TELUGU_SIGNS[rasi1],
        "Nakshatra": TELUGU_NAKSHATRAS[nak1],
        "Pada": pada1,
        "Weekday": TELUGU_VAARAM[day1]
    }
    groom_details = {
        "Rasi": TELUGU_SIGNS[rasi2],
        "Nakshatra": TELUGU_NAKSHATRAS[nak2],
        "Pada": pada2,
        "Weekday": TELUGU_VAARAM[day2]
    }
    return {
        "Varna": {
            "points": pvarna,
            "max": 1,
            "desc": f"{VARNA_TELUGU[varna1]} / {VARNA_TELUGU[varna2]}"
        },
        "Vashya": {
            "points": pvashya,
            "max": 2,
            "desc": f"{VASHYA_TELUGU[vashya1]} / {VASHYA_TELUGU[vashya2]}"
        },
        "Tara": {
            "points": ptara,
            "max": 3,
            "desc": f"{TELUGU_NAKSHATRAS[nak1]} / {TELUGU_NAKSHATRAS[nak2]}"
        },
        "Yoni": {
            "points": pyoni,
            "max": 4,
            "desc": f"{YONI_NAMES[yoni1]} / {YONI_NAMES[yoni2]}"
        },
        "Maitri": {
            "points": pmaitri,
            "max": 5,
            "desc": f"{TELUGU_SIGNS[rasi1]} / {TELUGU_SIGNS[rasi2]}"
        },
        "Gana": {
            "points": pgana,
            "max": 6,
            "desc": f"{GANA_TELUGU[gana1]} / {GANA_TELUGU[gana2]}"
        },
        "Bhakoota": {
            "points": prasi,
            "max": 7,
            "desc": f"{TELUGU_SIGNS[rasi1]} / {TELUGU_SIGNS[rasi2]}"
        },
        "Nadi": {
            "points": pnadi,
            "max": 8,
            "desc": f"{NADI_TELUGU[nadi1]} / {NADI_TELUGU[nadi2]}"
        },
        "Rajju": {
            "points": prajju,
            "max": 4,
            "desc": ""
        },
        "Total": {
            "points": ptotal,
            "max": 36,
            "desc": f"{round(ptotal / 36 * 100)}%"
        },
        "bride": bride_details,
        "groom": groom_details
    }
