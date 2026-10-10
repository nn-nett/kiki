"""Converte um recorte de foto em matriz de sprite (.txt) usando a paleta.

Cada pixel do recorte reduzido é mapeado para a cor mais próxima da paleta.
O resultado é um RASCUNHO: o fundo vem junto e precisa ser limpo à mão no .txt
(trocando por '.'), mas as proporções e marcações vêm da foto real.

Uso:
  python3 sprites/tools/photo2matrix.py reference/foto.jpg out.txt \
      --crop 0.36 0.05 0.84 0.34 --size 24 24
"""
import argparse
from pathlib import Path

from PIL import Image

from common import load_palette, nearest_letter


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
        rows.append("".join(nearest_letter(small.getpixel((x, y)), palette)
                            for x in range(small.width)))
    out = Path(args.out)
    out.write_text("\n".join(rows) + "\n")
    print(f"salvo: {out}")


if __name__ == "__main__":
    main()
