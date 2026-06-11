"""Renderiza um preview visual da paleta (sprites/palette.json) com amostras
de cor nomeadas, agrupadas por categoria. Saída: sprites/previews/palette.png
"""
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SPRITES_DIR = Path(__file__).resolve().parent.parent
PALETTE_PATH = SPRITES_DIR / "palette.json"
OUT_PATH = SPRITES_DIR / "previews" / "palette.png"

SWATCH = 56
PAD = 16
ROW_H = SWATCH + 28
TITLE_H = 34
BG = (58, 58, 64)
FG = (240, 240, 240)


def load_font(size):
    for path in (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def main():
    palette = json.loads(PALETTE_PATH.read_text())
    groups = palette["groups"]

    cols = 4
    font_title = load_font(18)
    font_label = load_font(12)

    width = PAD * 2 + cols * (SWATCH * 3 + PAD)
    height = PAD
    for _, colors in groups.items():
        rows = -(-len(colors) // cols)
        height += TITLE_H + rows * ROW_H + PAD

    img = Image.new("RGB", (width, height), BG)
    draw = ImageDraw.Draw(img)

    y = PAD
    for group_name, colors in groups.items():
        draw.text((PAD, y), group_name.replace("_", " "), fill=FG, font=font_title)
        y += TITLE_H
        for i, (key, info) in enumerate(colors.items()):
            col, row = i % cols, i // cols
            x = PAD + col * (SWATCH * 3 + PAD)
            cy = y + row * ROW_H
            hex_ = info["hex"]
            rgb = tuple(int(hex_[j : j + 2], 16) for j in (1, 3, 5))
            draw.rectangle([x, cy, x + SWATCH, cy + SWATCH], fill=rgb, outline=FG)
            draw.text((x + SWATCH + 8, cy + 4), f"{key}  {hex_}", fill=FG, font=font_label)
            # quebra o nome em linhas curtas pra caber ao lado da amostra
            words, lines, cur = info["name"].split(), [], ""
            for w in words:
                if len(cur) + len(w) + 1 > 18:
                    lines.append(cur)
                    cur = w
                else:
                    cur = f"{cur} {w}".strip()
            lines.append(cur)
            for li, line in enumerate(lines[:3]):
                draw.text((x + SWATCH + 8, cy + 22 + li * 13), line, fill=FG, font=font_label)
        y += -(-len(colors) // cols) * ROW_H + PAD

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT_PATH)
    print(f"salvo: {OUT_PATH}")


if __name__ == "__main__":
    main()
