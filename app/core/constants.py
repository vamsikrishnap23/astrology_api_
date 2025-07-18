import swisseph as swe

# Classical planet indices for internal usage
OSUN, OMOON, OMARS, OMERCURY, OJUPITER, OVENUS, OSATURN, OASCENDANT = range(8)

PLANET_INDEX_TO_NAME = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Ascendant"]
PLANETS_INDEXED = [OSUN, OMOON, OMARS, OMERCURY, OJUPITER, OVENUS, OSATURN, OASCENDANT]

# Swisseph integer IDs and backend-unified PLANETS dict
PLANETS = {
    'Sun': swe.SUN,
    'Moon': swe.MOON,
    'Mars': swe.MARS,
    'Mercury': swe.MERCURY,
    'Jupiter': swe.JUPITER,
    'Venus': swe.VENUS,
    'Saturn': swe.SATURN,
    'Uranus': swe.URANUS,
    'Neptune': swe.NEPTUNE,
    'Pluto': swe.PLUTO,
    'Rahu': swe.MEAN_NODE
}

# --- Sign names ---
SIGN_NAMES = {
    1: "Aries",       2: "Taurus",    3: "Gemini",     4: "Cancer",
    5: "Leo",         6: "Virgo",     7: "Libra",      8: "Scorpio",
    9: "Saggitarius", 10: "Capricorn",11: "Aquarius", 12: "Pisces"
}
TELUGU_SIGNS = {
    1: "మేషం",   2: "వృషభం",     3: "మిథునం",    4: "కర్కాటకం",
    5: "సింహం",  6: "కన్యా",      7: "తులా",      8: "వృశ్చికం",
    9: "ధనుస్సు", 10: "మకరం",    11: "కుంభం",   12: "మీనం"
}

# --- Planets (Telugu) ---
TELUGU_PLANETS = {
    "Lagna": "లగ్నం",
    "Sun": "సూర్యుడు", "Moon": "చంద్రుడు", "Mars": "కుజుడు",
    "Mercury": "బుధుడు", "Jupiter": "గురు", "Venus": "శుక్రుడు", "Saturn": "శని",
    "Uranus": "యురేనస్", "Neptune": "నెప్ట్యూన్", "Pluto": "ప్లూటో",
    "Rahu": "రాహు", "Ketu": "కేతు"
}

PLANETS_ORDER = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu", "Ascendant"]

# --- Rasi Lords (Eng & Telugu) ---
RASI_LORDS = {
    1: "Mars", 2: "Venus", 3: "Mercury", 4: "Moon", 5: "Sun", 6: "Mercury",
    7: "Venus", 8: "Mars", 9: "Jupiter", 10: "Saturn", 11: "Saturn", 12: "Jupiter"
}
TELUGU_RASI_LORDS = {
    1: "కుజుడు", 2: "శుక్రుడు", 3: "బుధుడు", 4: "చంద్రుడు",
    5: "సూర్యుడు", 6: "బుధుడు", 7: "శుక్రుడు", 8: "కుజుడు",
    9: "గురు", 10: "శని", 11: "శని", 12: "గురు"
}

# --- Nakshatras ---
NAKSHATRA_NAMES = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu", "Pushya", "Ashlesha",
    "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada",
    "Uttara Bhadrapada", "Revati"
]
TELUGU_NAKSHATRAS = [
    "అశ్విని", "భరణి", "కృత్తిక", "రోహిణి", "మృగశిర", "ఆర్ద్ర", "పునర్వసు", "పుష్యమి", "ఆశ్లేష", "మఖ",
    "పుబ్బ", "ఉత్తర", "హస్త", "చిత్త", "స్వాతి", "విశాఖ", "అనూరాధ", "జ్యేష్ఠ", "మూల", "పూర్వాషాఢ",
    "ఉత్తరాషాఢ", "శ్రవణం", "ధనిష్ట", "శతభిష", "పూర్వాభాద్ర", "ఉత్తరాభాద్ర", "రేవతి"
]

# --- Days (Vaara) ---
ENGLISH_WEEKDAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
TELUGU_VAARAM = {
    "Sunday": "ఆదివారం", "Monday": "సోమవారం", "Tuesday": "మంగళవారం",
    "Wednesday": "బుధవారం", "Thursday": "గురువారం", "Friday": "శుక్రవారం", "Saturday": "శనివారం"
}

# --- Dashas ---
VIMSOTTARI_LORDS = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]

# --- Planet Dignities ---
OWN_SIGNS = {
    "Sun": [5], "Moon": [4], "Mars": [1, 8], "Mercury": [3, 6],
    "Jupiter": [9, 12], "Venus": [2, 7], "Saturn": [10, 11]
}
EXALTATION = {
    "Sun": (1, 10), "Moon": (2, 3), "Mars": (10, 28), "Mercury": (6, 15),
    "Jupiter": (4, 5), "Venus": (12, 27), "Saturn": (7, 20)
}
DEBILITATION = {
    "Sun": (7, 10), "Moon": (8, 3), "Mars": (4, 28), "Mercury": (12, 15),
    "Jupiter": (10, 5), "Venus": (6, 27), "Saturn": (1, 20)
}

# --- Table & Chart Headers (English & Telugu) ---
TABLE_HEADERS = {
    "planet":     {"en": "Planet",     "te": "గ్రహం"},
    "degrees":    {"en": "Degrees",    "te": "డిగ్రీలు"},
    "rasi":       {"en": "Sign",       "te": "రాశి"},
    "rasi_adhipathi": {"en": "Sign Lord",  "te": "రాశి అధిపతి"},
    "nakshatram": {"en": "Nakshatra",  "te": "నక్షత్రం"},
    "padam":      {"en": "Pada",       "te": "పాదం"},
    "retrogration":{"en": "Retrograde","te": "వక్రగతి"},
    "speed":      {"en": "Speed",      "te": "వేగం"},
    "ascendant":  {"en": "Ascendant",  "te": "లగ్నం"},
    "dignity":    {"en": "Dignity",    "te": "స్థితి"},
    "house":      {"en": "House",      "te": "స్థానం"},
    "vimsottari_adhipathi": {"en": "Dasha Lord", "te": "దశాధిపతి"}
}

PNCHANG_HEADERS = {
    "nakshatram": {"en": "Nakshatra", "te": "నక్షత్రం"},
    "padam": {"en": "Pada", "te": "పాదం"},
    "rasi": {"en": "Sign", "te": "రాశి"},
    "vaaram": {"en": "Weekday", "te": "వారం"},
    "tithi": {"en": "Tithi", "te": "తిథి"},
    "yoga": {"en": "Yoga", "te": "యోగం"},
    "karana": {"en": "Karana", "te": "కరణం"}
}

DASHA_HEADERS = {
    "mahadasa": {"en": "Mahadasha", "te": "మహాదశ"},
    "antardasha": {"en": "Antardasha", "te": "అంతర్దశ"},
    "start": {"en": "Start", "te": "ప్రారంభం"},
    "end": {"en": "End", "te": "ముగింపు"}
}

ASHTAKAVARGA_HEADERS = {
    "rekha": {"en": "Rekha", "te": "రేఖ"},
    "sarva": {"en": "Sarva", "te": "సర్వ"}
}

COMPATIBILITY_HEADERS = {
    "varna": {"en": "Varna", "te": "వర్ణ"},
    "vashya": {"en": "Vashya", "te": "వశ్య"},
    "tara": {"en": "Tara", "te": "తారా"},
    "yoni": {"en": "Yoni", "te": "యోని"},
    "maitri": {"en": "Maitri", "te": "మైత్రీ"},
    "gana": {"en": "Gana", "te": "గణ"},
    "bhakoota": {"en": "Bhakoota", "te": "భకూత"},
    "nadi": {"en": "Nadi", "te": "నాడి"},
    "raju": {"en": "Rajju", "te": "రాజుయు"},
    "total": {"en": "Total", "te": "మొత్తం"}
}

# --- Utility reverse dictionaries for quick translation ---
def planet_en2te(name):
    return TELUGU_PLANETS.get(name, name)

def sign_en2te(num):
    return TELUGU_SIGNS.get(num, SIGN_NAMES.get(num, str(num)))

def nakshatra_en2te(idx):
    try:
        return TELUGU_NAKSHATRAS[idx]
    except Exception:
        return NAKSHATRA_NAMES[idx] if idx < len(NAKSHATRA_NAMES) else str(idx+1)
