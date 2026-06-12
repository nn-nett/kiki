"""Empacota frames em um spritesheet único + JSON de metadados.

O JSON descreve cada animação (frames, duração de cada um, loop) com as
coordenadas no sheet — formato compartilhado entre desktop (Electron) e
Android (Kotlin).

O spec de entrada é um JSON:
{
  "out": "kiara-sprites",
  "animations": {
    "walk":  { "frames": ["f0.png", "f1.png"], "durations": [280, 280], "loop": true },
    "sleep": { "frames": ["s0.png"], "durations": [1000], "loop": true }
  }
}

Uso:
  python3 sprites/tools/pack.py spec.json saida_dir
"""
import argparse
import json
from pathlib import Path

from PIL import Image


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("outdir")
    args = ap.parse_args()

    spec_path = Path(args.spec)
    spec = json.loads(spec_path.read_text())
    base = spec_path.parent
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    # carrega todos os frames (frames repetidos entre animações entram 1x)
    unique = {}   # caminho -> (Image, index)
    order = []
    for anim in spec["animations"].values():
        for f in anim["frames"]:
            if f not in unique:
                img = Image.open(base / f).convert("RGBA")
                unique[f] = img
                order.append(f)

    cell_w = max(i.width for i in unique.values())
    cell_h = max(i.height for i in unique.values())
    sheet = Image.new("RGBA", (cell_w * len(order), cell_h), (0, 0, 0, 0))
    coords = {}
    for n, f in enumerate(order):
        img = unique[f]
        x = n * cell_w + (cell_w - img.width) // 2
        y = cell_h - img.height  # alinha pela base
        sheet.alpha_composite(img, (x, y))
        coords[f] = {"x": n * cell_w, "y": 0, "w": cell_w, "h": cell_h}

    name = spec.get("out", "sprites")
    sheet_file = outdir / f"{name}.png"
    sheet.save(sheet_file)

    meta = {
        "sheet": sheet_file.name,
        "cell": {"w": cell_w, "h": cell_h},
        "animations": {},
    }
    for anim_name, anim in spec["animations"].items():
        durations = anim["durations"]
        if len(durations) == 1:
            durations = durations * len(anim["frames"])
        meta["animations"][anim_name] = {
            "loop": anim.get("loop", True),
            "frames": [
                {**coords[f], "duration_ms": d}
                for f, d in zip(anim["frames"], durations)
            ],
        }
    meta_file = outdir / f"{name}.json"
    meta_file.write_text(json.dumps(meta, indent=2) + "\n")
    print(f"sheet: {sheet_file}  ({sheet.width}x{sheet.height}, {len(order)} células)")
    print(f"meta:  {meta_file}")


if __name__ == "__main__":
    main()
