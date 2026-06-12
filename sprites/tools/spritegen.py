"""Gerador de sprites da Kiara.

Cada sprite é um arquivo .txt em sprites/frames/ com uma matriz de caracteres:
cada letra mapeia para uma cor da paleta (sprites/palette.json) e '.' é
transparente. Este script converte a matriz em PNG (tamanho real) e gera um
preview ampliado (nearest-neighbor, sem anti-aliasing).

Uso:
    python3 sprites/tools/spritegen.py frames/sit_base.txt [--scale 8]
"""
import argparse
import json
import sys
from pathlib import Path

from PIL import Image

SPRITES_DIR = Path(__file__).resolve().parent.parent
PALETTE_PATH = SPRITES_DIR / "palette.json"


def load_palette():
    data = json.loads(PALETTE_PATH.read_text())
    colors = {}
    for group in data["groups"].values():
        for key, info in group.items():
            hex_ = info["hex"].lstrip("#")
            colors[key] = tuple(int(hex_[i : i + 2], 16) for i in (0, 2, 4)) + (255,)
    return colors


def parse_matrix(path):
    rows = [
        line.rstrip("\n")
        for line in path.read_text().splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    width = max(len(r) for r in rows)
    return [r.ljust(width, ".") for r in rows], width


def render(txt_path, scale):
    palette = load_palette()
    rows, width = parse_matrix(txt_path)
    img = Image.new("RGBA", (width, len(rows)), (0, 0, 0, 0))
    unknown = set()
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch == ".":
                continue
            if ch not in palette:
                unknown.add(ch)
                continue
            img.putpixel((x, y), palette[ch])
    if unknown:
        sys.exit(f"ERRO: caracteres sem cor na paleta: {sorted(unknown)}")

    out_png = txt_path.with_suffix(".png")
    img.save(out_png)

    preview_dir = SPRITES_DIR / "previews"
    preview_dir.mkdir(exist_ok=True)
    big = img.resize((img.width * scale, img.height * scale), Image.NEAREST)
    # fundo quadriculado pra enxergar a transparência no preview
    bg = Image.new("RGBA", big.size, (70, 70, 76, 255))
    cell = scale * 4
    for cy in range(0, big.height, cell):
        for cx in range(0, big.width, cell):
            if (cx // cell + cy // cell) % 2 == 0:
                for yy in range(cy, min(cy + cell, big.height)):
                    for xx in range(cx, min(cx + cell, big.width)):
                        bg.putpixel((xx, yy), (82, 82, 90, 255))
    bg.alpha_composite(big)
    out_preview = preview_dir / f"{txt_path.stem}_x{scale}.png"
    bg.save(out_preview)
    print(f"sprite:  {out_png}  ({img.width}x{img.height})")
    print(f"preview: {out_preview}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("matrix", help="caminho do .txt da matriz (relativo a sprites/)")
    ap.add_argument("--scale", type=int, default=8)
    args = ap.parse_args()
    path = Path(args.matrix)
    if not path.is_absolute() and not path.exists():
        path = SPRITES_DIR / args.matrix
    render(path, args.scale)
