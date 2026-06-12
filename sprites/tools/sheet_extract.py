"""Extrai frames de um spritesheet com fundo sólido.

- Remove o fundo por flood-fill a partir das bordas (não come cores iguais
  dentro do sprite).
- Pixels da cor do fundo que ficaram EMPAREDADOS dentro do sprite (truque
  clássico do NES: rosto do Black Mage) podem virar uma cor sólida (--enclosed).

Uso:
  python3 sprites/tools/sheet_extract.py sheet.png saida_dir prefixo \
      --cells "5,105,16,24 22,105,16,24" --bg auto --enclosed "#000000"
"""
import argparse
from pathlib import Path

from PIL import Image


def hex2rgb(s):
    s = s.lstrip("#")
    return tuple(int(s[i : i + 2], 16) for i in (0, 2, 4))


def extract_cell(sheet, x, y, w, h, bg, enclosed):
    cell = sheet.crop((x, y, x + w, y + h)).convert("RGBA")
    px = cell.load()
    if bg == "auto":
        bg_rgb = px[0, 0][:3]
    else:
        bg_rgb = hex2rgb(bg)
    # 1) fundo conectado às bordas -> transparente
    stack = [(i, j) for i in range(w) for j in (0, h - 1)] + [
        (i, j) for i in (0, w - 1) for j in range(h)
    ]
    seen = set()
    while stack:
        i, j = stack.pop()
        if (i, j) in seen or not (0 <= i < w and 0 <= j < h):
            continue
        seen.add((i, j))
        if px[i, j][:3] == bg_rgb and px[i, j][3] > 0:
            px[i, j] = (0, 0, 0, 0)
            stack += [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]
    # 2) cor de fundo emparedada dentro do sprite -> cor sólida (ou mantém)
    if enclosed:
        enc = hex2rgb(enclosed) + (255,)
        for j in range(h):
            for i in range(w):
                if px[i, j][3] > 0 and px[i, j][:3] == bg_rgb:
                    px[i, j] = enc
    return cell


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("sheet")
    ap.add_argument("outdir")
    ap.add_argument("prefix")
    ap.add_argument("--cells", required=True,
                    help='lista "x,y,w,h" separada por espaço')
    ap.add_argument("--bg", default="auto", help='"auto" (canto da célula) ou #hex')
    ap.add_argument("--enclosed", default=None,
                    help="#hex p/ cor de fundo emparedada (ex.: rosto do black mage)")
    args = ap.parse_args()

    sheet = Image.open(args.sheet).convert("RGB")
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    for n, spec in enumerate(args.cells.split()):
        x, y, w, h = (int(v) for v in spec.split(","))
        frame = extract_cell(sheet, x, y, w, h, args.bg, args.enclosed)
        out = outdir / f"{args.prefix}_{n}.png"
        frame.save(out)
        print(f"frame {n}: {out} ({w}x{h})")


if __name__ == "__main__":
    main()
