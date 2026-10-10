"""Gerador de sprites da Kiara.

Cada sprite é um arquivo .txt em sprites/frames/ com uma matriz de caracteres:
cada letra mapeia para uma cor da paleta (sprites/palette.json) e '.' é
transparente. Este script converte a matriz em PNG (tamanho real) e gera um
preview ampliado (nearest-neighbor, sem anti-aliasing).

Uso:
    python3 sprites/tools/spritegen.py frames/sit_base.txt [--scale 8]
"""
import argparse
import sys
from pathlib import Path

from common import SPRITES_DIR, matrix_to_image, parse_matrix, upscale


def render(txt_path, scale):
    rows, _ = parse_matrix(txt_path)
    try:
        img = matrix_to_image(rows)
    except ValueError as e:
        sys.exit(f"ERRO: {e}")

    out_png = txt_path.with_suffix(".png")
    img.save(out_png)

    preview_dir = SPRITES_DIR / "previews"
    preview_dir.mkdir(exist_ok=True)
    # fundo quadriculado pra enxergar a transparência no preview
    out_preview = preview_dir / f"{txt_path.stem}_x{scale}.png"
    upscale(img, scale, bg="checker").save(out_preview)
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
