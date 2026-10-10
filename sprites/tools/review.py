"""Folha de revisão: a imagem que um modelo com visão (ou você) olha pra criticar um sprite.

Layout, sobre fundo cinza neutro:
  1. o primeiro sprite ampliado sobre quadriculado, com grade de pixel (linha fina
     a cada pixel, mais forte a cada 4) e coordenadas 0-based (colunas em cima,
     linhas à esquerda) pra dar pra dizer "linha 12, coluna 15"; ao lado, a foto
     de referência na mesma altura (sem --ref, usa sprites/candidates/target/
     target_cutout.png se existir);
  2. faixas de taskbar falsa (escura e clara) com o sprite em 1x e 2x, alinhado
     pela base, como aparece no app;
  3. se houver mais de um frame: todos lado a lado em 4x, com o índice embaixo
     (pasta com manifest.json usa a ordem do manifest, sem repetir arquivos).

Entradas: .png, .txt (matriz de letras) ou pastas de frames.

Uso:
  python3 sprites/tools/review.py sprites/frames/sit_base.png --out folha.png
  python3 sprites/tools/review.py sprites/out/walk --out folha.png \
      --ref recorte.png --scale 8 --title "andando v2"
"""
import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

from common import SPRITES_DIR, TASKBAR_DARK, TASKBAR_LIGHT, checkerboard, hex2rgb, upscale
from lint import collect_animations, load_sprite

BG = hex2rgb("#3a3a40")
FG = (240, 240, 244)
DIM = (178, 178, 190)
ACCENT = (255, 214, 102)
GRID_THIN = (255, 255, 255, 34)
GRID_STRONG = (255, 214, 102, 120)

PAD = 16
GAP = 22
STRIP_W, STRIP_H = 360, 60
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
DEFAULT_REF = SPRITES_DIR / "candidates" / "target" / "target_cutout.png"


# ---------- utilidades de desenho (compartilhadas com compare.py)

def load_font(size, bold=False):
    for path in ((FONT_BOLD_PATH, FONT_PATH) if bold else (FONT_PATH,)):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    try:
        return ImageFont.load_default(size)
    except TypeError:  # Pillow antigo: fonte bitmap fixa
        return ImageFont.load_default()


def put(draw, text, x, y, font, fill=FG, ha="l", va="t"):
    """Escreve texto com alinhamento horizontal (l/c/r) e vertical (t/m) pelo bbox real."""
    l, t, r, b = draw.textbbox((0, 0), text, font=font)
    px = {"l": x, "c": x - (r - l) / 2, "r": x - (r - l)}[ha] - l
    py = {"t": y, "m": y - (b - t) / 2}[va] - t
    draw.text((px, py), text, font=font, fill=fill)
    return r - l, b - t


def text_width(text, font):
    return int(ImageDraw.Draw(Image.new("L", (1, 1))).textlength(text, font=font)) + 1


def heading(text, font, sub=None, sub_font=None):
    """Faixa de título de seção: texto em destaque e, opcional, uma linha de explicação."""
    width = max(text_width(text, font), text_width(sub or "", sub_font) if sub else 0)
    img = Image.new("RGBA", (width, 22 + (16 if sub else 0)), BG + (255,))
    d = ImageDraw.Draw(img)
    put(d, text, 0, 0, font, ACCENT)
    if sub:
        put(d, sub, 0, 21, sub_font, DIM)
    return img


def load_ref(path, height):
    """Foto de referência redimensionada pra `height` mantendo a proporção (LANCZOS)."""
    img = ImageOps.exif_transpose(Image.open(path)).convert("RGBA")
    width = max(1, round(img.width * height / img.height))
    img = img.resize((width, height), Image.LANCZOS)
    base = checkerboard(img.size, 8)  # recorte com transparência aparece quadriculado
    base.alpha_composite(img)
    return base


def resolve_ref(arg):
    """--ref explícito, ou o recorte-alvo padrão se existir, ou None."""
    if arg:
        if not Path(arg).exists():
            sys.exit(f"ERRO: referência não existe: {arg}")
        return Path(arg)
    return DEFAULT_REF if DEFAULT_REF.exists() else None


def gather_frames(inputs):
    """Entradas -> lista de (nome, imagem), na ordem dada, sem repetir arquivos."""
    frames, seen = [], set()
    for arg in inputs:
        if not Path(arg).exists():
            sys.exit(f"ERRO: não existe: {arg}")
        for anim in collect_animations([arg]):
            for _, _, msg, path in anim["problems"]:
                print(f"aviso: {msg} ({path})", file=sys.stderr)
            for path, _ in anim["entries"]:
                if path.resolve() in seen:
                    continue
                seen.add(path.resolve())
                try:
                    frames.append((path.stem, load_sprite(path)))
                except (OSError, ValueError) as e:
                    sys.exit(f"ERRO: não consegui ler {path}: {e}")
    if not frames:
        sys.exit("ERRO: nenhum sprite encontrado nas entradas")
    return frames


# ---------- bloco 1: sprite com grade e coordenadas

def grid_view(img, scale):
    """Sprite ampliado + grade + números de coluna (em cima) e de linha (à esquerda)."""
    w, h = img.size
    stagger = scale < 14  # colunas estreitas: números ímpares numa segunda linha
    avail = 2 * scale if stagger else scale
    size = max(7, min(12, int((avail - 3) / 1.28)))
    font, font_b = load_font(size), load_font(size, bold=True)
    lh = size + 3
    top = lh * (2 if stagger else 1) + 4
    left = text_width("00", font_b) + 8

    big = upscale(img, scale, bg="checker")
    grid = Image.new("RGBA", big.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(grid)
    for i in range(max(w, h) + 1):
        color = GRID_STRONG if i % 4 == 0 else GRID_THIN
        if i <= w:
            x = min(i * scale, w * scale - 1)
            gd.line([(x, 0), (x, h * scale - 1)], fill=color)
        if i <= h:
            y = min(i * scale, h * scale - 1)
            gd.line([(0, y), (w * scale - 1, y)], fill=color)
    big.alpha_composite(grid)

    out = Image.new("RGBA", (left + big.width + 4, top + big.height + 4), BG + (255,))
    out.alpha_composite(big, (left, top))
    d = ImageDraw.Draw(out)
    for x in range(w):
        strong = x % 4 == 0
        row = (x % 2) if stagger else 0
        put(d, str(x), left + x * scale + scale / 2, 2 + row * lh + lh / 2,
            font_b if strong else font, ACCENT if strong else DIM, ha="c", va="m")
    for y in range(h):
        strong = y % 4 == 0
        put(d, str(y), left - 5, top + y * scale + scale / 2,
            font_b if strong else font, ACCENT if strong else DIM, ha="r", va="m")
    return out, top


def block_sprite(name, img, ref_path, scale):
    f_head, f_small = load_font(13, bold=True), load_font(11)
    view, top = grid_view(img, scale)
    head = heading(f"1. Sprite ampliado {scale}x", f_head,
                   f"{name}  ({img.width}x{img.height})  -  coordenadas 0-based: coluna em cima, "
                   f"linha à esquerda; linha forte a cada 4 pixels", f_small)
    parts = [(view, 0)]
    if ref_path:
        photo = load_ref(ref_path, img.height * scale)
        parts.append((photo, view.width + GAP))
    width = max(head.width, parts[-1][1] + parts[-1][0].width)
    height = head.height + 8 + view.height + (16 if ref_path else 0)
    out = Image.new("RGBA", (width, height), BG + (255,))
    out.alpha_composite(head, (0, 0))
    y0 = head.height + 8
    out.alpha_composite(view, (0, y0))
    if ref_path:
        photo, x = parts[1]
        out.alpha_composite(photo, (x, y0 + top))
        put(ImageDraw.Draw(out), f"referência: {Path(ref_path).name}", x, y0 + top + photo.height + 3, f_small, DIM)
    return out


# ---------- bloco 2: taskbar falsa

def taskbar_strip(img, bg, label, edge):
    strip = Image.new("RGBA", (STRIP_W, STRIP_H), bg + (255,))
    d = ImageDraw.Draw(strip)
    d.line([(0, 0), (STRIP_W, 0)], fill=edge)
    base = STRIP_H - 6
    font = load_font(10)
    tint = (150, 150, 150) if sum(bg) < 384 else (110, 110, 110)
    for x, k in ((70, 1), (190, 2)):
        put(d, f"{k}x", x - 6, STRIP_H / 2, font, tint, ha="r", va="m")
        sprite = upscale(img, k)
        strip.alpha_composite(sprite, (x, base - sprite.height))
    return strip


def block_taskbar(img):
    f_head, f_small = load_font(13, bold=True), load_font(11)
    head = heading("2. Na taskbar do Windows 11", f_head,
                   "sprite em 1x e 2x, alinhado pela base, sobre fundo escuro e claro", f_small)
    width = 2 * STRIP_W + GAP
    out = Image.new("RGBA", (width, head.height + 8 + 18 + STRIP_H), BG + (255,))
    out.alpha_composite(head, (0, 0))
    d = ImageDraw.Draw(out)
    for i, (label, bg, edge) in enumerate((("taskbar escura", TASKBAR_DARK, (58, 58, 58, 255)),
                                           ("taskbar clara", TASKBAR_LIGHT, (214, 214, 214, 255)))):
        x = i * (STRIP_W + GAP)
        put(d, label, x, head.height + 8, f_small, FG)
        out.alpha_composite(taskbar_strip(img, bg, label, edge), (x, head.height + 8 + 18))
    return out


# ---------- bloco 3: todos os frames

def block_frames(frames, max_width, zoom=4):
    f_head, f_small, f_idx = load_font(13, bold=True), load_font(10), load_font(12, bold=True)
    head = heading(f"3. Frames ({len(frames)}) em {zoom}x", f_head, None)
    cw = max(i.width for _, i in frames) * zoom
    ch = max(i.height for _, i in frames) * zoom
    gap = 12
    per_row = max(1, (max_width + gap) // (cw + gap))
    rows = -(-len(frames) // per_row)
    label_h = 32
    width = min(len(frames), per_row) * (cw + gap) - gap
    out = Image.new("RGBA", (max(width, head.width), head.height + 8 + rows * (ch + label_h + gap)), BG + (255,))
    out.alpha_composite(head, (0, 0))
    d = ImageDraw.Draw(out)
    for n, (name, img) in enumerate(frames):
        x = (n % per_row) * (cw + gap)
        y = head.height + 8 + (n // per_row) * (ch + label_h + gap)
        cell = upscale(img, zoom, bg="checker")
        out.alpha_composite(cell, (x + (cw - cell.width) // 2, y + ch - cell.height))
        put(d, f"#{n}", x + cw / 2, y + ch + 3, f_idx, ACCENT, ha="c")
        put(d, name if len(name) <= 16 else name[:15] + "…", x + cw / 2, y + ch + 18, f_small, DIM, ha="c")
    return out


def main():
    ap = argparse.ArgumentParser(description="Monta a folha de revisão de um sprite ou animação.")
    ap.add_argument("inputs", nargs="+", metavar="sprite_ou_pasta",
                    help=".png, .txt (matriz) ou pasta de frames; o primeiro sprite vai no bloco 1")
    ap.add_argument("--out", required=True, help="PNG de saída")
    ap.add_argument("--ref", help="foto de referência (padrão: sprites/candidates/target/target_cutout.png, se existir)")
    ap.add_argument("--scale", type=int, default=8, help="ampliação do bloco 1 (padrão: 8)")
    ap.add_argument("--title", help="título no topo da folha")
    args = ap.parse_args()

    frames = gather_frames(args.inputs)
    ref = resolve_ref(args.ref)
    name, first = frames[0]

    blocks = [block_sprite(name, first, ref, args.scale), block_taskbar(first)]
    title = None
    if args.title:
        title = heading(args.title, load_font(18, bold=True))
    inner = max([b.width for b in blocks] + [title.width if title else 0])
    if len(frames) > 1:
        blocks.append(block_frames(frames, inner))
    blocks = ([title] if title else []) + blocks
    inner = max(b.width for b in blocks)

    sheet = Image.new("RGBA", (inner + 2 * PAD, 2 * PAD + sum(b.height for b in blocks) + GAP * (len(blocks) - 1)), BG + (255,))
    y = PAD
    for b in blocks:
        sheet.alpha_composite(b, (PAD, y))
        y += b.height + GAP
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.convert("RGB").save(out)
    print(f"folha: {out}  ({sheet.width}x{sheet.height}, {len(frames)} frame(s))")


if __name__ == "__main__":
    main()
