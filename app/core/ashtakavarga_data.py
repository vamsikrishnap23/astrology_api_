# ashtakavarga_data.py

# The full REKHA_MAP is a 3-dimensional array:
# Dimensions: [8][8][12]
# - First index: Ashtakavarga source planet (Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Ascendant)
# - Second index: Counting planet (Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Ascendant)
# - Third index: Offset sign (0: counted-from sign, 1: next, ... 11: previous)

# Each entry is 1 (bindu given) or 0 (no bindu).

REKHA_MAP = [
    # Sun's Ashtakavarga
    [
        [1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0],  # Sun
        [0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0],  # Moon
        [0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1],  # Mercury
        [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1],  # Venus
        [1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0],  # Mars
        [0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0],  # Jupiter
        [1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0],  # Saturn
        [0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1],  # Ascendant
    ],
    # Moon's Ashtakavarga
    [
        [0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0],  # Sun
        [1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0],  # Moon
        [1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0],  # Mercury
        [0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0],  # Venus
        [0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0],  # Mars
        [1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0],  # Jupiter
        [0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0],  # Saturn
        [0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0],  # Ascendant
    ],
    # Mercury's Ashtakavarga
    [
        [0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1],  # Sun
        [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0],  # Moon
        [1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1],  # Mercury
        [1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0],  # Venus
        [1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0],  # Mars
        [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1],  # Jupiter
        [1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0],  # Saturn
        [1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0],  # Ascendant
    ],
    # Venus's Ashtakavarga
    [
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1],  # Sun
        [1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1],  # Moon
        [0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0],  # Mercury
        [1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0],  # Venus
        [0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1],  # Mars
        [0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0],  # Jupiter
        [0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0],  # Saturn
        [1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0],  # Ascendant
    ],
    # Mars's Ashtakavarga
    [
        [0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0],  # Sun
        [0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0],  # Moon
        [0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0],  # Mercury
        [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1],  # Venus
        [1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0],  # Mars
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1],  # Jupiter
        [1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0],  # Saturn
        [1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0],  # Ascendant
    ],
    # Jupiter's Ashtakavarga
    [
        [1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0],  # Sun
        [0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0],  # Moon
        [1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0],  # Mercury
        [0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0],  # Venus
        [1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0],  # Mars
        [1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0],  # Jupiter
        [0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1],  # Saturn
        [1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0],  # Ascendant
    ],
    # Saturn's Ashtakavarga
    [
        [1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0],  # Sun
        [0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0],  # Moon
        [0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1],  # Mercury
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1],  # Venus
        [1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0],  # Mars
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1],  # Jupiter
        [1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0],  # Saturn
        [1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0],  # Ascendant
    ],
    # Ascendant's Ashtakavarga
    [
        [1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0],  # Sun
        [0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0],  # Moon
        [1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0],  # Mercury
        [1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0],  # Venus
        [1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0],  # Mars
        [1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0],  # Jupiter
        [0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1],  # Saturn
        [1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0],  # Ascendant
    ],
]
