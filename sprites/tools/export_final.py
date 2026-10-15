"""Exporta as animações aprovadas (final/aprovadas.json) como arquivos finais.

Para cada animação aprovada, monta os frames com o rig e grava em
final/frames/<nome>/ quatro versões: normal, esquerda (espelhada), contorno
(borda G) e contorno_esquerda. Depois empacota tudo com pack.py em
final/kiara-sprites.png + final/kiara-sprites.json (células 32x32, durações,
loop, step_px e frames no ar), o formato que o app desktop e o Android leem.

Expressões desacopladas (pedido do dono: "piscar, latir, tudo desacoplado"): o
piscar sai como remendos pequenos do olho em final/expressoes/ e cada frame de
cada animação leva "olho": [x, y], o canto onde o remendo cai na célula (null
quando a animação já mexe no olho). O app pisca por cima de qualquer animação.
O ponto vem do pixel E de cima do olho (é o @socket.olho das cabeças) e é
conferido contra o "piscando" montado pelo rig.

Do mesmo jeito o ofegante sai como remendo da boca (final/expressoes/boca_*),
com "boca": [x, y] por frame, pra tocar no ritmo dele (130 ms) por cima de um
corpo em outro ritmo (ex.: andando, 100 ms). Entradas de aprovadas.json com
"composicao" ({"corpo", "expressao"}) não geram frames: vão pro JSON como
"composicoes" e o app toca o corpo e a expressão juntos, cada um no seu relógio.

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

from common import SPRITES_DIR, load_palette
from rig import Rig

FINAL = SPRITES_DIR / "final"
TOOLS = SPRITES_DIR / "tools"
PARTS = SPRITES_DIR / "parts" / "32"
# piscar: remendos do olho (rig: olho_meio/olho_fechado, @anchor 1,0) e a ordem do piscar
BLINK = [("olho_meio", 60), ("olho_fechado", 110), ("olho_meio", 60)]
BLINK_EVERY_MS = [2500, 7000]
# ofegante: remendo da boca recortado das cabeças ofegantes (só a boca muda em relação à head.txt)
PANT = [("boca_ofegante1", "head_ofegante1", 130), ("boca_ofegante2", "head_ofegante2", 130)]
MOUTH_BOX = (10, 13, 15, 18)          # recorte na cabeça (x0, y0, x1, y1), cobre tudo o que muda
FACE_PARTS = {"head": (0, 0), "upper": (16, 0)}   # peça com a cara normal -> canto da cabeça dentro dela


def render(recipe, tmp):
    subprocess.run([sys.executable, str(TOOLS / "rig.py"), str(SPRITES_DIR / "anims" / f"{recipe}.json"),
                    "--parts", str(SPRITES_DIR / "parts" / "32"), "--out", str(tmp)], check=True, stdout=subprocess.DEVNULL)
    return json.loads((SPRITES_DIR / "anims" / f"{recipe}.json").read_text())


def load(folder):
    man = json.loads((folder / "manifest.json").read_text())
    return [(Image.open(folder / f["file"]).convert("RGBA"), f["duration"]) for f in man["frames"]], man


def eye_corner(im, anchor):
    """Canto do remendo do olho na célula: o pixel E de cima do olho menos a âncora do remendo."""
    eye = tuple(load_palette()["E"])
    pts = [(y, x) for y in range(im.height) for x in range(im.width)
           if im.getpixel((x, y))[3] and im.getpixel((x, y))[:3] == eye]
    if not pts:
        return None
    y, x = min(pts)
    return [x - anchor[0], y - anchor[1]]


def export_blink(meta, recipes):
    """Grava os remendos do piscar e põe "olho" em cada frame; confere contra o "piscando" do rig."""
    rig = Rig(PARTS)
    dst = FINAL / "expressoes"
    dst.mkdir(exist_ok=True)
    patches = {}
    for name in dict.fromkeys(n for n, _ in BLINK):
        part = rig.part(name)
        img = part.image
        img.save(dst / f"{name}.png")
        img.transpose(Image.FLIP_LEFT_RIGHT).save(dst / f"{name}_esquerda.png")
        patches[name] = (img, part.anchor)
    sheet = Image.open(FINAL / meta["sheet"]).convert("RGBA")
    cells = {}
    for anim, a in meta["animations"].items():
        base = anim.replace("_contorno", "").replace("_esquerda", "")
        uses_eye = any(p.get("part", "").startswith("olho")
                       for fr in recipes[base]["frames"] for p in fr.get("parts", []))
        cells[anim] = []
        for f in a["frames"]:
            im = sheet.crop((f["x"], f["y"], f["x"] + f["w"], f["y"] + f["h"]))
            cells[anim].append(im)
            if uses_eye:
                f["olho"] = None
                continue
            flip = anim.endswith("_esquerda")
            pos = eye_corner(im.transpose(Image.FLIP_LEFT_RIGHT) if flip else im, patches[BLINK[0][0]][1])
            if pos and flip:  # espelhado: o remendo espelhado cai no lado oposto
                pos = [f["w"] - pos[0] - patches[BLINK[0][0]][0].width, pos[1]]
            f["olho"] = pos
    # prova: parada + remendo == piscando montado pelo rig (nas 4 versões)
    if "parada" in meta["animations"] and "piscando" in meta["animations"]:
        for suf in ("", "_esquerda", "_contorno", "_contorno_esquerda"):
            stand, blink = cells["parada" + suf][0], cells["piscando" + suf]
            x, y = meta["animations"]["parada" + suf]["frames"][0]["olho"]
            for i, (name, _) in enumerate(BLINK, start=1):
                img = patches[name][0]
                if suf.endswith("_esquerda"):
                    img = img.transpose(Image.FLIP_LEFT_RIGHT)
                got = stand.copy()
                got.alpha_composite(img, (x, y))
                if got.tobytes() != blink[i].tobytes():
                    raise SystemExit(f"remendo do olho não bate com piscando{suf} frame {i}")
        print("piscar: remendos conferidos contra o piscando do rig (4 versões)")
    meta["expressoes"] = {"piscar": {
        "ancora": "olho",
        "frames": [{"img": f"expressoes/{n}.png", "img_esquerda": f"expressoes/{n}_esquerda.png",
                    "duration_ms": d} for n, d in BLINK],
        "intervalo_ms": BLINK_EVERY_MS,
    }}


def outline(img):
    from filters import FILTERS
    return FILTERS["outline"](img, color="G")


def export_pant(meta, recipes, approved):
    """Remendos da boca ofegante (normal e contorno) e "boca" em cada frame; confere contra o rig."""
    rig = Rig(PARTS)
    dst = FINAL / "expressoes"
    x0, y0, x1, y1 = MOUTH_BOX
    # cabeça normal e ofegante na pose parada, pra recortar a boca (e o contorno em volta dela)
    def stand_with(head):
        rec = {"name": "s", "canvas": [32, 32], "frames": [{"parts": [
            {"id": "legs", "part": "legs_base", "at": [0, 19]}, {"id": "torso", "part": "torso", "at": [0, 0]},
            {"id": "head", "part": head, "attach": "torso.pescoco"}]}]}
        fr = rig.resolve_frames(rec)[0]
        img, _, _ = rig.render_frame(fr["parts"], (32, 32))
        return img, rig.origins(fr["parts"])["head"]
    base_img, (hx, hy) = stand_with("head")
    base_out = outline(base_img)
    box = (hx + x0, hy + y0, hx + x1, hy + y1)
    pad = (box[0] - 1, box[1] - 1, box[2] + 1, box[3] + 1)      # o contorno passa 1 px pra fora
    patches = {}
    for name, head, _ in PANT:
        img, _ = stand_with(head)
        normal = img.crop(box)
        out = outline(img)
        # contorno: só os pixels que mudam em relação ao contorno da cara normal
        cont = Image.new("RGBA", (pad[2] - pad[0], pad[3] - pad[1]), (0, 0, 0, 0))
        for y in range(cont.height):
            for x in range(cont.width):
                a = out.getpixel((pad[0] + x, pad[1] + y))
                if a != base_out.getpixel((pad[0] + x, pad[1] + y)):
                    if a[3] == 0:
                        raise SystemExit(f"{name}: o contorno precisaria apagar um pixel")
                    cont.putpixel((x, y), a)
        for suf, im in (("", normal), ("_contorno", cont)):
            im.save(dst / f"{name}{suf}.png")
            im.transpose(Image.FLIP_LEFT_RIGHT).save(dst / f"{name}{suf}_esquerda.png")
        patches[name] = (normal, cont)
    # "boca" por frame: canto da cabeça (peça com a cara normal) + canto do recorte; null se a boca já mexe
    for name, info in approved.items():
        if "composicao" in info:
            continue
        rec = recipes[name]
        frames = rig.resolve_frames(rec)
        seq = rec.get("sequence", list(range(len(frames))))
        pos = []
        for i in seq:
            parts = frames[i]["parts"]
            origins = rig.origins(parts)
            face = [p for p in parts if p["part"] in FACE_PARTS]
            heads = [p for p in parts if p["part"].startswith("head") and p["part"] != "head"]
            if not face or heads:
                pos = None
                break
            p = face[0]
            ox, oy = origins[p.get("id", p["part"])]
            dx, dy = FACE_PARTS[p["part"]]
            pos.append([ox + dx + x0, oy + dy + y0])
        for suf in ("", "_esquerda", "_contorno", "_contorno_esquerda"):
            for k, f in enumerate(meta["animations"][name + suf]["frames"]):
                if pos is None:
                    f["boca"] = None
                elif suf.endswith("_esquerda"):
                    f["boca"] = [f["w"] - pos[k][0] - (x1 - x0), pos[k][1]]
                else:
                    f["boca"] = list(pos[k])
    # prova: andando + remendo == trote com a cabeça ofegante montado pelo rig (4 versões, as duas bocas)
    if "andando" in meta["animations"]:
        sheet = Image.open(FINAL / meta["sheet"]).convert("RGBA")
        walk = json.loads((SPRITES_DIR / "anims" / f"{approved['andando']['recipe']}.json").read_text())
        with tempfile.TemporaryDirectory() as tmp:
            for name, head, _ in PANT:
                rec = json.loads(json.dumps(walk))
                rec["name"] = "w"
                for fr in rec["frames"]:
                    for p in fr.get("parts", []):
                        if p.get("part") == "upper":
                            p.update({"part": "torso", "id": "torso"})
                    for pid in list(fr.get("set", {})):
                        if pid == "upper":
                            fr["set"]["torso"] = fr["set"].pop("upper")
                    if "parts" in fr:
                        fr["parts"].append({"id": "head", "part": head, "attach": "torso.pescoco"})
                rig.build(rec, tmp)
                for suf, folder, flip, k in (("", "w", False, 0), ("_esquerda", "w", True, 0),
                                             ("_contorno", "w_contorno", False, 1),
                                             ("_contorno_esquerda", "w_contorno", True, 1)):
                    man = json.loads((Path(tmp) / folder / "manifest.json").read_text())
                    for f, mf in zip(meta["animations"]["andando" + suf]["frames"], man["frames"]):
                        ref = Image.open(Path(tmp) / folder / mf["file"]).convert("RGBA")
                        if flip:
                            ref = ref.transpose(Image.FLIP_LEFT_RIGHT)
                        got = sheet.crop((f["x"], f["y"], f["x"] + f["w"], f["y"] + f["h"]))
                        patch = patches[name][k]
                        if flip:
                            patch = patch.transpose(Image.FLIP_LEFT_RIGHT)
                        bx, by = f["boca"]
                        if k:   # o remendo do contorno tem 1 px de folga em volta
                            bx, by = (bx - 1, by - 1) if not flip else (bx - 1, by - 1)
                        got.alpha_composite(patch, (bx, by))
                        if got.tobytes() != ref.tobytes():
                            raise SystemExit(f"boca {name} não bate com o rig em andando{suf}")
        print("ofegante: remendos da boca conferidos contra o trote com a cabeça ofegante (4 versões, 2 bocas)")
    meta["expressoes"]["ofegante"] = {
        "ancora": "boca",
        "frames": [{"img": f"expressoes/{n}.png", "img_esquerda": f"expressoes/{n}_esquerda.png",
                    "img_contorno": f"expressoes/{n}_contorno.png",
                    "img_contorno_esquerda": f"expressoes/{n}_contorno_esquerda.png", "duration_ms": d}
                   for n, _, d in PANT],
        "loop": True,
        "contorno_folga_px": 1,
    }


def main():
    approved = {k: v for k, v in json.loads((FINAL / "aprovadas.json").read_text()).items()
                if not k.startswith("_")}
    frames_dir = FINAL / "frames"
    if frames_dir.exists():
        shutil.rmtree(frames_dir)
    spec = {"out": "kiara-sprites", "animations": {}}
    extra, recipes = {}, {}
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for name, info in approved.items():
            if "composicao" in info:   # corpo + expressão em relógios separados: não gera frames
                continue
            recipe = render(info["recipe"], tmp)
            recipes[name] = recipe
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
    export_blink(meta, recipes)
    export_pant(meta, recipes, approved)
    meta["composicoes"] = {k: v["composicao"] for k, v in approved.items() if "composicao" in v}
    meta["_comment"] = ("step_px: px do sprite que a janela anda por frame (negativo = pra esquerda); "
                        "airborne_frames: frames com as patas fora do chão; "
                        "olho: canto [x, y] do remendo do piscar na célula (null = a animação já mexe no olho); "
                        "expressoes.piscar: remendos e durações, tocados por cima de qualquer animação a cada "
                        "intervalo_ms (sorteado entre os dois valores); boca: canto [x, y] do remendo do ofegante "
                        "(null = a animação já mexe na boca); expressoes.ofegante: remendos da boca em loop, no ritmo "
                        "deles; os _contorno têm 1 px de folga (desenhe em boca - 1); composicoes: animações que são "
                        "um corpo + uma expressão tocando juntos, cada um no seu relógio")
    meta_path.write_text(json.dumps(meta, indent=2) + "\n")
    # a galeria (página com tudo o que foi aprovado) é refeita junto
    subprocess.run([sys.executable, str(TOOLS / "gallery.py")], check=True)


if __name__ == "__main__":
    main()
