"""Gera a página animada de aprovação (a do artifact no claude.ai), num HTML só.

Mesmas entradas do preview_html.py ("Nome|nota|pasta do rig[|parada.png]"),
mas com canvas e controles: velocidade, taskbar clara/escura, andando/parada.
Usa sprites/tools/page_template.html e embute os PNGs e a foto de referência.
Pra atualizar o artifact, publique sempre o mesmo arquivo de saída.

Uso:
  python3 sprites/tools/page.py --out pagina.html --title "Kiara correndo" \
      --intro "..." --step 2 "Galope|6 frames|/tmp/out/run" "Trote|6 frames|/tmp/out/walk_b"
"""
import argparse
import base64
import io
import json
from html import escape
from pathlib import Path

from PIL import Image, ImageOps

from common import SPRITES_DIR

TEMPLATE = Path(__file__).with_name("page_template.html")
FOTO = SPRITES_DIR.parent / "reference" / "kiki_perfil_potinho.jpg"


def png_uri(path):
    return "data:image/png;base64," + base64.b64encode(Path(path).read_bytes()).decode()


def foto_uri(path, crop=None, size=640):
    im = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    if crop:  # frações x0,y0,x1,y1 da foto
        x0, y0, x1, y1 = (float(v) for v in crop.split(","))
        im = im.crop((int(x0 * im.width), int(y0 * im.height), int(x1 * im.width), int(y1 * im.height)))
    im.thumbnail((size, size))
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=80)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("entries", nargs="+", help='"Nome|nota|pasta do rig[|parada.png[|passo]]"')
    ap.add_argument("--out", required=True)
    ap.add_argument("--title", default="Kiara")
    ap.add_argument("--intro", default="")
    ap.add_argument("--foto", default=str(FOTO))
    ap.add_argument("--foto-crop", default="0,0.34,1,0.6", help="recorte em frações x0,y0,x1,y1")
    ap.add_argument("--foto-nota", default="Referência de perfil: corpo compacto e robusto, pernas finas, orelhas enormes.")
    ap.add_argument("--stand", default=str(SPRITES_DIR / "base" / "kiara_32.png"))
    ap.add_argument("--step", type=float, default=1, help="px do sprite que ela anda por frame na taskbar")
    args = ap.parse_args()

    variants = []
    for entry in args.entries:
        name, note, folder, *own = entry.split("|", 4)
        folder = Path(folder)
        man = json.loads((folder / "manifest.json").read_text())
        variants.append({
            "nome": escape(name), "nota": escape(note),
            "step": float(own[1]) if len(own) > 1 and own[1] else args.step,
            "durs": [f["duration"] for f in man["frames"]],
            "walk": [png_uri(folder / f["file"]) for f in man["frames"]],
            "stand": png_uri(own[0] if own and own[0] else args.stand),
        })
    data = {"foto": foto_uri(args.foto, args.foto_crop), "variants": variants}
    html = (TEMPLATE.read_text()
            .replace("__TITLE__", escape(args.title))
            .replace("__INTRO__", escape(args.intro))
            .replace("__FOTO_NOTA__", escape(args.foto_nota))
            .replace("__DATA__", json.dumps(data)))
    Path(args.out).write_text(html)
    print(f"página: {args.out} ({len(html) // 1024} KB)")


if __name__ == "__main__":
    main()
