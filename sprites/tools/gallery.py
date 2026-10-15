"""Gera a "Galeria da Kiara": página com todas as animações já aprovadas.

Lê SÓ os arquivos finais (final/kiara-sprites.png + .json, que é o que o app vai
usar) e a lista final/aprovadas.json, então serve de prova de que o que foi
aprovado está guardado e funcionando. Também mostra o checklist da Fase 0 tirado
do CLAUDE.md. O export_final.py chama este script no fim, então a galeria é
refeita a cada aprovação; depois é só republicar o artifact com o mesmo arquivo.

Uso:
  python3 sprites/tools/gallery.py [--out sprites/final/galeria.html]
"""
import argparse
import base64
import io
import json
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from PIL import Image

from common import SPRITES_DIR
from spritemap import spritemap

FINAL = SPRITES_DIR / "final"
TEMPLATE = Path(__file__).with_name("gallery_template.html")
CLAUDE_MD = SPRITES_DIR.parent / "CLAUDE.md"
REPO_URL = "https://github.com/nn-nett/kiki/tree/claude/charming-gates-tf2lki/sprites/final"


def checklist():
    """Itens do checklist da Fase 0 no CLAUDE.md: [{feito, nome}]."""
    text = CLAUDE_MD.read_text()
    block = text.split("## Fase 0 — checklist", 1)[-1].split("\n## ", 1)[0]
    items = []
    for line in block.splitlines():
        m = re.match(r"- \[( |x)\] (.*)", line)
        if not m:
            continue
        name = m.group(2).replace("✅", "").strip()
        name = re.split(r" — | \(", name, maxsplit=1)[0]
        name = re.sub(r"[`*]", "", name).strip()
        items.append({"feito": m.group(1) == "x", "nome": name})
    return items


def mapa_uri(meta, approved):
    """Spritemap (frames numerados, grade e régua) das versões normais, recortado da folha final."""
    sheet = Image.open(FINAL / meta["sheet"]).convert("RGBA")
    rows = []
    crop = lambda f: sheet.crop((f["x"], f["y"], f["x"] + f["w"], f["y"] + f["h"]))
    for key, info in approved.items():
        comp = info.get("composicao")
        if not comp:
            frames = meta["animations"][key]["frames"]
            rows.append((key, [(f"f{i} · {f['duration_ms']} ms", crop(f)) for i, f in enumerate(frames)]))
            continue
        # corpo + expressão: cada frame do corpo com cada frame da expressão por cima
        expr = meta["expressoes"][comp["expressao"]]
        cells = []
        for i, f in enumerate(meta["animations"][comp["corpo"]]["frames"]):
            for j, e in enumerate(expr["frames"]):
                im = crop(f)
                im.alpha_composite(Image.open(FINAL / e["img"]).convert("RGBA"), tuple(f[expr["ancora"]]))
                cells.append((f"f{i} + {comp['expressao']} {j}", im))
        rows.append((f"{key} ({comp['corpo']} + {comp['expressao']}, cada um no seu ritmo)", cells))
    buf = io.BytesIO()
    img = spritemap(rows)
    img.save(buf, "PNG")
    img.save(FINAL / "spritemap.png")  # o mesmo PNG solto, pra mandar junto e abrir fora da página
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(FINAL / "galeria.html"))
    args = ap.parse_args()

    meta = json.loads((FINAL / "kiara-sprites.json").read_text())
    approved = {k: v for k, v in json.loads((FINAL / "aprovadas.json").read_text()).items()
                if not k.startswith("_")}
    sheet = "data:image/png;base64," + base64.b64encode((FINAL / meta["sheet"]).read_bytes()).decode()
    now = datetime.now(ZoneInfo("America/Sao_Paulo"))
    data = {
        "sheet": sheet,
        "meta": meta,
        "aprovadas": [{"key": k, "nota": v.get("aprovada", ""), "receita": v.get("recipe"),
                       "composicao": v.get("composicao")} for k, v in approved.items()],
        "checklist": checklist(),
        "mapa": mapa_uri(meta, approved),
        # remendos do piscar (expressão desacoplada), lidos de final/expressoes/
        # remendos das expressões (piscar, ofegante), lidos de final/expressoes/
        "olhos": {fr[k]: "data:image/png;base64," + base64.b64encode((FINAL / fr[k]).read_bytes()).decode()
                  for e in meta.get("expressoes", {}).values() for fr in e["frames"]
                  for k in ("img", "img_esquerda", "img_contorno", "img_contorno_esquerda") if k in fr},
        "atualizada": now.strftime("%d/%m/%Y %H:%M"),
        "repo": REPO_URL,
    }
    html = TEMPLATE.read_text().replace("__DATA__", json.dumps(data))
    Path(args.out).write_text(html)
    print(f"galeria: {args.out} ({len(html) // 1024} KB, {len(approved)} animações aprovadas)")


if __name__ == "__main__":
    main()
