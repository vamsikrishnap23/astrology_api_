import swisseph as swe

# Telugu output values for Panchang
TELUGU_NAKSHATRAS = [
    "అశ్విని", "భరణి", "కృత్తిక", "రోహిణి", "మృగశిర", "ఆరుద్ర", "పునర్వసు",
    "పుష్యము", "ఆశ్లేష", "మాఘ", "పూర్వ ఫల్గుని", "ఉత్తర ఫల్గుని", "హస్త",
    "చిత్త", "స్వాతి", "విశాఖ", "అనూరాధ", "జ్యేష్ఠ", "మూల", "పూర్వాషాఢ",
    "ఉత్తరాషాఢ", "శ్రవణం", "ధనిష్ఠ", "శతభిష", "పూర్వభాద్ర", "ఉత్తరభాద్ర", "రేవతి"
]
TELUGU_RASI = [
    "మేషం", "వృషభం", "మిథునం", "కర్కాటకం", "సింహం", "కన్యా", "తుల",
    "వృశ్చికం", "ధనుస్సు", "మకరం", "కుంభం", "మీనం"
]
TELUGU_TITHI = [
    "పాడ్యమి", "విదియ", "తృతీయ", "చవితి", "పంచమి", "షష్ఠి", "సప్తమి",
    "అష్టమి", "నవమి", "దశమి", "ఏకాదశి", "ద్వాదశి", "త్రయోదశి", "చతుర్దశి", "పౌర్ణమి/అమావాస్య"
]
TELUGU_PAKSHA = ["శుక్ల", "కృష్ణ"]
TELUGU_YOGA = [
    "విష్కంబ", "ప్రీతి", "ఆయుష్మాన్", "సౌభాగ్య", "శోభన", "అతిగండ", "సుకర్మ", "ధృతి",
    "శూల", "గండ", "వృద్ధి", "ధృవ", "వ్యాఘాత", "హర్షణ", "వజ్ర", "సిద్ధి", "వ్యతిపాత",
    "వర్యాన్", "పరిఘ", "శివ", "సిద్ధ్", "సాధ్య", "శుభ", "శుక్ల", "బ్రహ్మ", "ఇంద్ర", "వైధృతి"
]
TELUGU_KARANA = [
    "బవ", "బలవ", "కౌలవ", "తైతిల", "గరజ", "వణిజ", "విష్టి",
    "శకుని", "చతుష్పద", "నాగ", "కిమిస్టుఘ్న"
]
TELUGU_VAARA = [
    "ఆదివారం", "సోమవారం", "మంగళవారం", "బుధవారం", "గురువారం", "శుక్రవారం", "శనివారం"
]

def get_ayanamsa(jd):
    return swe.get_ayanamsa(jd)

def get_sidereal_longitude(jd, planet):
    flag = swe.FLG_SWIEPH | swe.FLG_SIDEREAL
    lon, _ = swe.calc_ut(jd, planet, flag)
    return lon[0] % 360

def get_panchang_telugu(jd, lat, lon, tz_offset):
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    # Core astronomical computations
    moon_long = get_sidereal_longitude(jd, swe.MOON)
    sun_long = get_sidereal_longitude(jd, swe.SUN)
    # Nakshatram
    nak_num = int(moon_long // (360/27))
    nak_name = TELUGU_NAKSHATRAS[nak_num]
    # Padam (Pada)
    pada = int((moon_long % (360/27)) // (360/108)) + 1
    # Rasi (Sign)
    rasi_num = int(moon_long // 30)
    rasi_name = TELUGU_RASI[rasi_num]
    # Tithi/paksha name
    tithi_float = ((moon_long - sun_long) % 360) / 12
    tithi_num = int(tithi_float)
    tithi_name = TELUGU_TITHI[tithi_num if tithi_num < 14 else 14]
    tithi_paksha = TELUGU_PAKSHA[0 if tithi_num < 15 else 1]
    # Yoga
    yoga_float = ((moon_long + sun_long) % 360) / (360/27)
    yoga_num = int(yoga_float)
    yoga_name = TELUGU_YOGA[yoga_num]
    # Karana
    phase = (moon_long - sun_long) % 360
    karana_num = int(phase // 6)
    if karana_num < 56:
        karana_name = TELUGU_KARANA[karana_num % 7]
    else:
        karana_name = TELUGU_KARANA[7 + (karana_num - 56)]
    # Varam (Weekday)
    weekday_num = int((jd + 1.5) % 7)
    vara_name = TELUGU_VAARA[weekday_num]
    # Result:
    return {
        "nakshatram": nak_name,
        "padam": str(pada),
        "rasi": rasi_name,
        "varam": vara_name,
        "tithi": f"{tithi_paksha} {tithi_name}",
        "yoga": yoga_name,
        "karanam": karana_name
    }
