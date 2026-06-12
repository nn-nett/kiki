"""Rascunho procedural da pose base sentada (vista lateral, olhando p/ esquerda).
Gera sprites/frames/sit_base.txt — depois o ajuste fino é feito direto no .txt.
"""
from pathlib import Path

W = H = 48
grid = [["." for _ in range(W)] for _ in range(H)]


def px(x, y, ch):
    if 0 <= x < W and 0 <= y < H:
        grid[y][x] = ch


def ellipse(cx, cy, rx, ry, ch):
    for y in range(cy - ry, cy + ry + 1):
        for x in range(cx - rx, cx + rx + 1):
            if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1.0:
                px(x, y, ch)


def rect(x0, y0, x1, y1, ch):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            px(x, y, ch)


def tri(tip, base_l, base_r, ch):
    (tx, ty), (lx, ly), (rx, ry) = tip, base_l, base_r
    for y in range(ty, ly + 1):
        f = (y - ty) / max(1, ly - ty)
        x0 = round(tx + (lx - tx) * f)
        x1 = round(tx + (rx - tx) * f)
        for x in range(x0, x1 + 1):
            px(x, y, ch)


# ---------- corpo (de trás pra frente) ----------
# rabo: fininho, sai da garupa e curva pra cima com gancho (caminho contínuo)
tail = [
    (36, 30), (37, 29), (37, 28), (38, 27), (38, 26), (39, 25), (39, 24),
    (39, 23), (40, 22), (40, 21), (40, 20), (40, 19), (40, 18), (40, 17),
    (39, 16), (39, 15),
]
for x, y in tail:
    px(x, y, "K")
    px(x + 1, y, "K")
px(39, 14, "k")
px(36, 31, "D")  # tan embaixo da base do rabo

# tronco: peito alto à esquerda descendo p/ garupa (sentada)
ellipse(22, 27, 9, 8, "K")   # caixa torácica/ombro
ellipse(29, 35, 9, 8, "K")   # garupa + coxa
rect(14, 24, 30, 36, "K")    # preenche o meio

# pata traseira no chão, apontando p/ esquerda
rect(23, 44, 30, 46, "T")
rect(23, 44, 30, 44, "t")
rect(31, 44, 32, 46, "D")

# pernas dianteiras: a de trás (sombra) e a da frente
rect(14, 34, 16, 43, "X")
rect(14, 44, 16, 46, "D")
rect(10, 32, 13, 43, "K")
rect(10, 36, 11, 43, "T")    # frente tan da perna
rect(7, 44, 13, 46, "T")
rect(7, 44, 13, 44, "t")

# peito tan na borda da frente, com mancha cremosa no centro
rect(10, 22, 12, 31, "T")
px(13, 23, "T")
px(13, 24, "T")
rect(11, 25, 12, 29, "W")

# ---------- cabeça ----------
# orelhas ENORMES de morcego (de trás primeiro)
tri((21, 0), (16, 9), (22, 9), "K")
tri((7, 0), (8, 9), (14, 9), "K")
px(10, 6, "D")  # leve interior da orelha da frente
px(10, 7, "D")
px(11, 7, "D")

# crânio
ellipse(13, 14, 7, 6, "K")

# focinho grisalho
rect(2, 14, 8, 18, "G")
rect(2, 13, 8, 13, "K")
rect(1, 14, 2, 15, "N")
rect(3, 18, 7, 19, "W")  # queixo

# bochecha tan + garganta
rect(7, 16, 9, 18, "T")
rect(7, 19, 10, 21, "T")

# olho com névoa azulada (anel escuro + íris + brilho)
for x, y in [(9, 13), (10, 13), (11, 13), (9, 14), (9, 15), (10, 16), (11, 16)]:
    px(x, y, "e")
rect(10, 14, 11, 15, "E")
px(10, 14, "B")

# sobrancelha tan
px(9, 12, "t")
px(10, 12, "t")

# ---------- acabamento ----------
# highlight azulado contínuo: topo da cabeça e borda superior do dorso
for x in range(10, 17):
    px(x, 9, "k")
for x in range(20, 36):
    for y in range(H):
        if grid[y][x] == "K":
            px(x, y, "k")
            break
# contorno-highlight contínuo da coxa (separa a perna do corpo)
for x, y in [(25, 30), (24, 31), (24, 32), (24, 33), (24, 34), (24, 35),
             (24, 36), (25, 37), (25, 38), (26, 39), (26, 40)]:
    px(x, y, "k")

# sombra X contínua na borda inferior do corpo
for x in range(16, 36):
    for y in range(H - 1, -1, -1):
        if grid[y][x] == "K":
            px(x, y, "X")
            break

# poucos pelos grisalhos salpicados (idade)
for x, y in [(12, 11), (15, 13), (14, 16)]:
    px(x, y, "W")

out = Path(__file__).resolve().parent.parent / "frames" / "sit_base.txt"
out.parent.mkdir(exist_ok=True)
out.write_text("\n".join("".join(r) for r in grid) + "\n")
print(f"salvo: {out}")
