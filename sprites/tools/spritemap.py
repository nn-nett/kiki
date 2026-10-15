"""Spritemap de revisão: todos os frames lado a lado, ampliados, numerados, com grade e régua.

Pedido do dono: "sempre que me mostrar algo, deixa o spritemap junto pra eu clicar,
expandir e dar print, talvez até no frame que tenho que atualizar". Cada linha é uma
animação; cada frame leva o número (f0, f1...) e a duração; a grade marca os pixels
(linha mais forte de 8 em 8) e a régua de 4 em 4 dá a coordenada x,y do quadro, a
mesma do tweak.py. O page.py e a galeria usam isto e embutem a imagem na página.

Uso:
  python3 sprites/tools/spritemap.py --out mapa.png "Nome|pasta do rig" ["Nome|pasta" ...]
"""
import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

BG = (243, 243, 243)
INK = (40, 40, 40)
MUTED = (110, 104, 98)


def font(size, bold=False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    try:
        return ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/{name}", size)
    except OSError:
        return ImageFont.load_default()


def from_folder(folder):
    """Frames de uma pasta do rig (manifest.json) -> [(rótulo, Image)]."""
    folder = Path(folder)
    man = json.loads((folder / "manifest.json").read_text())
    return [(f"f{i} · {f['duration']} ms", Image.open(folder / f["file"]).convert("RGBA"))
            for i, f in enumerate(man["frames"])]


def cell(im, zoom):
    """Frame ampliado sobre o fundo claro, com grade de pixel e régua."""
    w, h = im.size
    big = Image.new("RGBA", (w * zoom, h * zoom), BG + (255,))
    big.alpha_composite(im.resize((w * zoom, h * zoom), Image.NEAREST))
    grid = Image.new("RGBA", big.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(grid)
    for x in range(w + 1):
        d.line([(x * zoom, 0), (x * zoom, h * zoom)], fill=(0, 0, 0, 70 if x % 8 == 0 else 22))
    for y in range(h + 1):
        d.line([(0, y * zoom), (w * zoom, y * zoom)], fill=(0, 0, 0, 70 if y % 8 == 0 else 22))
    big.alpha_composite(grid)
    return big.convert("RGB")


def spritemap(rows, zoom=8):
    """rows = [(nome, [(rótulo, Image)])] -> Image do spritemap."""
    F, Fb, Fs = font(15), font(20, bold=True), font(11)
    ruler, gap, pad, head, lab = 22, 22, 16, 30, 22
    sizes = [[im.size for _, im in frames] for _, frames in rows]
    row_w = [sum(ruler + w * zoom + gap for w, _ in s) for s in sizes]
    row_h = [head + lab + ruler + max(h for _, h in s) * zoom + 14 for s in sizes]
    img = Image.new("RGB", (pad * 2 + max(row_w), pad + sum(row_h)), BG)
    d = ImageDraw.Draw(img)
    y0 = pad
    for (name, frames), rh in zip(rows, row_h):
        d.text((pad, y0), name, font=Fb, fill=INK)
        x0 = pad
        for label, im in frames:
            w, h = im.size
            cx, cy = x0 + ruler, y0 + head + lab + ruler
            d.text((cx, y0 + head), label, font=F, fill=INK)
            for x in range(0, w, 4):  # régua de cima (coluna x do quadro)
                d.text((cx + x * zoom + zoom // 2, cy - 4), str(x), font=Fs, fill=MUTED, anchor="mb")
            for y in range(0, h, 4):  # régua da esquerda (linha y)
                d.text((cx - 4, cy + y * zoom + zoom // 2), str(y), font=Fs, fill=MUTED, anchor="rm")
            img.paste(cell(im, zoom), (cx, cy))
            x0 = cx + w * zoom + gap
        y0 += rh
    return img


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("entries", nargs="+", help='"Nome|pasta do rig"')
    ap.add_argument("--out", required=True)
    ap.add_argument("--zoom", type=int, default=8)
    args = ap.parse_args()
    rows = []
    for entry in args.entries:
        name, folder = entry.split("|", 1)
        rows.append((name, from_folder(folder)))
    spritemap(rows, args.zoom).save(args.out)
    print(f"spritemap: {args.out}")


if __name__ == "__main__":
    main()
