"""Imagem de IA ("pixel art de mentira") -> sprite 24x24 na paleta da Kiara.

Imagem gerada por IA parece pixel art, mas não tem grade de verdade: cada
"pixelão" tem borda mole, cor levemente diferente e tamanho não inteiro.
Este script usa a biblioteca `unfake` pra achar o tamanho do pixelão, alinhar
na grade e reduzir; depois tira o fundo, recorta no bbox, encaixa em
--size x --size (centralizado, patas na última linha) e troca cada cor pela
letra mais parecida da paleta (common.nearest_letter).

Passos:
  1. unfake: detecta a escala, alinha a grade, quantiza em --max-colors cores
     e reduz pela cor dominante de cada bloco
  2. fundo: cor mais comum da borda (ou --bg #hex); tudo que é parecido
     (--tol) e liga na borda vira transparente (flood fill)
  3. recorta no bbox; se passar de --size, reduz pra caber pela letra
     dominante de cada célula (nunca suaviza)
  4. letras: cada cor vira a letra mais próxima da paleta; --letters limita
     quais letras valem (padrão: todas menos as das variantes que o filters.py
     gera, S s O o U u L)

Grava saida.txt (matriz com cabeçalho de origem/escala), saida.png e
saida_x8.png (ampliado 8x sobre quadriculado).

Uso:
  python3 sprites/tools/normalize.py entrada.png saida_prefixo
  python3 sprites/tools/normalize.py ia.png sprites/candidates/c/pose --size 24 --bg auto --max-colors 16
  python3 sprites/tools/normalize.py ia.png pose --bg "#00ff00" --tol 60 --scale 8
"""
import argparse
import logging
from pathlib import Path

import cv2
import numpy as np
import unfake
from PIL import Image

from common import (
    TRANSPARENT, hex2rgb, load_palette, matrix_to_image, nearest_letter,
    upscale, write_matrix,
)

DEFAULT_EXCLUDE = "SsOoUuL"


def detect_bg(rgba, bg):
    """Cor de fundo (r,g,b) ou None se a imagem já tem fundo transparente."""
    if bg != "auto":
        return hex2rgb(bg)
    ring = np.concatenate([rgba[0], rgba[-1], rgba[:, 0], rgba[:, -1]])
    if (ring[:, 3] < 128).mean() > 0.5:
        return None
    rgb = ring[ring[:, 3] >= 128][:, :3].astype(int)
    _, inv = np.unique(rgb // 8, axis=0, return_inverse=True)
    top = np.argmax(np.bincount(inv.ravel()))
    return tuple(int(v) for v in np.median(rgb[inv.ravel() == top], axis=0))


def remove_bg(rgba, bg, tol):
    """Zera o alpha do fundo: pixels parecidos com bg ligados à borda."""
    near = rgba[..., 3] < 128
    if bg is not None:
        d = np.sqrt(((rgba[..., :3].astype(int) - np.array(bg)) ** 2).sum(-1))
        near = near | (d <= tol)
    _, lab = cv2.connectedComponents(near.astype(np.uint8), connectivity=4)
    edge = np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))
    gone = np.isin(lab, edge[edge > 0]) & near
    out = rgba.copy()
    out[gone, 3] = 0
    return out


def to_letters(rgba, allowed):
    """RGBA -> matriz de índices (-1 = transparente) + lista de letras."""
    letters = list(allowed)
    pal = {k: allowed[k] for k in letters}
    idx = np.full(rgba.shape[:2], -1, np.int16)
    opaque = rgba[..., 3] >= 128
    colors = {}
    for y, x in zip(*np.nonzero(opaque)):
        rgb = tuple(int(v) for v in rgba[y, x, :3])
        if rgb not in colors:
            colors[rgb] = letters.index(nearest_letter(rgb, pal))
        idx[y, x] = colors[rgb]
    return idx, letters


def fit_dominant(idx, new_w, new_h):
    """Reduz a matriz de índices pela letra dominante de cada célula."""
    h, w = idx.shape
    ys = np.linspace(0, h, new_h + 1).round().astype(int)
    xs = np.linspace(0, w, new_w + 1).round().astype(int)
    out = np.full((new_h, new_w), -1, np.int16)
    for j in range(new_h):
        for i in range(new_w):
            block = idx[ys[j]:max(ys[j + 1], ys[j] + 1), xs[i]:max(xs[i + 1], xs[i] + 1)].ravel()
            solid = block[block >= 0]
            if len(solid) * 2 >= len(block):
                out[j, i] = np.argmax(np.bincount(solid))
    return out


def normalize(path, size=24, bg="auto", max_colors=16, tol=40, letters=None, scale=None):
    logging.getLogger("unfake.py").setLevel(logging.WARNING)
    res = unfake.process_image_sync(
        str(path), max_colors=max(2, min(max_colors, 255)), detect_method="auto",
        downscale_method="dominant", cleanup={"morph": False, "jaggy": False},
        snap_grid=True, transparent_background=False, manual_scale=scale,
    )
    detected = res["manifest"].processing_steps["scale_detection"]["detected_scale"]
    rgba = np.array(res["image"].convert("RGBA"))
    bgc = detect_bg(rgba, bg)
    rgba = remove_bg(rgba, bgc, tol)

    pal = load_palette()
    if letters is None:
        allowed = {k: v for k, v in pal.items() if k not in DEFAULT_EXCLUDE}
    elif letters == "all":
        allowed = pal
    else:
        allowed = {k: pal[k] for k in letters}
    idx, names = to_letters(rgba, allowed)

    ys, xs = np.nonzero(idx >= 0)
    if len(ys) == 0:
        raise SystemExit("nada sobrou depois de tirar o fundo; tente --bg ou --tol menor")
    idx = idx[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    h, w = idx.shape
    bbox = f"{w}x{h}"
    if max(w, h) > size:
        f = size / max(w, h)
        idx = fit_dominant(idx, max(1, round(w * f)), max(1, round(h * f)))
        ys, xs = np.nonzero(idx >= 0)
        idx = idx[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
        h, w = idx.shape

    frame = np.full((size, size), -1, np.int16)
    x0 = (size - w) // 2
    frame[size - h:, x0:x0 + w] = idx
    rows = ["".join(TRANSPARENT if v < 0 else names[v] for v in row) for row in frame]
    info = dict(detected_scale=detected, bg=bgc, bbox=bbox, final=f"{w}x{h}",
                colors=len(res["palette"]))
    return rows, info


def main():
    ap = argparse.ArgumentParser(description="Imagem de IA -> sprite na paleta da Kiara (usa unfake).")
    ap.add_argument("entrada", help="imagem de entrada (png/jpg)")
    ap.add_argument("saida", help="prefixo de saída (gera .txt, .png e _x8.png)")
    ap.add_argument("--size", type=int, default=24, help="lado do quadro final (padrão 24)")
    ap.add_argument("--bg", default="auto", help="'auto' (cor mais comum da borda) ou #hex")
    ap.add_argument("--max-colors", type=int, default=16, help="cores antes de mapear pra paleta (padrão 16)")
    ap.add_argument("--tol", type=float, default=40, help="tolerância do fundo (distância RGB, padrão 40)")
    ap.add_argument("--scale", type=int, help="tamanho do pixelão, se a detecção automática errar")
    ap.add_argument("--letters", help="letras permitidas (ex. KkTtGWEBNP) ou 'all'; "
                    f"padrão: todas menos {DEFAULT_EXCLUDE}")
    args = ap.parse_args()

    rows, info = normalize(args.entrada, args.size, args.bg, args.max_colors, args.tol,
                           args.letters, args.scale)
    out = Path(args.saida)
    out.parent.mkdir(parents=True, exist_ok=True)
    bg = info["bg"] if info["bg"] is None else "#%02x%02x%02x" % info["bg"]
    scale = info["detected_scale"]
    write_matrix(Path(f"{out}.txt"), rows, [
        f"origem: {Path(args.entrada).name} | normalize.py (unfake) | {args.size}x{args.size}",
        f"escala detectada: {scale}x{' (grade não detectada, redução direta)' if scale <= 1 else ''}"
        f" | fundo: {bg} | bbox {info['bbox']} -> {info['final']} | max-colors {args.max_colors}",
    ])
    img = matrix_to_image(rows)
    img.save(Path(f"{out}.png"))
    upscale(img, 8, bg="checker").save(Path(f"{out}_x8.png"))
    print(f"escala detectada {scale}x, fundo {bg}, bbox {info['bbox']} -> {info['final']}; "
          f"gravado {f'{out}.txt'}")
    if scale <= 1 and info["bbox"] != info["final"]:
        print("aviso: grade de pixel não detectada; a redução foi direta e pode borrar detalhes")


if __name__ == "__main__":
    main()
