"""Quadro comparativo de candidatos nos 4 tamanhos (8, 16, 32, 64).

Para cada candidato, lê <dir>/<chave>_<tamanho>.png, mostra todos na mesma
área (ampliados sem suavização) e, ao lado, como ficam na taskbar escura e
clara do Windows 11 (16 em 2x, 32 e 64 em 1x).

Uso:
  python3 sprites/tools/tiers_board.py --dir sprites/candidates/tiers \
      --out quadro.png B_foto:"B · foto→pixels" C1:"C1 · Canva"
"""
import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from common import TASKBAR_DARK, TASKBAR_LIGHT, upscale

SIZES = [8, 16, 32, 64]
CELL, PAD, LABEL_W = 192, 16, 190


def font(size, bold=False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    try:
        return ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/{name}", size)
    except OSError:
        return ImageFont.load_default()


def build(folder, rows, title):
    F, f = font(18, True), font(14)
    W = LABEL_W + len(SIZES) * (CELL + PAD) + 300
    H = 70 + len(rows) * (CELL + PAD + 24)
    board = Image.new("RGB", (W, H), (40, 40, 46))
    d = ImageDraw.Draw(board)
    d.text((PAD, 14), title, font=F, fill=(255, 220, 120))
    for j, s in enumerate(SIZES):
        d.text((LABEL_W + j * (CELL + PAD) + 60, 44), f"{s}x{s}", font=F, fill=(230, 230, 230))
    strips_x = LABEL_W + len(SIZES) * (CELL + PAD) + 10
    d.text((strips_x, 44), "na taskbar", font=F, fill=(230, 230, 230))
    for i, (key, label) in enumerate(rows):
        y = 70 + i * (CELL + PAD + 24)
        d.text((PAD, y + CELL // 2 - 10), label, font=f, fill=(230, 230, 230))
        for j, s in enumerate(SIZES):
            path = Path(folder) / f"{key}_{s}.png"
            if not path.exists():
                continue
            big = upscale(Image.open(path), CELL // s, bg="checker").convert("RGB")
            board.paste(big, (LABEL_W + j * (CELL + PAD), y))
        for k, bg in enumerate((TASKBAR_DARK, TASKBAR_LIGHT)):
            strip = Image.new("RGBA", (280, 70), bg + (255,))
            x = 8
            for s, scale in ((16, 2), (32, 1), (64, 1)):
                path = Path(folder) / f"{key}_{s}.png"
                if not path.exists():
                    continue
                im = upscale(Image.open(path), scale)
                strip.alpha_composite(im, (x, 70 - im.height - 3))
                x += im.width + 14
            board.paste(strip.convert("RGB"), (strips_x, y + k * (CELL // 2 + 8)))
    d.text((strips_x, H - 24), "16 em 2x · 32 · 64", font=f, fill=(190, 190, 190))
    return board


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("rows", nargs="+", help='candidatos "chave:rótulo"')
    ap.add_argument("--dir", required=True, help="pasta com <chave>_<tamanho>.png")
    ap.add_argument("--out", required=True)
    ap.add_argument("--title", default="Candidatos em 8, 16, 32 e 64 px")
    args = ap.parse_args()
    rows = [tuple(r.split(":", 1)) if ":" in r else (r, r) for r in args.rows]
    build(args.dir, rows, args.title).save(args.out)
    print(f"quadro: {args.out}")


if __name__ == "__main__":
    main()
