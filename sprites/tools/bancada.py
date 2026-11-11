"""Bancada de desenho: monta candidatos pelo rig e gera uma folha pra conferir antes de mostrar.

Cada folha tem o spritemap ampliado (grade + régua, igual ao spritemap.py) e, embaixo, os
mesmos frames em TAMANHO REAL (2x e 3x), em fundo claro e em fundo escuro com contorno G.
O ampliado serve pra achar pixel errado; o tamanho real é o que o dono vê na taskbar, e é
nele que se decide se a pose lê bem. Também roda a checagem de buracos, pixels soltos e
entalhes do tweak.py em cada frame.

Uso em scripts de rascunho:
    import sys; sys.path.insert(0, "sprites/tools")
    from bancada import *
    show("saida.png", [("linha", frames_of("virar_B5")), ("solta", [("a", mat("..X.\\n.XX."))])])
"""
import json
from pathlib import Path

from PIL import Image

from common import SPRITES_DIR, load_palette, matrix_to_image
from rig import Rig
from spritemap import spritemap
from tweak import problems

PARTS = SPRITES_DIR / "parts" / "32"
ANIMS = SPRITES_DIR / "anims"
PAL = load_palette()


def frames_of(recipe, only=None):
    """[(rótulo, Image)] de uma receita (nome em anims/ ou dict), sem gravar nada."""
    rec = json.loads((ANIMS / f"{recipe}.json").read_text()) if isinstance(recipe, str) else recipe
    rig = Rig(PARTS)
    frs = rig.resolve_frames(rec)
    canvas = tuple(rec.get("canvas", (32, 32)))
    out = []
    for i, fr in enumerate(frs):
        if only is not None and i not in only:
            continue
        img, _, warns = rig.render_frame(fr["parts"], canvas)
        if warns:
            print("aviso", rec["name"], i, warns)
        out.append((f"f{i} · {fr['duration']} ms", img))
    return out


def mat(text):
    """Matriz de texto (letras da paleta, '#' = comentário) -> Image."""
    rows = [l for l in text.strip("\n").splitlines() if not l.startswith("#")]
    w = max(len(l) for l in rows)
    return matrix_to_image([l.ljust(w, ".") for l in rows], PAL)


def compose(parts, canvas=(32, 32)):
    """Lista de peças no formato do rig -> Image."""
    img, _, warns = Rig(PARTS).render_frame(parts, canvas)
    if warns:
        print("aviso", warns)
    return img


def outline(img):
    """Contorno G (vizinho de cima/baixo/lados), igual ao filtro da saída final."""
    g = tuple(PAL["G"]) + (255,)
    src, out = img.load(), img.copy()
    dst = out.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            if src[x, y][3]:
                continue
            if any(0 <= x + dx < w and 0 <= y + dy < h and src[x + dx, y + dy][3]
                   for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                dst[x, y] = g
    return out


def real(frames, scales=(2, 3)):
    """Tira em tamanho real: fundo claro e fundo escuro (com contorno), em cada escala."""
    pad = 6
    tall = max(im.height for _, im in frames)
    h = sum((tall * s + pad) * 2 for s in scales) + pad
    w = max(sum(im.width * s + pad for _, im in frames) for s in scales) + pad
    sheet = Image.new("RGBA", (w, h), (243, 243, 243, 255))
    y = pad
    for s in scales:
        for dark in (False, True):
            band = Image.new("RGBA", (w, tall * s + pad), (32, 32, 32, 255) if dark else (243, 243, 243, 255))
            sheet.paste(band, (0, y - pad // 2))
            x = pad
            for _, im in frames:
                src = outline(im) if dark else im
                sheet.alpha_composite(src.resize((im.width * s, im.height * s), Image.NEAREST), (x, y))
                x += im.width * s + pad
            y += tall * s + pad
    return sheet.convert("RGB")


def show(path, rows, zoom=10, with_real=True):
    """Grava a folha em `path`: rows = [(nome da linha, [(rótulo, Image)])]."""
    big = spritemap(rows, zoom)
    if with_real:
        strips = [real(frames) for _, frames in rows]
        sheet = Image.new("RGB", (max([big.width] + [s.width + 16 for s in strips]),
                                  big.height + sum(s.height + 8 for s in strips)), (243, 243, 243))
        sheet.paste(big, (0, 0))
        y = big.height
        for s in strips:
            sheet.paste(s, (16, y))
            y += s.height + 8
        big = sheet
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    big.save(path)
    for label, frames in rows:
        for fl, im in frames:
            holes, loose, notches = problems(im)
            if holes or loose or notches:
                print(f"conferir {label} / {fl}: buracos={holes} soltos={loose} entalhes={sorted(notches)}")
    print("->", path, big.size)
    return path


def diff(a, b):
    """Quantos pixels mudam de um frame pro outro."""
    pa, pb = a.load(), b.load()
    return sum(1 for y in range(a.height) for x in range(a.width) if pa[x, y] != pb[x, y])
