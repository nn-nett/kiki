"""Exporta as animações aprovadas (final/aprovadas.json) como arquivos finais.

Para cada animação aprovada, monta os frames com o rig e grava em
final/frames/<nome>/ quatro versões: normal, esquerda (espelhada), contorno
(borda G) e contorno_esquerda. Depois empacota tudo com pack.py em
final/kiara-sprites.png + final/kiara-sprites.json (células 32x32, durações,
loop, step_px e frames no ar), o formato que o app desktop e o Android leem.

Uso:
  python3 sprites/tools/export_final.py
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

from common import SPRITES_DIR

FINAL = SPRITES_DIR / "final"
TOOLS = SPRITES_DIR / "tools"


def render(recipe, tmp):
    subprocess.run([sys.executable, str(TOOLS / "rig.py"), str(SPRITES_DIR / "anims" / f"{recipe}.json"),
                    "--parts", str(SPRITES_DIR / "parts" / "32"), "--out", str(tmp)], check=True, stdout=subprocess.DEVNULL)
    return json.loads((SPRITES_DIR / "anims" / f"{recipe}.json").read_text())


def load(folder):
    man = json.loads((folder / "manifest.json").read_text())
    return [(Image.open(folder / f["file"]).convert("RGBA"), f["duration"]) for f in man["frames"]], man


def main():
    approved = {k: v for k, v in json.loads((FINAL / "aprovadas.json").read_text()).items()
                if not k.startswith("_")}
    frames_dir = FINAL / "frames"
    if frames_dir.exists():
        shutil.rmtree(frames_dir)
    spec = {"out": "kiara-sprites", "animations": {}}
    extra = {}
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for name, info in approved.items():
            recipe = render(info["recipe"], tmp)
            rname = recipe["name"]
            airborne = [i for i, fr in enumerate(recipe["frames"]) if fr.get("airborne")]
            outline = tmp / f"{rname}_contorno"
            if not outline.exists():  # receita sem variante contorno: aplica o filtro
                from filters import FILTERS
                outline.mkdir()
                fr, man = load(tmp / rname)
                for (im, _), f in zip(fr, man["frames"]):
                    FILTERS["outline"](im, color="G").save(outline / f["file"])
                (outline / "manifest.json").write_text(json.dumps(man))
            for suffix, folder, flip in (("", tmp / rname, False), ("_esquerda", tmp / rname, True),
                                         ("_contorno", outline, False),
                                         ("_contorno_esquerda", outline, True)):
                fr, man = load(folder)
                dst = frames_dir / name
                dst.mkdir(parents=True, exist_ok=True)
                files = []
                for i, (im, _) in enumerate(fr):
                    if flip:
                        im = im.transpose(Image.FLIP_LEFT_RIGHT)
                    f = dst / f"{name}{suffix}_{i}.png"
                    im.save(f)
                    files.append(str(f.relative_to(FINAL)))
                anim = name + suffix
                spec["animations"][anim] = {"frames": files, "durations": [d for _, d in fr],
                                            "loop": man.get("loop", True)}
                extra[anim] = {"step_px": info.get("step_px", 0) * (-1 if flip else 1),
                               "airborne_frames": airborne}
            print(f"{name}: {len(fr)} frames x 4 versões")
    spec_path = FINAL / "spec.json"
    spec_path.write_text(json.dumps(spec, indent=2) + "\n")
    subprocess.run([sys.executable, str(TOOLS / "pack.py"), str(spec_path), str(FINAL)], check=True)
    meta_path = FINAL / "kiara-sprites.json"
    meta = json.loads(meta_path.read_text())
    for anim, e in extra.items():
        meta["animations"][anim].update(e)
    meta["_comment"] = ("step_px: px do sprite que a janela anda por frame (negativo = pra esquerda); "
                        "airborne_frames: frames com as patas fora do chão")
    meta_path.write_text(json.dumps(meta, indent=2) + "\n")


if __name__ == "__main__":
    main()
