"""Gera um HTML único (offline, sem JavaScript) pra ver animações do rig.

Cada animação vira GIFs embutidos no próprio arquivo: a cachorra ampliada
andando, ela parada, e ela passeando de um lado pro outro numa taskbar do
Windows 11 em tamanho real (2x). Abre em qualquer navegador, inclusive no
celular, sem internet.

Cada entrada é "Nome|nota|pasta[|parada.png]", onde a pasta é uma saída do
rig.py (com manifest.json: ordem dos frames e duração de cada um). O 4º campo,
opcional, troca a pose parada daquele cartão (o padrão é a de --stand).

Uso:
  python3 sprites/tools/preview_html.py --out kiara.html --stand sprites/base/kiara_32.png \
      "Trote B|6 frames|/tmp/out/walk_b" "Trote A|4 frames|/tmp/out/walk_a"
"""
import argparse
import base64
import io
import json
from html import escape
from pathlib import Path

from PIL import Image

from common import TASKBAR_LIGHT, upscale

ZOOM, BAR_SCALE, BAR_W, BAR_H = 6, 2, 360, 76


def gif_bytes(frames, durations, bg):
    """GIF em memória; fundo sólido (GIF não tem alpha bom)."""
    out = []
    for im in frames:
        c = Image.new("RGBA", im.size, bg + (255,))
        c.alpha_composite(im.convert("RGBA"))
        out.append(c.convert("P", palette=Image.ADAPTIVE))
    buf = io.BytesIO()
    out[0].save(buf, "GIF", save_all=True, append_images=out[1:],
                duration=list(durations), loop=0, disposal=2)
    return buf.getvalue()


def data_uri(raw, mime):
    return f"data:{mime};base64," + base64.b64encode(raw).decode()


def load_anim(folder):
    folder = Path(folder)
    man = json.loads((folder / "manifest.json").read_text())
    frames = [Image.open(folder / f["file"]).convert("RGBA") for f in man["frames"]]
    durs = [f["duration"] for f in man["frames"]]
    return frames, durs


def taskbar_walk(frames, durs, bg):
    """Ela atravessa a barra e volta (espelhada), 1 px do sprite por frame."""
    w = frames[0].width * BAR_SCALE
    x, d, i = 6, 1, 0
    seq, seq_d = [], []
    for _ in range(2 * ((BAR_W - w - 12) // BAR_SCALE)):
        f = upscale(frames[i % len(frames)], BAR_SCALE)
        if d < 0:
            f = f.transpose(Image.FLIP_LEFT_RIGHT)
        c = Image.new("RGBA", (BAR_W, BAR_H), (0, 0, 0, 0))
        c.alpha_composite(f, (x, BAR_H - f.height - 4))
        seq.append(c)
        seq_d.append(durs[i % len(durs)])
        i += 1
        x += d * BAR_SCALE
        if x > BAR_W - w - 6:
            d = -1
        if x < 6:
            d = 1
    return gif_bytes(seq, seq_d, bg)


CSS = """
:root { --bg:#f1eee9; --surface:#fbfaf7; --ink:#1d1b1a; --muted:#6b645d; --line:#ddd6cc; --accent:#b5652f; }
@media (prefers-color-scheme: dark) { :root { --bg:#161514; --surface:#1f1d1b; --ink:#f0ebe4; --muted:#a39a90; --line:#34302c; --accent:#d08a52; color-scheme: dark; } }
* { box-sizing: border-box; }
body { margin:0; background:var(--bg); color:var(--ink); font: 15px/1.5 system-ui, -apple-system, "Segoe UI", sans-serif; }
.wrap { max-width: 980px; margin: 0 auto; padding: 24px 16px 48px; display: grid; gap: 18px; }
h1 { margin: 0; font-size: clamp(26px, 6vw, 38px); letter-spacing: .01em; }
header p { margin: 6px 0 0; color: var(--muted); max-width: 62ch; }
.cards { display: grid; gap: 16px; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); }
.card { background: var(--surface); border: 1px solid var(--line); border-radius: 12px; padding: 14px; display: grid; gap: 10px; min-width: 0; }
.card h2 { margin: 0; font-size: 20px; }
.card h2 small { font-size: 13px; color: var(--muted); font-weight: 400; margin-left: 6px; }
.zoom { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
figure { margin: 0; display: grid; gap: 4px; justify-items: center; }
figcaption { font-size: 12px; color: var(--muted); text-transform: uppercase; letter-spacing: .05em; }
img { image-rendering: pixelated; image-rendering: crisp-edges; display: block; max-width: 100%; height: auto; border-radius: 8px; }
.zoom img { width: 100%; }
.bar { width: 100%; }
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("entries", nargs="+", help='"Nome|nota|pasta do rig[|parada.png]"')
    ap.add_argument("--out", required=True)
    ap.add_argument("--stand", required=True, help="PNG da pose parada")
    ap.add_argument("--title", default="Kiara andando")
    ap.add_argument("--intro", default="")
    args = ap.parse_args()

    bg = TASKBAR_LIGHT
    stand = Image.open(args.stand).convert("RGBA")
    stand_uri = data_uri(gif_bytes([upscale(stand, ZOOM)], [1000], bg), "image/gif")
    cards = []
    for entry in args.entries:
        name, note, folder, *own = entry.split("|", 3)
        card_stand = stand_uri
        if own:
            im = Image.open(own[0]).convert("RGBA")
            card_stand = data_uri(gif_bytes([upscale(im, ZOOM)], [1000], bg), "image/gif")
        frames, durs = load_anim(folder)
        zoom = data_uri(gif_bytes([upscale(f, ZOOM) for f in frames], durs, bg), "image/gif")
        bar = data_uri(taskbar_walk(frames, durs, bg), "image/gif")
        cards.append(f"""
  <section class="card">
    <h2>{escape(name)}<small>{escape(note)}</small></h2>
    <div class="zoom">
      <figure><img src="{zoom}" alt="{escape(name)} andando, ampliada"><figcaption>andando</figcaption></figure>
      <figure><img src="{card_stand}" alt="Kiara parada, ampliada"><figcaption>parada</figcaption></figure>
    </div>
    <img class="bar" src="{bar}" alt="{escape(name)} passeando na taskbar">
  </section>""")
    html = f"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(args.title)}</title><style>{CSS}</style></head>
<body><div class="wrap">
  <header><h1>{escape(args.title)}</h1><p>{escape(args.intro)}</p></header>
  <div class="cards">{''.join(cards)}
  </div>
</div></body></html>
"""
    Path(args.out).write_text(html)
    print(f"html: {args.out} ({len(html)//1024} KB)")


if __name__ == "__main__":
    main()
