# pintura manual da rodada 1 (executada dentro de build_r1.py; g, put, W, H disponiveis)
def px(x, y, ch):
    g[y][x] = ch


def line(y, x0, x1, ch):
    for x in range(x0, x1 + 1):
        g[y][x] = ch


# ---------------------------------------------------------------- orelha de perto (esquerda)
put(18, 36, "T")
put(19, 36, "tT")
put(20, 36, "ttT")
put(21, 36, "ttT")
put(22, 36, "ttTD")
put(23, 36, "ttTTD")
put(24, 36, "ttTTD"); px(41, 24, "X")
put(25, 36, "ttTD");  px(40, 25, "X"); px(41, 25, "X")
put(26, 36, "tTD");   px(39, 26, "X"); px(40, 26, "X")
put(27, 37, "TD");    px(39, 27, "X")

# ---------------------------------------------------------------- orelha de longe (direita)
put(18, 50, "D")
put(19, 49, "Tt")
put(20, 49, "Tt")
put(21, 48, "TtT")
put(22, 48, "TtT")
put(23, 47, "DTtT")
put(24, 47, "DTTtT"); px(46, 24, "X")
put(25, 47, "DTtT");  px(46, 25, "X")
put(26, 48, "TtD");   px(47, 26, "X")
put(27, 49, "TD");    px(48, 27, "X")

# ---------------------------------------------------------------- testa e pelos grisalhos
put(24, 42, "XXXX")
put(25, 42, "KkGK"); px(46, 25, "X")
put(26, 41, "KGWKGK")
put(27, 40, "KKGKtGKKKGKGK")
# sobrancelhas (pontinhos tan)
put(27, 43, "tt")
put(27, 48, "Tt")

# ---------------------------------------------------------------- olhos (E com contorno e, brilho B)
# olho de perto: cols 42-45, rows 28-31
put(28, 41, "GeeeGtt")
put(29, 41, "GeEBeK")
put(30, 41, "KeEEeG")
put(31, 41, "Geee")
# olho de longe: cols 48-51
put(28, 47, "KGeeeK")
put(29, 47, "KGeEBe")
put(30, 47, "KGeEEe")
put(31, 47, "KGeee")

# ---------------------------------------------------------------- focinho / bochecha / queixo
put(31, 45, "G")
put(31, 50, "kK")
put(32, 40, "TttTTGWGGKKNkX")
put(33, 39, "TtttTGWGWGGeNNX")
put(34, 38, "KTTTGGeeeeeeX")
put(35, 41, "TtTTGWWGWG")
put(36, 41, "TTDT")
# nariz
put(32, 51, "NkX")
put(33, 51, "NNX")

# ---------------------------------------------------------------- garganta
put(37, 41, "tTTD")
put(38, 41, "TtD")
put(39, 41, "TTD")
put(40, 40, "kkkkk")
put(41, 40, "kKkKK")
# mancha do peito (tan + creme W no centro)
put(42, 41, "WW")
put(43, 39, "TTWWWT")
put(44, 38, "TttWWWtT")
put(45, 37, "TTtWWWWtT")
put(46, 37, "TTtWWWWtT")
put(47, 38, "TTtWWtT")
put(48, 39, "XTtWtX")

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

# ---------------------------------------------------------------- sombra X (barriga, contorno inferior)
line(46, 25, 28, "X"); line(47, 29, 31, "X"); line(48, 32, 34, "X")
line(47, 22, 28, "X"); line(46, 21, 24, "X")

# ---------------------------------------------------------------- pernas
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

# ---------------------------------------------------------------- toquinho
px(14, 35, "k")
