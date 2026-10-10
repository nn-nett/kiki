"""Funções compartilhadas pelas ferramentas de sprite.

- paleta (sprites/palette.json): letra -> cor
- matrizes de caracteres (.txt): leitura, tags de encaixe (# @tag), conversão
  matriz <-> imagem
- preview ampliado sem suavização, com fundo quadriculado
- cores da taskbar do Windows 11 (pra testar contraste)
"""
import json
from pathlib import Path

from PIL import Image

SPRITES_DIR = Path(__file__).resolve().parent.parent
PALETTE_PATH = SPRITES_DIR / "palette.json"

# fundo aproximado da taskbar do Windows 11 (tema escuro / claro)
TASKBAR_DARK = (32, 32, 32)
TASKBAR_LIGHT = (243, 243, 243)

TRANSPARENT = "."


def hex2rgb(s):
    s = s.lstrip("#")
    return tuple(int(s[i : i + 2], 16) for i in (0, 2, 4))


def rgb2hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(*rgb[:3])


def load_palette():
    """{letra: (r, g, b)} de todas as cores da paleta."""
    data = json.loads(PALETTE_PATH.read_text())
    colors = {}
    for group in data["groups"].values():
        for key, info in group.items():
            colors[key] = hex2rgb(info["hex"])
    return colors


def nearest_letter(rgb, palette):
    """Letra da cor da paleta mais próxima (olho é mais sensível ao verde)."""
    best, bk = None, None
    for k, (r, g, b) in palette.items():
        d = 3 * (rgb[0] - r) ** 2 + 4 * (rgb[1] - g) ** 2 + 2 * (rgb[2] - b) ** 2
        if best is None or d < best:
            best, bk = d, k
    return bk


def parse_matrix(path):
    """Lê uma matriz .txt. Linhas começando com '#' são comentário/tag.

    Retorna (linhas, largura); linhas curtas são completadas com '.'.
    """
    rows = [
        line.rstrip("\n")
        for line in Path(path).read_text().splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    width = max(len(r) for r in rows)
    return [r.ljust(width, TRANSPARENT) for r in rows], width


def parse_tags(path):
    """Tags de encaixe no cabeçalho: '# @nome x,y' -> {'nome': (x, y)}.

    Tags sem coordenadas ('# @flag') viram {'flag': True}; texto livre
    ('# @nota olá') vira string.
    """
    tags = {}
    for line in Path(path).read_text().splitlines():
        s = line.strip()
        if not s.startswith("#"):
            continue
        s = s.lstrip("#").strip()
        if not s.startswith("@"):
            continue
        name, _, value = s[1:].partition(" ")
        value = value.strip()
        if not value:
            tags[name] = True
            continue
        try:
            x, y = (int(v) for v in value.split(","))
            tags[name] = (x, y)
        except ValueError:
            tags[name] = value
    return tags


def matrix_to_image(rows, palette=None):
    """Matriz de letras -> imagem RGBA. Erro se houver letra fora da paleta."""
    palette = palette or load_palette()
    width = max(len(r) for r in rows)
    img = Image.new("RGBA", (width, len(rows)), (0, 0, 0, 0))
    unknown = set()
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch == TRANSPARENT:
                continue
            if ch not in palette:
                unknown.add(ch)
                continue
            img.putpixel((x, y), palette[ch] + (255,))
    if unknown:
        raise ValueError(f"caracteres sem cor na paleta: {sorted(unknown)}")
    return img


def image_to_matrix(img, palette=None, snap=False):
    """Imagem -> matriz de letras.

    Pixel transparente vira '.'. Cor fora da paleta vira '?', ou a letra mais
    próxima se snap=True.
    """
    palette = palette or load_palette()
    lookup = {rgb: k for k, rgb in palette.items()}
    img = img.convert("RGBA")
    rows = []
    for y in range(img.height):
        row = []
        for x in range(img.width):
            r, g, b, a = img.getpixel((x, y))
            if a < 128:
                row.append(TRANSPARENT)
            elif (r, g, b) in lookup:
                row.append(lookup[(r, g, b)])
            else:
                row.append(nearest_letter((r, g, b), palette) if snap else "?")
        rows.append("".join(row))
    return rows


def write_matrix(path, rows, header=None):
    """Salva matriz .txt; header é uma lista de linhas de comentário/tag."""
    lines = [f"# {h}" if not h.startswith("#") else h for h in (header or [])]
    Path(path).write_text("\n".join(lines + list(rows)) + "\n")


def checkerboard(size, cell, c1=(70, 70, 76), c2=(82, 82, 90)):
    """Fundo quadriculado pra enxergar transparência."""
    w, h = size
    tile = Image.new("RGBA", (cell * 2, cell * 2), c1 + (255,))
    tile.paste(c2 + (255,), (0, 0, cell, cell))
    tile.paste(c2 + (255,), (cell, cell, cell * 2, cell * 2))
    bg = Image.new("RGBA", (w, h))
    for y in range(0, h, cell * 2):
        for x in range(0, w, cell * 2):
            bg.paste(tile, (x, y))
    return bg


def upscale(img, scale, bg=None):
    """Amplia sem suavização. bg: None (transparente), 'checker' ou (r, g, b)."""
    big = img.convert("RGBA").resize((img.width * scale, img.height * scale), Image.NEAREST)
    if bg is None:
        return big
    if bg == "checker":
        base = checkerboard(big.size, scale * 4)
    else:
        base = Image.new("RGBA", big.size, tuple(bg) + (255,))
    base.alpha_composite(big)
    return base
