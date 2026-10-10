"""Variações automáticas de um sprite (sem desenhar de novo).

Cada filtro é uma função fn(img, masks=None, **opts) -> img (RGBA -> RGBA, mesmo
tamanho) e fica no dicionário FILTERS. `masks` é um dict papel -> imagem "L" do
mesmo tamanho (255 = o pixel pertence àquela peça, ex. "torso"), fornecida pelo rig.

Filtros:
  mirror   espelha na horizontal
  night    câmera noturna: corpo vira silhueta S, borda s, olhos (E/B) viram O,
           vizinhos opacos do olho viram o (glow)
  sweater  suéter: dentro de masks["torso"] vira U com faixas verticais u
           (opts period=3, width=1, phase=0); fora da máscara nada muda
  rim      brilho de borda: pixels de borda de classe preto (K k X N e S s U L)
           recebem opts color (letra, padrão k)
  outline  contorno de 1 px por fora: transparentes vizinhos de um opaco
           recebem opts color (letra, padrão k); não aumenta o quadro
  overlay  compõe opts layer (imagem RGBA ou caminho; dx, dy opcionais) por cima

"Borda" = pixel opaco com algum vizinho (cima/baixo/esquerda/direita)
transparente ou fora do quadro. Entrada e saída podem ser .png ou .txt.

Uso:
  python3 sprites/tools/filters.py sprites/frames/sit_base.png noite.png --filter night
  python3 sprites/tools/filters.py pose.png sueter.png --filter sweater --mask torso=torso.png --opt period=3
  python3 sprites/tools/filters.py pose.png rim.png --filter rim --opt color=k
  python3 sprites/tools/filters.py pose.png forte.png --filter sweater,outline --mask torso=torso.png
"""
import argparse
from pathlib import Path

import numpy as np
from PIL import Image

from common import (
    TRANSPARENT, image_to_matrix, load_palette, matrix_to_image, parse_matrix,
    write_matrix,
)

DARK = set("KkXNeSsUL")
EYES = set("EBO")  # B e O têm a mesma cor (#ffffff); image_to_matrix devolve O


def _grid(img):
    rows = image_to_matrix(img, snap=True)
    return np.array([list(r) for r in rows])


def _image(grid):
    return matrix_to_image(["".join(r) for r in grid])


def _edge(op):
    """Opacos com algum vizinho-4 transparente (ou fora do quadro)."""
    p = np.pad(op, 1)
    inner = p[:-2, 1:-1] & p[2:, 1:-1] & p[1:-1, :-2] & p[1:-1, 2:]
    return op & ~inner


def _near(m):
    """Pixels que têm algum vizinho-4 em m."""
    p = np.pad(m, 1)
    return p[:-2, 1:-1] | p[2:, 1:-1] | p[1:-1, :-2] | p[1:-1, 2:]


def _mask(masks, role, shape):
    if not masks or role not in masks:
        raise ValueError(f"este filtro precisa de masks['{role}'] (imagem L, 255 = {role}); "
                         f"na CLI use --mask {role}=arquivo.png")
    m = np.asarray(masks[role].convert("L")) > 127
    if m.shape != shape:
        raise ValueError(f"máscara '{role}' tem tamanho {m.shape[::-1]}, o sprite tem {shape[::-1]}")
    return m


def _letter(opts, default):
    ch = str(opts.get("color", default))
    if ch not in load_palette():
        raise ValueError(f"color={ch!r} não é uma letra da paleta")
    return ch


def mirror(img, masks=None, **opts):
    return img.convert("RGBA").transpose(Image.FLIP_LEFT_RIGHT)


def night(img, masks=None, **opts):
    g = _grid(img)
    op = g != TRANSPARENT
    eye = np.isin(g, list(EYES))
    out = np.full(g.shape, TRANSPARENT)
    out[op] = "S"
    out[_edge(op)] = "s"
    out[_near(eye) & op] = "o"
    out[eye] = "O"
    return _image(out)


def sweater(img, masks=None, **opts):
    period = int(opts.get("period", 3))
    width = int(opts.get("width", 1))
    phase = int(opts.get("phase", 0))
    if period < 1 or not 0 < width <= period:
        raise ValueError("use period >= 1 e 1 <= width <= period")
    g = _grid(img)
    m = _mask(masks, "torso", g.shape) & (g != TRANSPARENT)
    if not m.any():
        return _image(g)
    x0 = np.nonzero(m.any(0))[0].min()
    stripe = ((np.arange(g.shape[1]) - x0 + phase) % period) < width
    g[m] = "U"
    g[m & stripe[None, :]] = "u"
    return _image(g)


def rim(img, masks=None, **opts):
    ch = _letter(opts, "k")
    g = _grid(img)
    hit = _edge(g != TRANSPARENT) & np.isin(g, list(DARK))
    g[hit] = ch
    return _image(g)


def outline(img, masks=None, **opts):
    ch = _letter(opts, "k")
    g = _grid(img)
    op = g != TRANSPARENT
    g[_near(op) & ~op] = ch
    return _image(g)


def overlay(img, masks=None, **opts):
    layer = opts.get("layer")
    if layer is None:
        raise ValueError("overlay precisa de opts layer (imagem RGBA ou caminho)")
    if not isinstance(layer, Image.Image):
        layer = Image.open(layer)
    layer = layer.convert("RGBA")
    base = img.convert("RGBA")
    dx, dy = int(opts.get("dx", 0)), int(opts.get("dy", 0))
    top = Image.new("RGBA", base.size, (0, 0, 0, 0))
    top.paste(layer, (dx, dy))
    return Image.alpha_composite(base, top)


FILTERS = {
    "mirror": mirror,
    "night": night,
    "sweater": sweater,
    "rim": rim,
    "outline": outline,
    "overlay": overlay,
}


def load_sprite(path):
    path = Path(path)
    if path.suffix == ".txt":
        return matrix_to_image(parse_matrix(path)[0])
    return Image.open(path).convert("RGBA")


def save_sprite(img, path):
    path = Path(path)
    if path.suffix == ".txt":
        write_matrix(path, image_to_matrix(img, snap=True), ["gerado por filters.py"])
    else:
        img.save(path)


def _value(v):
    try:
        return int(v)
    except ValueError:
        return v


def main():
    ap = argparse.ArgumentParser(description="Aplica filtros automáticos (noite, suéter, contorno...) a um sprite.")
    ap.add_argument("entrada", help="sprite .png ou .txt")
    ap.add_argument("saida", help="arquivo de saída (.png ou .txt)")
    ap.add_argument("--filter", required=True,
                    help=f"filtro(s), separados por vírgula e aplicados em ordem: {', '.join(FILTERS)}")
    ap.add_argument("--mask", action="append", default=[], metavar="papel=arquivo.png",
                    help="máscara de uma peça (L, 255 = peça), ex. torso=torso.png; pode repetir")
    ap.add_argument("--opt", action="append", default=[], metavar="chave=valor",
                    help="opção do filtro, ex. period=3 ou color=k; pode repetir")
    args = ap.parse_args()

    names = [n.strip() for n in args.filter.split(",") if n.strip()]
    bad = [n for n in names if n not in FILTERS]
    if bad:
        ap.error(f"filtro desconhecido: {', '.join(bad)} (existem: {', '.join(FILTERS)})")
    masks, opts = {}, {}
    for item in args.mask:
        role, _, path = item.partition("=")
        if not path:
            ap.error(f"--mask espera papel=arquivo.png, veio {item!r}")
        masks[role] = Image.open(path).convert("L")
    for item in args.opt:
        key, _, val = item.partition("=")
        if not val:
            ap.error(f"--opt espera chave=valor, veio {item!r}")
        opts[key] = _value(val)

    img = load_sprite(args.entrada)
    try:
        for n in names:
            img = FILTERS[n](img, masks or None, **opts)
    except ValueError as e:
        ap.error(str(e))
    save_sprite(img, args.saida)
    print(f"{args.entrada} -> {args.saida} ({'+'.join(names)})")


if __name__ == "__main__":
    main()
