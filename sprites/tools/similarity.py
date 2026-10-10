"""Nota de 0 a 100 de quanto um sprite 24x24 se parece com a foto lateral da Kiara.

É o "olho automático" do loop de desenho pixel a pixel: roda em menos de 1 ms.
A nota mistura a silhueta (sobreposição entre a máscara do sprite e a da foto)
com as cores por região (preto / tan / grisalho / olho onde a foto manda).
Pequenos desalinhamentos (até 2 px pra cada lado) não são punidos.

--build-target monta o alvo a partir de reference/78cd3897-1000248733.jpg:
segmenta a cachorra (chão claro e pouco saturado fica de fora), conta peitoral
e saia de renda como corpo preto, tira a guia/bolinha/clipe, espelha pra olhar
pra direita e encaixa em 24x24 (patas na última linha, centralizada).
Saídas em sprites/candidates/target/:
  target_cutout.png       recorte RGBA em alta resolução (cores da foto, espelhado)
  target_cutout_body.png  o mesmo com peitoral/saia pintados de preto
  target_mask.png         24x24, L: 255 = cachorra
  target_classes.txt      matriz 24x24: K preto, T tan, G grisalho, E olho, . fundo
  target_preview_x8.png   classes | máscara ampliadas 8x

Classes das letras da paleta (pra comparar sprite x alvo):
  preto K k X N e S s U L | tan T t D | grisalho G W | olho E B O o
  outras H Y R V v C c P u (nunca batem com nada)
O alvo não tem olho visível (a foto pega a cabeça de cima), então um olho E
desenhado sobre região preta do alvo conta como acerto.

Uso:
  python3 sprites/tools/similarity.py --build-target
  python3 sprites/tools/similarity.py sprite.png [outro.txt ...] [--json]
  python3 sprites/tools/similarity.py sprite.png --ignore 6,0,13,7 --ignore 0,10,4,20

--ignore x0,y0,x1,y1 (coordenadas do sprite, extremos INCLUSIVOS) exclui a
região do cálculo: "exagero permitido" (ex.: orelhas maiores que na foto).
Pode repetir. Na API: Scorer().score(sprite, ignore=[(x0, y0, x1, y1)]).
Retorno: total = 100*(0.6*silhouette + 0.4*color), silhouette = IoU (0-1), color =
fração (0-1) dos pixels opacos do sprite que caem sobre a cachorra com a classe
certa, dx/dy = quanto mover o sprite (px) pra casar melhor com o alvo.
"""
import argparse
import json
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

from common import (
    SPRITES_DIR, TRANSPARENT, load_palette, matrix_to_image, parse_matrix,
    upscale, write_matrix,
)

SIZE = 24
SHIFT = 2
PHOTO = SPRITES_DIR.parent / "reference" / "78cd3897-1000248733.jpg"
TARGET_DIR = SPRITES_DIR / "candidates" / "target"

# classes: 0 fundo, 1 preto, 2 tan, 3 grisalho, 4 olho, 5 outro
BG, CK, CT, CG, CE, CO = range(6)
CLASS_LETTER = {CK: "K", CT: "T", CG: "G", CE: "E"}
CLASS_OF = {}
for _letters, _cls in (("KkXNeSsUL", CK), ("TtD", CT), ("GW", CG), ("EBOo", CE),
                       ("HYRVvCcPu", CO)):
    for _ch in _letters:
        CLASS_OF[_ch] = _cls

# compat[classe do sprite, classe do alvo]
COMPAT = np.eye(6, dtype=bool)
COMPAT[BG, :] = False
COMPAT[CO, :] = False
COMPAT[CE, CK] = True  # olho dentro do preto da cabeça

# True: color = acertos / pixels do sprite SOBRE o alvo (definição literal, mas um
# bloco preto qualquer tira ~54). False: acertos / TODOS os pixels opacos do sprite
# (pixel fora da silhueta também derruba a cor; bloco preto tira ~33, ruído ~21).
COLOR_ON_OVERLAP = False

# região da guia/bolinha/clipe na foto (px da imagem original); ver build_target
LEASH_POLY = [(793, 887), (1080, 760), (1080, 1010), (809, 1010), (807, 970)]


# ---------------------------------------------------------------- alvo

def classify_pixels(rgb, fg):
    """Classe (K/T/G) de cada pixel da foto. Peitoral e renda viram preto."""
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV_FULL).astype(np.float32)
    hue = hsv[..., 0] * 360 / 256
    sat = hsv[..., 1] / 255
    val = hsv[..., 2]
    cls = np.full(rgb.shape[:2], CK, np.uint8)
    teal = (hue >= 160) & (hue <= 215) & (sat > 0.25) & (val > 45)
    lace = (hue < 17) & (sat > 0.5) & (val > 60)
    tan = (hue >= 17) & (hue <= 45) & (sat >= 0.33) & (val >= 60)
    gray = (sat < 0.25) & (val >= 55)
    cls[gray] = CG
    cls[tan] = CT
    cls[teal | lace] = CK
    # ferragens prateadas do peitoral/clipe não são pelo grisalho
    near = cv2.dilate(teal.astype(np.uint8), np.ones((25, 25), np.uint8)).astype(bool)
    cls[near & (cls == CG)] = CK
    cls[~fg] = BG
    return cls, teal | lace


def segment(rgb):
    """Máscara booleana da cachorra (sem guia/bolinha/clipe), tamanho da foto."""
    mx = rgb.max(2).astype(np.int32)
    mn = rgb.min(2).astype(np.int32)
    sat = (mx - mn) / np.maximum(mx, 1)
    m = ((mx < 120) | ((sat > 0.30) & (mx > 60))).astype(np.uint8)
    m[:700] = 0
    m[1800:] = 0
    cv2.fillPoly(m, [np.array(LEASH_POLY, np.int32)], 0)
    ell = lambda n: cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (n, n))
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, ell(9))
    # preenche buracos (unhas, fivelas): tudo que não é alcançável pela borda
    pad = cv2.copyMakeBorder(m, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=0)
    flood = pad.copy()
    cv2.floodFill(flood, np.zeros((pad.shape[0] + 2, pad.shape[1] + 2), np.uint8), (0, 0), 2)
    m = ((flood[1:-1, 1:-1] != 2)).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, ell(7))
    n, lab, stats, _ = cv2.connectedComponentsWithStats(m, connectivity=8)
    biggest = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
    m = (lab == biggest).astype(np.uint8)
    m = (cv2.GaussianBlur(m * 255, (0, 0), 3) > 127).astype(np.uint8)
    return m.astype(bool)


def build_target(photo=PHOTO, outdir=TARGET_DIR, weights=(1.0, 1.35, 1.6), thr=0.35):
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    rgb = np.asarray(Image.open(photo).convert("RGB"))
    fg = segment(rgb)
    ys, xs = np.where(fg)
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    fg = fg[y0:y1, x0:x1][:, ::-1]  # espelha: olhando pra direita
    rgb = np.ascontiguousarray(rgb[y0:y1, x0:x1][:, ::-1])
    h, w = fg.shape

    # recorte em alta resolução (alpha levemente erodido: tira o halo do chão)
    alpha = cv2.erode(fg.astype(np.uint8) * 255, np.ones((5, 5), np.uint8))
    alpha = cv2.GaussianBlur(alpha, (0, 0), 1.2)
    cut = np.dstack([rgb, alpha])
    Image.fromarray(cut, "RGBA").save(outdir / "target_cutout.png")
    cls, body = classify_pixels(rgb, fg)
    flat = rgb.copy()
    flat[body & fg] = (23, 23, 27)
    Image.fromarray(np.dstack([flat, alpha]), "RGBA").save(outdir / "target_cutout_body.png")

    # quadro quadrado L x L: centralizado, pés na base; depois área -> 24x24
    L = max(w, h)
    ox, oy = (L - w) // 2, L - h
    inner = cv2.erode(fg.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (13, 13))).astype(bool)

    def canvas(a):
        c = np.zeros((L, L), np.float32)
        c[oy:oy + h, ox:ox + w] = a
        return cv2.resize(c, (SIZE, SIZE), interpolation=cv2.INTER_AREA)

    cover = canvas(fg.astype(np.float32))
    mask = cover >= thr
    votes = []
    for c in (CK, CT, CG):
        votes.append(canvas(((cls == c) & inner).astype(np.float32)))
    all_votes = [canvas(((cls == c) & fg).astype(np.float32)) for c in (CK, CT, CG)]
    votes = np.stack(votes)
    all_votes = np.stack(all_votes)
    use = np.where(votes.sum(0, keepdims=True) > 0.02, votes, all_votes)
    best = np.argmax(use * np.array(weights, np.float32)[:, None, None], axis=0)
    letters = np.array(["K", "T", "G"])[best]
    rows = ["".join(letters[y, x] if mask[y, x] else TRANSPARENT for x in range(SIZE))
            for y in range(SIZE)]

    Image.fromarray(mask.astype(np.uint8) * 255, "L").save(outdir / "target_mask.png")
    write_matrix(outdir / "target_classes.txt", rows, [
        "Alvo da similaridade: Kiara de lado olhando pra direita (foto 78cd3897),",
        "peitoral e saia viram preto; guia removida. K preto, T tan, G grisalho, E olho.",
        f"gerado por similarity.py --build-target (bbox {w}x{h} px, cobertura >= {thr})",
    ])
    cls_img = matrix_to_image(rows)
    mask_img = Image.fromarray(mask.astype(np.uint8) * 255, "L").convert("RGBA")
    a = upscale(cls_img, 8, bg="checker")
    b = upscale(mask_img, 8, bg=(40, 40, 46))
    prev = Image.new("RGBA", (a.width * 2 + 16, a.height), (24, 24, 28, 255))
    prev.paste(a, (0, 0))
    prev.paste(b, (a.width + 16, 0))
    prev.save(outdir / "target_preview_x8.png")
    print(f"alvo gravado em {outdir} (bbox {w}x{h}, {int(mask.sum())} px opacos)")
    return rows


# ---------------------------------------------------------------- nota

_LUT = np.full(256, CO, np.uint8)
for _ch, _c in CLASS_OF.items():
    _LUT[ord(_ch)] = _c
_LUT[ord(TRANSPARENT)] = BG


class Scorer:
    """Carrega o alvo uma vez; score() compara qualquer sprite 24x24 com ele."""

    def __init__(self, target_dir=TARGET_DIR):
        target_dir = Path(target_dir)
        try:
            tmask = np.asarray(Image.open(target_dir / "target_mask.png").convert("L")) > 127
            rows, _ = parse_matrix(target_dir / "target_classes.txt")
        except FileNotFoundError:
            sys.exit(f"alvo não encontrado em {target_dir}; rode: "
                     "python3 sprites/tools/similarity.py --build-target")
        tcls = _LUT[np.frombuffer("".join(rows).encode("latin-1"), np.uint8)].reshape(SIZE, SIZE)
        tcls = np.where(tmask, tcls, BG).astype(np.uint8)
        self.tmask, self.tcls = tmask, tcls
        pm = np.pad(tmask, SHIFT)
        pc = np.pad(tcls, SHIFT)
        win = np.lib.stride_tricks.sliding_window_view
        self._wmask = win(pm, (SIZE, SIZE))
        self._wcls = win(pc, (SIZE, SIZE))
        self._wmask_n = self._wmask.sum((2, 3))
        pal = load_palette()
        self._pal_letters = list(pal)
        self._pal = np.array([pal[k] for k in self._pal_letters], np.int32)
        self._pal_cls = np.array([CLASS_OF.get(k, CO) for k in self._pal_letters], np.uint8)
        self._w = np.array([3, 4, 2], np.int32)
        self._ign_cache = {}
        offs = np.arange(-SHIFT, SHIFT + 1)
        self._offs = offs
        self._pen = 1e-6 * (np.abs(offs)[:, None] + np.abs(offs)[None, :])

    # sprite -> (máscara, classes)
    def _prepare(self, sprite):
        if isinstance(sprite, (str, Path)):
            p = Path(sprite)
            sprite = parse_matrix(p)[0] if p.suffix == ".txt" else Image.open(p)
        if isinstance(sprite, Image.Image):
            px = np.asarray(sprite.convert("RGBA"))
            if px.shape[:2] != (SIZE, SIZE):
                raise ValueError(f"sprite deve ser {SIZE}x{SIZE}, veio {sprite.size[0]}x{sprite.size[1]}")
            mask = px[..., 3] >= 128
            cls = np.zeros((SIZE, SIZE), np.uint8)
            rgb = px[..., :3][mask].astype(np.int32)
            if len(rgb):
                d = (((rgb[:, None, :] - self._pal[None]) ** 2) * self._w).sum(-1)
                cls[mask] = self._pal_cls[d.argmin(1)]
            return mask, cls
        rows = list(sprite)
        if len(rows) != SIZE or any(len(r) > SIZE for r in rows):
            raise ValueError(f"matriz deve ser {SIZE}x{SIZE}")
        rows = [r.ljust(SIZE, TRANSPARENT) for r in rows]
        cls = _LUT[np.frombuffer("".join(rows).encode("latin-1"), np.uint8)].reshape(SIZE, SIZE)
        return cls != BG, cls

    def _ignore_mask(self, ignore):
        key = tuple(tuple(r) for r in ignore)
        m = self._ign_cache.get(key)
        if m is None:
            m = np.zeros((SIZE, SIZE), bool)
            for x0, y0, x1, y1 in key:
                m[max(y0, 0):y1 + 1, max(x0, 0):x1 + 1] = True
            self._ign_cache[key] = m
        return m

    def score(self, sprite, ignore=None):
        mask, cls = self._prepare(sprite)
        if ignore:
            keep = ~self._ignore_mask(ignore)
            mask = mask & keep
            wmask = self._wmask & keep
            wn = wmask.sum((2, 3))
        else:
            wmask, wn = self._wmask, self._wmask_n
        n = int(mask.sum())
        if n == 0:
            return dict(total=0.0, silhouette=0.0, color=0.0, dx=0, dy=0)
        both = wmask & mask
        inter = both.sum((2, 3))
        iou = inter / (n + wn - inter)
        ok = (both & COMPAT[cls, self._wcls]).sum((2, 3))
        col = ok / (np.maximum(inter, 1) if COLOR_ON_OVERLAP else n)
        tot = 100 * (0.6 * iou + 0.4 * col)
        i, j = np.unravel_index(np.argmax(tot - self._pen), tot.shape)
        return dict(total=round(float(tot[i, j]), 1), silhouette=round(float(iou[i, j]), 3),
                    color=round(float(col[i, j]), 3), dx=int(self._offs[j]), dy=int(self._offs[i]))


def parse_rect(s):
    try:
        x0, y0, x1, y1 = (int(v) for v in s.split(","))
    except ValueError:
        raise argparse.ArgumentTypeError("use x0,y0,x1,y1 (inteiros)")
    return (x0, y0, x1, y1)


def main():
    ap = argparse.ArgumentParser(description="Nota (0-100) de semelhança de um sprite 24x24 com a foto da Kiara.")
    ap.add_argument("sprites", nargs="*", help="sprites .png ou .txt (matriz de letras)")
    ap.add_argument("--build-target", action="store_true",
                    help="monta o alvo a partir da foto em reference/ e grava em sprites/candidates/target/")
    ap.add_argument("--photo", default=str(PHOTO), help="foto lateral (com --build-target)")
    ap.add_argument("--json", action="store_true", help="saída em JSON")
    ap.add_argument("--ignore", action="append", type=parse_rect, metavar="x0,y0,x1,y1",
                    help="região ignorada (extremos inclusivos); pode repetir")
    args = ap.parse_args()

    if args.build_target:
        build_target(args.photo)
        if not args.sprites:
            return
    if not args.sprites:
        ap.error("informe sprites ou --build-target")

    scorer = Scorer()
    res = {s: scorer.score(s, ignore=args.ignore) for s in args.sprites}
    if args.json:
        print(json.dumps(res, indent=2, ensure_ascii=False))
        return
    print(f"{'sprite':40s} {'nota':>6s} {'silhueta':>9s} {'cor':>6s}  dx dy")
    for name, r in res.items():
        print(f"{Path(name).name:40s} {r['total']:6.1f} {r['silhouette']:9.3f} {r['color']:6.3f} {r['dx']:3d}{r['dy']:3d}")


if __name__ == "__main__":
    main()
