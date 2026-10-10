"""Imagem A/B pra um juiz rápido: "qual parece mais com a FOTO?".

Monta lado a lado, do mesmo tamanho, os painéis A, B e FOTO (a referência, na
mesma altura; sem --ref usa sprites/candidates/target/target_cutout.png se
existir). A imagem nunca diz qual é o "antes" e qual é o "depois": quem é A e
quem é B sai no stdout, em JSON.

--region x0,y0,x1,y1 (em pixels do sprite, x1/y1 exclusivos) marca a região com
um retângulo magenta nos painéis A e B e acrescenta uma segunda linha com o
recorte dela bem ampliado. --shuffle sorteia se A=antes ou A=depois, pra o juiz
não ter viés de posição.

Uso:
  python3 sprites/tools/compare.py antes.png depois.png --out ab.png \
      --ref foto.png --label "orelhas" --region 6,0,18,8 --shuffle
  # stdout: {"A": "depois", "B": "antes"}
"""
import argparse
import json
import random
import sys
from pathlib import Path

from PIL import Image, ImageDraw

from common import upscale
from lint import load_sprite
from review import BG, FG, ACCENT, load_font, load_ref, put, resolve_ref, text_width

MAGENTA = (255, 0, 255, 255)
MARGIN = 4
GAP = 24
CROP_TARGET = 280  # lado maior (px) do recorte ampliado da região


def parse_region(text):
    try:
        x0, y0, x1, y1 = (int(v) for v in text.split(","))
    except ValueError:
        raise argparse.ArgumentTypeError("use x0,y0,x1,y1 (inteiros), ex.: 6,0,18,8")
    if x1 <= x0 or y1 <= y0:
        raise argparse.ArgumentTypeError("x1,y1 têm que ser maiores que x0,y0 (x1/y1 são exclusivos)")
    return x0, y0, x1, y1


def sprite_panel(img, size, scale, region):
    """Sprite ampliado sobre quadriculado, no canvas `size`, com a região marcada."""
    w, h = size
    canvas = Image.new("RGBA", (w * scale, h * scale))
    canvas.alpha_composite(upscale(Image.new("RGBA", size), scale, bg="checker"))
    canvas.alpha_composite(upscale(img, scale))
    panel = Image.new("RGBA", (canvas.width + 2 * MARGIN, canvas.height + 2 * MARGIN), BG + (255,))
    panel.alpha_composite(canvas, (MARGIN, MARGIN))
    if region:
        x0, y0, x1, y1 = region
        ImageDraw.Draw(panel).rectangle(
            [MARGIN + x0 * scale - 2, MARGIN + y0 * scale - 2, MARGIN + x1 * scale + 1, MARGIN + y1 * scale + 1],
            outline=MAGENTA, width=2)
    return panel


def labeled(img, label, font):
    out = Image.new("RGBA", (max(img.width, text_width(label, font)), img.height + 30), BG + (255,))
    put(ImageDraw.Draw(out), label, 0, 2, font, ACCENT)
    out.alpha_composite(img, (0, 30))
    return out


def row(items):
    """Alinha imagens lado a lado pelo topo, com GAP entre elas."""
    out = Image.new("RGBA", (sum(i.width for i in items) + GAP * (len(items) - 1), max(i.height for i in items)),
                    BG + (255,))
    x = 0
    for i in items:
        out.alpha_composite(i, (x, 0))
        x += i.width + GAP
    return out


def main():
    ap = argparse.ArgumentParser(description="Gera a imagem A/B (A | B | FOTO) pra um juiz.")
    ap.add_argument("antes", help="sprite antes (.png ou .txt)")
    ap.add_argument("depois", help="sprite depois (.png ou .txt)")
    ap.add_argument("--out", required=True, help="PNG de saída")
    ap.add_argument("--ref", help="foto de referência (padrão: sprites/candidates/target/target_cutout.png, se existir)")
    ap.add_argument("--label", default="aparência geral", help='critério do juiz, ex.: "orelhas"')
    ap.add_argument("--region", type=parse_region, metavar="x0,y0,x1,y1",
                    help="região a destacar, em pixels do sprite (x1,y1 exclusivos)")
    ap.add_argument("--shuffle", action="store_true", help="sorteia quem é A e quem é B")
    ap.add_argument("--scale", type=int, default=8, help="ampliação dos painéis (padrão: 8)")
    args = ap.parse_args()

    sprites = {}
    for nome, path in (("antes", args.antes), ("depois", args.depois)):
        try:
            sprites[nome] = load_sprite(path)
        except (OSError, ValueError) as e:
            sys.exit(f"ERRO: não consegui ler {path}: {e}")
    ref = resolve_ref(args.ref)
    if not ref:
        print("aviso: sem foto de referência (use --ref); painel FOTO omitido", file=sys.stderr)

    order = ["antes", "depois"]
    if args.shuffle:
        random.shuffle(order)
    mapping = {"A": order[0], "B": order[1]}
    imgs = {k: sprites[v] for k, v in mapping.items()}

    size = (max(i.width for i in imgs.values()), max(i.height for i in imgs.values()))
    region = args.region
    if region:
        x0, y0, x1, y1 = region
        if x0 < 0 or y0 < 0 or x1 > size[0] or y1 > size[1]:
            sys.exit(f"ERRO: região {x0},{y0},{x1},{y1} fora do canvas {size[0]}x{size[1]}")

    f_label, f_title = load_font(18, bold=True), load_font(16, bold=True)
    panels = [labeled(sprite_panel(imgs[k], size, args.scale, region), k, f_label) for k in "AB"]
    if ref:
        photo = load_ref(ref, size[1] * args.scale + 2 * MARGIN)
        panels.append(labeled(photo, "FOTO", f_label))
    rows = [row(panels)]

    if region:
        rw, rh = x1 - x0, y1 - y0
        zoom = max(args.scale, min(48, CROP_TARGET // max(rw, rh)))
        f_small = load_font(12, bold=True)
        crops = []
        for k in "AB":
            crop = upscale(imgs[k].crop(region), zoom, bg="checker")
            crops.append(labeled(crop, f"{k} - região {x0},{y0} a {x1},{y1} ({zoom}x)", f_small))
        rows.append(row(crops))

    if ref:
        title = f"Critério: {args.label} — qual parece mais com a FOTO?"
    else:
        title = f"Critério: {args.label} — qual está melhor?"
    head = Image.new("RGBA", (text_width(title, f_title), 28), BG + (255,))
    put(ImageDraw.Draw(head), title, 0, 0, f_title, FG)

    parts = [head] + rows
    pad = 16
    width = max(p.width for p in parts) + 2 * pad
    height = 2 * pad + sum(p.height for p in parts) + GAP * (len(parts) - 1)
    sheet = Image.new("RGBA", (width, height), BG + (255,))
    y = pad
    for p in parts:
        sheet.alpha_composite(p, (pad, y))
        y += p.height + GAP
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.convert("RGB").save(out)

    print(f"ab: {out} ({width}x{height})", file=sys.stderr)
    print(json.dumps(mapping, ensure_ascii=False))


if __name__ == "__main__":
    main()
