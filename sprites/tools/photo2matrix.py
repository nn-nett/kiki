"""Converte um recorte de foto em matriz de sprite (.txt) usando a paleta.

Cada pixel do recorte reduzido é mapeado para a cor mais próxima da paleta.
O resultado é um RASCUNHO: o fundo vem junto e precisa ser limpo à mão no .txt
(trocando por '.'), mas as proporções e marcações vêm da foto real.

Uso:
  python3 sprites/tools/photo2matrix.py reference/foto.jpg out.txt \
      --crop 0.36 0.05 0.84 0.34 --size 24 24
"""
import argparse
import json
from pathlib import Path

from PIL import Image

SPRITES_DIR = Path(__file__).resolve().parent.parent


def load_palette():
    data = json.loads((SPRITES_DIR / "palette.json").read_text())
    colors = {}
    for group in data["groups"].values():
        for key, info in group.items():
            h = info["hex"].lstrip("#")
            colors[key] = tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))
    return colors


def nearest(rgb, palette):
    # distância ponderada (olho humano é mais sensível ao verde)
    best, bk = None, None
    for k, (r, g, b) in palette.items():
        d = 3 * (rgb[0] - r) ** 2 + 4 * (rgb[1] - g) ** 2 + 2 * (rgb[2] - b) ** 2
        if best is None or d < best:
            best, bk = d, k
    return bk


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("photo")
    ap.add_argument("out")
    ap.add_argument("--crop", nargs=4, type=float, required=True,
                    metavar=("X0", "Y0", "X1", "Y1"), help="frações 0..1")
    ap.add_argument("--size", nargs=2, type=int, default=(24, 24))
    args = ap.parse_args()

    img = Image.open(args.photo).convert("RGB")
    w, h = img.size
    x0, y0, x1, y1 = args.crop
    crop = img.crop((int(x0 * w), int(y0 * h), int(x1 * w), int(y1 * h)))
    small = crop.resize(tuple(args.size), Image.LANCZOS)

    palette = load_palette()
    rows = []
    for y in range(small.height):
        rows.append("".join(nearest(small.getpixel((x, y)), palette)
                            for x in range(small.width)))
    out = Path(args.out)
    out.write_text("\n".join(rows) + "\n")
    print(f"salvo: {out}")


if __name__ == "__main__":
    main()
