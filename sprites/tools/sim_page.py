"""Gera a simulação "Kiara na taskbar": uma página com a Kiara vivendo numa taskbar
do Windows 11, decidindo sozinha (ao acaso) entre ficar parada, andar, latir parada
e latir andando. É uma prévia do comportamento da Fase 1, feita só com animações
aprovadas.

Como a cabeça é uma peça separada, a página monta cada frame por camadas
(pernas, tronco, cabeça), igual ao rig: assim dá pra latir andando (pernas do
trote + cabeça do latido) sem desenhar frames novos. Antes de gravar, o script
confere que as camadas recompõem pixel a pixel os frames do rig (walk_b e o
latido escolhido).

Uso:
  python3 sprites/tools/sim_page.py --out kiara_na_taskbar.html
"""
import argparse
import base64
import io
import json
import tempfile
from pathlib import Path

from PIL import Image

from common import SPRITES_DIR, TASKBAR_DARK, TASKBAR_LIGHT, load_palette
from rig import Rig

PARTS = SPRITES_DIR / "parts" / "32"
ANIMS = SPRITES_DIR / "anims"
TEMPLATE = Path(__file__).with_name("sim_template.html")
CANVAS = (32, 32)


def png_uri(img):
    buf = io.BytesIO()
    img.save(buf, "PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def layer(rig, part_name, origin):
    """A peça sozinha num quadro 32x32, na posição dela (sem offset)."""
    img = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    src = rig.part(part_name).image
    img.paste(src, origin, src)
    return img


def frame_spec(parts):
    """Do frame resolvido do rig pra {pernas, tronco, cabeça, offsets}."""
    by_role = {}
    for p in parts:
        role = "legs" if p["part"].startswith("legs") else (
            "head" if p["part"].startswith("head") else "torso")
        by_role[role] = p
    torso = by_role.get("torso", {})
    head = by_role.get("head", {})
    return {
        "legs": by_role["legs"]["part"],
        "torso": torso.get("part", "torso"),
        "torsoOff": list(torso.get("offset", [0, 0])),
        "head": head.get("part", "head"),
        "headOff": list(head.get("offset", [0, 0])),
    }


def upper_to_layers(recipe):
    """Receita com 'upper' (peça única) -> mesma receita com torso + head."""
    recipe = json.loads(json.dumps(recipe))
    for fr in recipe["frames"]:
        for p in fr.get("parts", []):
            if p.get("part") == "upper":
                p["part"], p["id"] = "torso", "torso"
        for pid, change in list(fr.get("set", {}).items()):
            if pid == "upper":
                fr["set"]["torso"] = fr["set"].pop("upper")
        if "parts" in fr and not any(p.get("part", "").startswith("head") for p in fr["parts"]):
            fr["parts"].append({"id": "head", "part": "head", "attach": "torso.pescoco"})
    return recipe


def compose(layers, spec):
    img = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    tx, ty = spec["torsoOff"]
    hx, hy = spec["headOff"]
    for name, (dx, dy) in ((spec["legs"], (0, 0)), (spec["torso"], (tx, ty)),
                           (spec["head"], (tx + hx, ty + hy))):
        src = layers[name]
        shifted = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
        shifted.paste(src, (dx, dy), src)
        img.alpha_composite(shifted)
    return img


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--walk", default="walk_b")
    ap.add_argument("--bark", default="latir_tranco")
    ap.add_argument("--stand", default="stand_head")
    ap.add_argument("--au-head", default="head_bark2", help="cabeça do AU! (conta os latidos)")
    ap.add_argument("--run", default="", help="receita de corrida (opcional, entra marcada como teste)")
    ap.add_argument("--run-step", type=int, default=2, help="px do sprite por frame na corrida")
    args = ap.parse_args()

    rig = Rig(PARTS)
    recipes = {k: json.loads((ANIMS / f"{v}.json").read_text())
               for k, v in (("walk", args.walk), ("bark", args.bark), ("stand", args.stand),
                            ("run", args.run)) if v}
    walk_layers = upper_to_layers(recipes["walk"])
    resolved = {"walk": rig.resolve_frames(walk_layers), "bark": rig.resolve_frames(recipes["bark"]),
                "stand": rig.resolve_frames(recipes["stand"])}
    if "run" in recipes:
        resolved["run"] = rig.resolve_frames(recipes["run"])

    # posição de cada peça (sem offset) e as camadas 32x32
    layers = {}
    for frames in resolved.values():
        for fr in frames:
            parts = [{k: v for k, v in p.items() if k != "offset"} for p in fr["parts"]]
            for pid, origin in rig.origins(parts).items():
                name = next(p["part"] for p in parts if p.get("id", p["part"]) == pid)
                layers.setdefault(name, layer(rig, name, origin))

    specs = {k: [frame_spec(fr["parts"]) for fr in v] for k, v in resolved.items()}
    durs = {k: [fr["duration"] for fr in v] for k, v in resolved.items()}
    seq = {k: recipes[k].get("sequence", list(range(len(resolved[k])))) for k in recipes}

    # prova: as camadas recompõem os frames do rig
    with tempfile.TemporaryDirectory() as tmp:
        for key in [k for k in ("walk", "bark", "run") if k in recipes]:
            name = recipes[key]["name"]
            rig.build(walk_layers if key == "walk" else recipes[key], tmp)
            man = json.loads((Path(tmp) / name / "manifest.json").read_text())
            for i, f in zip(seq[key], man["frames"]):
                ref = Image.open(Path(tmp) / name / f["file"]).convert("RGBA")
                got = compose(layers, specs[key][i])
                if ref.tobytes() != got.tobytes():
                    raise SystemExit(f"camadas não batem com o rig em {name} frame {i}")
        rig.build(recipes["walk"], Path(tmp) / "orig")
        for i in range(len(specs["walk"])):
            a = Image.open(Path(tmp) / "orig" / recipes["walk"]["name"] / f"{recipes['walk']['name']}_{i}.png")
            if a.convert("RGBA").tobytes() != compose(layers, specs["walk"][i]).tobytes():
                raise SystemExit(f"torso+head não bate com upper no frame {i} do andar")
    print("camadas conferidas: recompõem " + ", ".join(k for k in ("walk", "bark", "run") if k in recipes)
          + " pixel a pixel")

    palette = load_palette()
    data = {
        "layers": {k: png_uri(v) for k, v in layers.items()},
        "walk": {"frames": specs["walk"], "durs": durs["walk"], "seq": seq["walk"], "step": 1},
        "bark": {"frames": specs["bark"], "durs": durs["bark"], "seq": seq["bark"], "au": args.au_head},
        "stand": specs["stand"][0],
        "run": ({"frames": specs["run"], "durs": durs["run"], "seq": seq["run"], "step": args.run_step}
                if "run" in recipes else None),
        "outline": "#%02x%02x%02x" % palette["G"],
        "taskbar": {"light": "#%02x%02x%02x" % TASKBAR_LIGHT, "dark": "#%02x%02x%02x" % TASKBAR_DARK},
    }
    html = TEMPLATE.read_text().replace("__DATA__", json.dumps(data))
    Path(args.out).write_text(html)
    print(f"página: {args.out} ({len(html) // 1024} KB, {len(layers)} camadas)")


if __name__ == "__main__":
    main()
