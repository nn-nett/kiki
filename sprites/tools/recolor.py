"""Recolore um sprite PNG trocando cores específicas (ex.: husky -> Kiara).

O mapa é um JSON simples {"#cor_origem": "#cor_destino" | "LETRA_da_paleta"}.
Cores não mapeadas ficam como estão (use --strict p/ listar as que sobraram).

Uso:
  python3 sprites/tools/recolor.py entrada.png saida.png mapa.json [--strict]
"""
import argparse
import json
from collections import Counter
from pathlib import Path

from PIL import Image

SPRITES_DIR = Path(__file__).resolve().parent.parent


def hex2rgb(s):
    s = s.lstrip("#")
    return tuple(int(s[i : i + 2], 16) for i in (0, 2, 4))


def palette_letters():
    data = json.loads((SPRITES_DIR / "palette.json").read_text())
    out = {}
    for group in data["groups"].values():
        for key, info in group.items():
            out[key] = hex2rgb(info["hex"])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("mapfile", help="JSON {#origem: #destino ou letra da paleta}")
    ap.add_argument("--strict", action="store_true",
                    help="lista cores do sprite que não foram mapeadas")
    args = ap.parse_args()

    letters = palette_letters()
    rawmap = json.loads(Path(args.mapfile).read_text())
    cmap = {}
    for src, dst in rawmap.items():
        dst_rgb = letters[dst] if dst in letters else hex2rgb(dst)
        cmap[hex2rgb(src)] = dst_rgb

    img = Image.open(args.src).convert("RGBA")
    px = img.load()
    leftover = Counter()
    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            if (r, g, b) in cmap:
                px[x, y] = cmap[(r, g, b)] + (a,)
            else:
                leftover[(r, g, b)] += 1
    img.save(args.dst)
    print(f"salvo: {args.dst}")
    if args.strict and leftover:
        print("cores NÃO mapeadas:")
        for (r, g, b), n in leftover.most_common():
            print(f"  #{r:02x}{g:02x}{b:02x}  ({n} px)")


if __name__ == "__main__":
    main()
