# pintura manual da rodada 2 (executada dentro de build_r2.py; g, put, W, H disponiveis)
def px(x, y, ch):
    g[y][x] = ch


def line(y, x0, x1, ch):
    for x in range(x0, x1 + 1):
        g[y][x] = ch


# ---------------------------------------------------------------- orelha de perto (esquerda)
put(18, 36, "D")
put(19, 36, "tT")
put(20, 36, "ttT")
put(21, 36, "ttT")
put(22, 36, "ttTD")
put(23, 36, "ttTTD")
put(24, 36, "ttTTD")
put(25, 36, "ttTD")
put(26, 36, "tTD")
put(27, 37, "TD")

# ---------------------------------------------------------------- orelha de longe (direita)
put(18, 50, "D")
put(19, 49, "Tt")
put(20, 49, "Tt")
put(21, 48, "TtT")
put(22, 48, "TtT")
put(23, 47, "DTtT")
put(24, 47, "DTTtT")
put(25, 47, "DTtT")

# ---------------------------------------------------------------- cabeca (bloco cols 41-53; '_' = deixa)
HEAD = [
    # r24
    "XXXXXX____X..",
    # r25
    "XKkGKX____X..",
    # r26
    "KGKWKkKKKKX..",
    # r27  sobrancelhas tan (pontinhos)
    "KGtTWGKTtKX..",
    # r28  palpebra de cima (e)
    "GeeeeGKeeeeX.",
    # r29  olhos: E com contorno e e brilho B
    "KeEBeGGeEBeX.",
    # r30
    "GeEEeKGeEEeX.",
    # r31  palpebra de baixo + inicio da bochecha
    "TKGGKKGKGGKX.",
    # r32  bochecha tan, focinho grisalho, nariz
    "ttTtGGWGKKNkX",
    # r33
    "tTTtGWWGGGNNX",
    # r34  linha da boca
    "TTtTeeeeeeeX.",
    # r35  queixo
    "TtTTGWWWGWX..",
    # r36  fundo do queixo + garganta
    "TTDTXXXXXX...",
]
for i, s in enumerate(HEAD):
    put(24 + i, 41, s)

# bochecha esquerda (cols 39-40)
px(40, 32, "T"); px(40, 33, "T"); px(40, 34, "D")

# ---------------------------------------------------------------- garganta
put(37, 41, "tTTD")
put(38, 41, "TtD")
put(39, 41, "TTD")
put(40, 40, "kkkkk")
put(41, 40, "kKkKK")
# mancha do peito (tan + creme W no centro)
put(42, 41, "WW")
put(43, 39, "TTWWTT")
put(44, 38, "TttWWtTT")
put(45, 37, "TTtWWWtTT")
put(46, 37, "TttWWtTT")
put(47, 38, "DTtWtT")
put(48, 39, "DTWTD")

# ---------------------------------------------------------------- brilho k (volume da pelagem)
line(37, 19, 31, "k")
for x in (22, 26, 29):
    px(x, 37, "K")
line(38, 20, 23, "k"); line(38, 27, 31, "k")
for (x, y) in [(33, 37), (34, 38), (34, 39), (35, 40), (35, 41), (36, 42)]:
    px(x, y, "k")
for y in range(29, 35):
    px(37, y, "k")
for (x, y) in [(17, 38), (17, 39), (18, 40), (18, 41), (19, 42)]:
    px(x, y, "k")
px(14, 35, "k")

# ---------------------------------------------------------------- sombra X (barriga, contorno inferior)
line(46, 26, 28, "X"); line(47, 24, 31, "X"); line(48, 32, 34, "X")
line(49, 36, 39, "X")

# ---------------------------------------------------------------- pernas
# faixa tan da frente da coxa traseira de perto (sobre o preto)
for (x, y, c) in [(22, 44, "T"), (21, 45, "T"), (20, 46, "t"), (20, 47, "t"),
                  (19, 48, "t"), (18, 49, "t"), (18, 50, "t")]:
    px(x, y, c)
# traseira de perto (diagonal): preta em cima, faixa tan na frente, tan embaixo
put(51, 15, "KKt")
put(52, 14, "KKt")
put(53, 13, "KTt")
put(54, 12, "KTt")
for y in range(55, 61):
    put(y, 12, "Tt")
put(61, 12, "TtT")
put(62, 12, "TtDt")
# traseira de longe (mais escura)
put(51, 21, "KKKK")
put(52, 21, "KKKK")
put(53, 21, "KTT")
put(54, 21, "TTD")
for y in range(55, 58):
    put(y, 21, "DT")
for y in range(58, 61):
    put(y, 22, "DT")
put(61, 22, "DTT")
put(62, 22, "DTDT")
# dianteira de perto (A)
put(52, 36, "KKt")
put(53, 36, "KKt")
put(54, 36, "KKt")
put(55, 36, "Kt")
put(56, 36, "Kt")
for y in range(57, 60):
    put(y, 36, "Tt")
put(60, 36, "Ttt")
put(61, 36, "TttT")
put(62, 36, "TtDt")
# dianteira de longe (B, mais escura)
put(52, 43, "KK")
put(53, 43, "KT")
for y in range(54, 61):
    put(y, 43, "DT")
put(61, 43, "DTT")
put(62, 43, "DTDT")

# ---------------------------------------------------------------- rodada 3: volume extra e pelos soltos
for (x, y) in [(36, 43), (37, 43), (35, 42)]:
    px(x, y, "k")
for (x, y) in [(19, 39), (20, 40), (21, 41), (16, 39), (16, 40), (17, 41)]:
    px(x, y, "k")
px(40, 28, "G"); px(39, 30, "W"); px(38, 32, "G")
