"""Rodada 2: silhueta por spans -> contorno automatico -> pintura manual.

Ferramenta de autoria (so desta pasta). A fonte da verdade continua sendo base_rN.txt.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent.parent / "tools"))
from common import write_matrix  # noqa: E402

W = H = 64
g = [["."] * W for _ in range(H)]


def span(y, x0, x1, ch="K"):
    for x in range(x0, x1 + 1):
        g[y][x] = ch


# ---------------------------------------------------------------- silhueta
SIL = {
    17: [(35, 36), (50, 51)],
    18: [(35, 38), (49, 51)],
    19: [(35, 38), (48, 51)],
    20: [(35, 39), (48, 51)],
    21: [(35, 39), (47, 51)],
    22: [(35, 40), (47, 51)],
    23: [(35, 41), (46, 51)],
    24: [(35, 51)],
    25: [(35, 51)],
    26: [(35, 51)],
    27: [(36, 51)],
    28: [(36, 52)],
    29: [(36, 52)],
    30: [(36, 52)],
    31: [(35, 52)],
    32: [(35, 53)],
    33: [(34, 53)],
    34: [(33, 52), (13, 14)],
    35: [(32, 51), (13, 15)],
    36: [(20, 50), (14, 16)],
    37: [(15, 45)],
    38: [(15, 45)],
    39: [(15, 45)],
    40: [(15, 45)],
    41: [(15, 45)],
    42: [(15, 46)],
    43: [(14, 46)],
    44: [(14, 46)],
    45: [(14, 46)],
    46: [(14, 46)],
    47: [(14, 46)],
    48: [(14, 25), (29, 45)],
    49: [(14, 25), (32, 45)],
    50: [(14, 25), (34, 45)],
    # pernas: traseira perto (diagonal), traseira longe, dianteira perto (A), longe (B)
    51: [(14, 18), (20, 25), (35, 45)],
    52: [(13, 17), (20, 25), (35, 39), (42, 45)],
    53: [(12, 16), (20, 24), (35, 39), (42, 45)],
    54: [(11, 15), (20, 24), (35, 39), (42, 45)],
    55: [(11, 14), (20, 23), (35, 38), (42, 45)],
    56: [(11, 14), (20, 23), (35, 38), (42, 45)],
    57: [(11, 14), (20, 23), (35, 38), (42, 45)],
    58: [(11, 14), (21, 24), (35, 38), (42, 45)],
    59: [(11, 14), (21, 24), (35, 38), (42, 45)],
    60: [(11, 14), (21, 24), (35, 39), (42, 45)],
    61: [(11, 15), (21, 25), (35, 40), (42, 46)],
    62: [(11, 16), (21, 26), (35, 40), (42, 47)],
    63: [(11, 16), (21, 26), (35, 40), (42, 47)],
}
for y, spans in SIL.items():
    for a, b in spans:
        span(y, a, b, "K")

# contorno automatico: pixel da silhueta com vizinho (4-conexo) transparente
sil = [[c != "." for c in row] for row in g]
for y in range(H):
    for x in range(W):
        if not sil[y][x]:
            continue
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if not (0 <= nx < W and 0 <= ny < H) or not sil[ny][nx]:
                g[y][x] = "X"
                break


def put(y, x, s):
    """Escreve a string s a partir de (x, y); '_' deixa o pixel como esta."""
    for i, ch in enumerate(s):
        if ch != "_":
            g[y][x + i] = ch


exec((HERE / "paint_r4.py").read_text())

rows = ["".join(r) for r in g]
assert len(rows) == 64 and all(len(r) == 64 for r in rows)
out = HERE / "base_r4.txt"
write_matrix(out, rows, header=[
    "Kiara base 64x64 - D2 limpo (rodada 4)",
    "origem: tiers/D2_64.txt (D2 Figma/gemini) | autoria: build_r4.py",
])
print("ok", out)
