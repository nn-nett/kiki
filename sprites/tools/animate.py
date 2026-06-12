"""Monta um GIF de preview animado a partir de frames PNG (nearest-neighbor).

Os frames são compostos sobre um fundo sólido (GIF não tem alpha de verdade),
ampliados sem suavização e alinhados pela base (pé no chão).

Uso:
  python3 sprites/tools/animate.py saida.gif f0.png f1.png f0.png f2.png \
      --duration 280 --scale 10 --bg "#46464c"
"""
import argparse
from pathlib import Path

from PIL import Image


def hex2rgb(s):
    s = s.lstrip("#")
    return tuple(int(s[i : i + 2], 16) for i in (0, 2, 4))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("frames", nargs="+")
    ap.add_argument("--duration", type=int, default=250, help="ms por frame")
    ap.add_argument("--scale", type=int, default=10)
    ap.add_argument("--bg", default="#46464c")
    args = ap.parse_args()

    imgs = [Image.open(f).convert("RGBA") for f in args.frames]
    w = max(i.width for i in imgs)
    h = max(i.height for i in imgs)
    bg = hex2rgb(args.bg) + (255,)
    s = args.scale

    rendered = []
    for im in imgs:
        canvas = Image.new("RGBA", (w * s, h * s), bg)
        big = im.resize((im.width * s, im.height * s), Image.NEAREST)
        # alinha pela base, centraliza na horizontal
        canvas.alpha_composite(big, ((w - im.width) * s // 2, (h - im.height) * s))
        rendered.append(canvas.convert("P", palette=Image.ADAPTIVE))

    rendered[0].save(
        args.out, save_all=True, append_images=rendered[1:],
        duration=args.duration, loop=0, disposal=2,
    )
    print(f"gif: {args.out} ({len(rendered)} frames, {args.duration}ms)")


if __name__ == "__main__":
    main()
