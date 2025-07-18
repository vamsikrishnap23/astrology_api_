# app/core/vimshottari_dashas.py

import swisseph as swe
from .constants import VIMSOTTARI_LORDS, TELUGU_PLANETS

# Full sequence of years for each Mahadasha (order matches VIMSOTTARI_LORDS)
VIMSOTTARI_YEARS = [7, 20, 6, 10, 7, 18, 16, 19, 17]  # Ketu, Venus, Sun, Moon, Mars, Rahu, Jupiter, Saturn, Mercury (Maitreya order)
TOTAL_YEARS = 120
NAKSHATRA_SPAN = 13 + 1/3  # 13°20' = 13.333...

def get_vimsottari_start_index(nakshatra_num):
    # Nakshatra: 0-based, Ketu starts at Ashwini (index 0)
    # Lord order: Ketu, Venus, Sun, Moon, Mars, Rahu, Jupiter, Saturn, Mercury
    return nakshatra_num % 9

def get_vimsottari_lord_sequence(nakshatra_num):
    start_index = get_vimsottari_start_index(nakshatra_num)
    lords = VIMSOTTARI_LORDS[start_index:] + VIMSOTTARI_LORDS[:start_index]
    years = VIMSOTTARI_YEARS[start_index:] + VIMSOTTARI_YEARS[:start_index]
    return lords, years, start_index

def jd_to_str(jd):
    y, m, d, frac = swe.revjul(jd, swe.GREG_CAL)
    total_seconds = int(round(frac * 86400))
    h = total_seconds // 3600
    mi = (total_seconds % 3600) // 60
    s = total_seconds % 60
    return f"{d:02}-{m:02}-{y} {h:02}:{mi:02}:{s:02}"

def compute_vimsottari_dashas(moon_longitude_deg, jd_birth, use_telugu=True):
    """
    :param moon_longitude_deg: sidereal longitude of Moon at birth (deg, 0–360)
    :param jd_birth: Julian Day at birth (UT)
    :param use_telugu: If True, output Telugu names, else English.
    :return: List of dicts with all Mahadasha and (nested) Antardasha periods.
    """
    # Find nakshatra (0-based, 13.333... per nak.)
    nakshatra_num = int(moon_longitude_deg // NAKSHATRA_SPAN)
    offset_in_nakshatra = moon_longitude_deg % NAKSHATRA_SPAN

    lords, years, _ = get_vimsottari_lord_sequence(nakshatra_num)

    # Fraction of first Mahadasha elapsed
    first_dasha_years = years[0]
    elapsed_fraction = offset_in_nakshatra / NAKSHATRA_SPAN
    elapsed_years = first_dasha_years * elapsed_fraction
    elapsed_days = elapsed_years * 365.25

    maha_start_jd = jd_birth - elapsed_days
    dashas = []
    jd = maha_start_jd

    for lord, duration in zip(lords, years):
        maha_lord_label = TELUGU_PLANETS.get(lord, lord) if use_telugu else lord
        dashas.append({
            "mahadasha_lord": maha_lord_label,
            "start_jd": jd,
            "end_jd": jd + duration * 365.25,
            "duration_years": duration,
            "antardashas": []
        })
        jd += duration * 365.25

    # Build antardashas for each Mahadasha
    for i, dasha in enumerate(dashas):
        m_lord = lords[i]
        m_years = years[i]
        ant_lords = lords[i:] + lords[:i]
        ant_years = years[i:] + years[:i]
        antardashas = []
        ant_jd = dasha["start_jd"]
        for a_lord, a_years in zip(ant_lords, ant_years):
            dur = m_years * a_years / TOTAL_YEARS
            antar_lord_label = TELUGU_PLANETS.get(a_lord, a_lord) if use_telugu else a_lord
            antardashas.append({
                "antardasha_lord": antar_lord_label,
                "start_jd": ant_jd,
                "end_jd": ant_jd + dur * 365.25,
                "duration_years": dur
            })
            ant_jd += dur * 365.25
        dasha["antardashas"] = antardashas

    return dashas
