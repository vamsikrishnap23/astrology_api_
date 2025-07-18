# core/ashtakavarga.py

from .constants import TELUGU_PLANETS, TELUGU_SIGNS

# Indices for classical planets and ascendant
OSUN, OMOON, OMERCURY, OVENUS, OMARS, OJUPITER, OSATURN, OASCENDANT = range(8)

# Rasi indices
R_ARIES, R_TAURUS, R_GEMINI, R_CANCER, R_LEO, R_VIRGO, R_LIBRA, R_SCORPIO, R_SAGITTARIUS, R_CAPRICORN, R_AQUARIUS, R_PISCES = range(12)

# Ashtakavarga calculation types
REKHA, TRIKONA, EKADHI = 0, 1, 2

GRAHAPINDA, RASIPINDA, YOGAPINDA = 0, 1, 2

def red12(x):
    return x % 12

def Min(a, b):
    return min(a, b)

# ---- IMPORTANT: REKHA_MAP must be filled from your uploaded ashtakavarga.py (8x8x12) ----
# Structure: REKHA_MAP[i][j][k] where
#   i = ashtakavarga source planet (Sun, ..., Asc)
#   j = counting planet (Sun, ..., Asc)
#   k = 0..11 (sign offset from reference rasi)
from .ashtakavarga_data import REKHA_MAP  # Import from a separate file for clarity and maintainability!

class Ashtakavarga:
    def __init__(self, get_rasi_func):
        self.get_rasi = get_rasi_func
        self.rekha = [[0]*12 for _ in range(8)]
        self.trikona = [[0]*12 for _ in range(8)]
        self.ekadhi = [[0]*12 for _ in range(8)]
        self.sarvaRekha = [0]*12
        self.sarvaTrikona = [0]*12
        self.sarvaEkadhi = [0]*12
        self.psarvaRekha = [0]*8
        self.psarvaTrikona = [0]*8
        self.psarvaEkadhi = [0]*8
        self.grahaPinda = [0]*8
        self.rasiPinda = [0]*8
        self.yogaPinda = [0]*8
        self.planetNumber = [0]*12

    def update(self):
        for i in range(8):
            for j in range(12):
                self.rekha[i][j] = self.trikona[i][j] = self.ekadhi[i][j] = 0
        for j in range(12):
            self.planetNumber[j] = 0
        self.calcRekha()
        self.calcTrikonaShodana()
        self.calcEkadhipatyaShodana()
        self.calcSarva()
        self.calcPinda()

    def getSingleRekha(self, i, j, k):
        # REKHA_MAP[i][j][k]: i = ashta source planet, j = counting planet, k = sign offset
        return REKHA_MAP[i][j][k]

    def calcRekha(self):
        for i in range(8):
            for j in range(8):
                p2_rasi = self.get_rasi(j if j < 7 else OASCENDANT)
                for k in range(12):
                    house = red12(p2_rasi + k)
                    if self.getSingleRekha(i, j, k):
                        self.rekha[i][house] += 1

    def calcTrikonaShodana(self):
        for i in range(8):
            for j in range(4):
                minrekha = min(self.rekha[i][j], self.rekha[i][j+4], self.rekha[i][j+8])
                for k in range(3):
                    self.trikona[i][j + 4*k] = self.rekha[i][j + 4*k] - minrekha

    def calcEkadhipatyaPair(self, rasi1, rasi2):
        for p in range(8):
            if not self.planetNumber[rasi1] and not self.planetNumber[rasi2] and self.trikona[p][rasi1] != self.trikona[p][rasi2]:
                val = Min(self.trikona[p][rasi1], self.trikona[p][rasi2])
                self.ekadhi[p][rasi1] = self.ekadhi[p][rasi2] = val
            elif self.planetNumber[rasi1] and self.planetNumber[rasi2]:
                pass
            elif self.planetNumber[rasi1] and not self.planetNumber[rasi2] and self.trikona[p][rasi1] < self.trikona[p][rasi2]:
                self.ekadhi[p][rasi2] -= self.trikona[p][rasi1]
            elif self.planetNumber[rasi2] and not self.planetNumber[rasi1] and self.trikona[p][rasi2] < self.trikona[p][rasi1]:
                self.ekadhi[p][rasi1] -= self.trikona[p][rasi2]
            elif self.planetNumber[rasi1] and not self.planetNumber[rasi2] and self.trikona[p][rasi1] > self.trikona[p][rasi2]:
                self.ekadhi[p][rasi2] = 0
            elif self.planetNumber[rasi2] and not self.planetNumber[rasi1] and self.trikona[p][rasi2] > self.trikona[p][rasi1]:
                self.ekadhi[p][rasi1] = 0
            elif not self.planetNumber[rasi1] and not self.planetNumber[rasi2] and self.trikona[p][rasi1] == self.trikona[p][rasi2]:
                self.ekadhi[p][rasi1] = self.ekadhi[p][rasi2] = 0
            elif self.planetNumber[rasi1] and not self.planetNumber[rasi2]:
                self.ekadhi[p][rasi2] = 0
            elif self.planetNumber[rasi2] and not self.planetNumber[rasi1]:
                self.ekadhi[p][rasi1] = 0

    def calcEkadhipatyaShodana(self):
        for i in range(7):
            rasi = self.get_rasi(i)
            self.planetNumber[rasi] += 1
        for i in range(8):
            for j in range(12):
                self.ekadhi[i][j] = self.trikona[i][j]
        self.calcEkadhipatyaPair(R_ARIES, R_SCORPIO)
        self.calcEkadhipatyaPair(R_TAURUS, R_LIBRA)
        self.calcEkadhipatyaPair(R_GEMINI, R_VIRGO)
        self.calcEkadhipatyaPair(R_SAGITTARIUS, R_PISCES)
        self.calcEkadhipatyaPair(R_CAPRICORN, R_AQUARIUS)

    def calcSarva(self):
        for i in range(12):
            self.sarvaRekha[i] = self.sarvaTrikona[i] = self.sarvaEkadhi[i] = 0
        for i in range(8):
            self.psarvaRekha[i] = self.psarvaTrikona[i] = self.psarvaEkadhi[i] = 0
        # Only count Sun to Saturn (planet indices 0 to 6), not Ascendant (7)
        for i in range(12):
            for j in range(7): 
                self.sarvaRekha[i] += self.rekha[j][i]
                self.sarvaTrikona[i] += self.trikona[j][i]
                self.sarvaEkadhi[i] += self.ekadhi[j][i]
            for j in range(8): 
                self.psarvaRekha[j] += self.rekha[j][i]
                self.psarvaTrikona[j] += self.trikona[j][i]
                self.psarvaEkadhi[j] += self.ekadhi[j][i]


    def calcPinda(self):
        k_rasimana = [7, 10, 8, 4, 10, 6, 7, 8, 9, 5, 11, 12]
        k_grahamana = [5, 5, 5, 7, 8, 10, 5]
        for planet in range(8):
            self.rasiPinda[planet] = self.grahaPinda[planet] = self.yogaPinda[planet] = 0
            for rasi in range(12):
                self.rasiPinda[planet] += self.ekadhi[planet][rasi] * k_rasimana[rasi]
                self.yogaPinda[planet] += self.ekadhi[planet][rasi]  # if sodhya pinda mode == 1
            for p in range(7):
                rasi = self.get_rasi(p)
                self.grahaPinda[planet] += self.ekadhi[planet][rasi] * k_grahamana[p]
            # If sodhya pinda mode != 1:
            self.yogaPinda[planet] = self.grahaPinda[planet] + self.rasiPinda[planet]

    def getItem(self, typ, planet, rasi):
        if typ == REKHA:
            return self.rekha[planet][rasi]
        elif typ == TRIKONA:
            return self.trikona[planet][rasi]
        elif typ == EKADHI:
            return self.ekadhi[planet][rasi]
        else:
            raise ValueError("Unknown type")

    def getPinda(self, typ, i):
        if typ == GRAHAPINDA:
            return self.grahaPinda[i]
        elif typ == RASIPINDA:
            return self.rasiPinda[i]
        elif typ == YOGAPINDA:
            return self.yogaPinda[i]
        else:
            raise ValueError("Unknown pinda type")

    def getSarva(self, typ, rasi):
        if typ == REKHA:
            return self.sarvaRekha[rasi]
        elif typ == TRIKONA:
            return self.sarvaTrikona[rasi]
        elif typ == EKADHI:
            return self.sarvaEkadhi[rasi]
        else:
            raise ValueError("Unknown sarva type")

    def getPlanetSarva(self, typ, planet):
        if typ == REKHA:
            return self.psarvaRekha[planet]
        elif typ == TRIKONA:
            return self.psarvaTrikona[planet]
        elif typ == EKADHI:
            return self.psarvaEkadhi[planet]
        else:
            raise ValueError("Unknown planet sarva type")
