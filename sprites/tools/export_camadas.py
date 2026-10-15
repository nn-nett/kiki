"""Exporta as animações aprovadas também em CAMADAS: corpo sem cabeça, cabeças soltas e olho.

Pedido do dono: "componentizar: a cabeça separada do corpo, o olho também sendo algo
específico, pra ela poder piscar em qualquer estado, tipo piscar enquanto late". Com as
camadas o app monta qualquer combinação sem frame novo: latir andando, piscar latindo,
ofegante andando, etc. Os frames inteiros de final/frames/ continuam valendo; isto é um
jeito a mais de montar a mesma coisa.

Gera em final/camadas/:
  corpo/<anim>_<i>.png    pernas + tronco do frame i, sem cabeça (32x32, olhando pra direita)
  cabeca/<cabeca>.png     cada cabeça desenhada (normal, latido 1 e 2, ofegante 1 e 2)
e põe "camadas" no kiara-sprites.json (formato no README). O olho do piscar é o mesmo
remendo de final/expressoes/ e cai em "olho" da cabeça.

Montar um frame: corpo em (0, 0); cabeça em pescoco - ancora + deslocamento; olho (se
piscando) em posição da cabeça + olho. Esquerda = espelhar o quadro pronto; taskbar escura
= contorno G em volta (pixel transparente com vizinho opaco em cima/baixo/lados) antes de
espelhar. O script confere que isso dá exatamente os frames aprovados, nas 4 versões.

Uso (o export_final.py chama sozinho):
  python3 sprites/tools/export_camadas.py
"""
import json
import shutil
from pathlib import Path

from PIL import Image

from common import SPRITES_DIR, load_palette
from rig import Rig
from sim_page import upper_to_layers

FINAL = SPRITES_DIR / "final"
PARTS = SPRITES_DIR / "parts" / "32"
ANIMS = SPRITES_DIR / "anims"
OUT = FINAL / "camadas"


def to_layers(recipe):
    """Receita com 'upper' (cabeça e tronco numa peça só) vira torso + head; as outras ficam como estão."""
    uses_upper = any(p.get("part") == "upper" for fr in recipe["frames"] for p in fr.get("parts", []))
    return upper_to_layers(recipe) if uses_upper else recipe


def is_head(part):
    return part.startswith("head")


def outline(img):
    """Contorno G em volta: igual ao filtro outline (vizinho de cima/baixo/lados)."""
    g = tuple(load_palette()["G"]) + (255,)
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


def main():
    approved = {k: v for k, v in json.loads((FINAL / "aprovadas.json").read_text()).items()
                if not k.startswith("_") and "recipe" in v}
    meta_path = FINAL / "kiara-sprites.json"
    meta = json.loads(meta_path.read_text())
    sheet = Image.open(FINAL / meta["sheet"]).convert("RGBA")
    rig = Rig(PARTS)
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "corpo").mkdir(parents=True)
    (OUT / "cabeca").mkdir()

    heads, bodies = {}, {}
    for name, info in approved.items():
        recipe = to_layers(json.loads((ANIMS / f"{info['recipe']}.json").read_text()))
        canvas = tuple(recipe.get("canvas", (32, 32)))
        frames = rig.resolve_frames(recipe)
        seq = recipe.get("sequence", list(range(len(frames))))
        out = []
        for k, i in enumerate(seq):
            parts = frames[i]["parts"]
            origins = rig.origins(parts)
            head = next(p for p in parts if is_head(p["part"]))
            torso_id = head["attach"].split(".")[0]
            torso = next(p for p in parts if p.get("id", p["part"]) == torso_id)
            sx, sy = rig.part(torso["part"]).sockets[head["attach"].split(".")[1]]
            tx, ty = origins[torso_id]
            body_parts = [p for p in parts if not is_head(p["part"]) and not p["part"].startswith("olho")]
            img, _, _ = rig.render_frame(body_parts, canvas)
            f = f"corpo/{name}_{k}.png"
            img.save(OUT / f)
            hp = rig.part(head["part"])
            heads[head["part"]] = hp
            out.append({"img": f"camadas/{f}", "duration_ms": frames[i]["duration"],
                        "pescoco": [tx + sx, ty + sy], "cabeca": head["part"],
                        "cabeca_off": list(head.get("offset", [0, 0]))})
        bodies[name] = {"loop": recipe.get("loop", True), "step_px": info.get("step_px", 0), "frames": out}

    olho_anchor = rig.part("olho_meio").anchor
    head_meta = {}
    for name, hp in sorted(heads.items()):
        hp.image.save(OUT / "cabeca" / f"{name}.png")
        sock = hp.sockets
        head_meta[name] = {"img": f"camadas/cabeca/{name}.png", "ancora": list(hp.anchor),
                           "olho": ([sock["olho"][0] - olho_anchor[0], sock["olho"][1] - olho_anchor[1]]
                                    if "olho" in sock else None)}

    # expressões de cabeça que dá pra pôr em qualquer corpo (o tranco do latido vai só na cabeça)
    def head_seq(recipe_name, idx):
        rec = to_layers(json.loads((ANIMS / f"{recipe_name}.json").read_text()))
        frs = rig.resolve_frames(rec)
        res = []
        for i in idx:
            parts = frs[i]["parts"]
            h = next(p for p in parts if is_head(p["part"]))
            t = next(p for p in parts if p.get("id", p["part"]) == h["attach"].split(".")[0])
            to, ho = t.get("offset", [0, 0]), h.get("offset", [0, 0])
            res.append({"cabeca": h["part"], "off": [to[0] + ho[0], to[1] + ho[1]], "duration_ms": frs[i]["duration"]})
        return res
    expr = {}
    if "latindo" in approved:
        expr["latir"] = {"loop": False, "frames": head_seq(approved["latindo"]["recipe"], [1, 2, 3, 1, 2, 3])}
    expr["ofegante"] = {"loop": True, "frames": [{"cabeca": "head_ofegante1", "off": [0, 0], "duration_ms": 130},
                                                 {"cabeca": "head_ofegante2", "off": [0, 0], "duration_ms": 130}]}
    for e in expr.values():
        for fr in e["frames"]:
            if fr["cabeca"] not in head_meta:
                hp = rig.part(fr["cabeca"])
                hp.image.save(OUT / "cabeca" / f"{fr['cabeca']}.png")
                head_meta[fr["cabeca"]] = {"img": f"camadas/cabeca/{fr['cabeca']}.png", "ancora": list(hp.anchor),
                                           "olho": [hp.sockets["olho"][0] - olho_anchor[0],
                                                    hp.sockets["olho"][1] - olho_anchor[1]]}

    # prova: montar as camadas dá os frames aprovados (4 versões); com o olho, dá o "piscando"
    def build(fr, head=None, off=None, eye=None):
        img = Image.open(FINAL / fr["img"]).convert("RGBA").copy()
        hname = head or fr["cabeca"]
        h = head_meta[hname]
        hx = fr["pescoco"][0] - h["ancora"][0] + (off or fr["cabeca_off"])[0]
        hy = fr["pescoco"][1] - h["ancora"][1] + (off or fr["cabeca_off"])[1]
        img.alpha_composite(Image.open(FINAL / h["img"]).convert("RGBA"), (hx, hy))
        if eye:
            img.alpha_composite(Image.open(FINAL / "expressoes" / f"{eye}.png").convert("RGBA"),
                                (hx + h["olho"][0], hy + h["olho"][1]))
        return img
    crop = lambda f: sheet.crop((f["x"], f["y"], f["x"] + f["w"], f["y"] + f["h"]))
    checked = 0
    for name, body in bodies.items():
        eyes = [None] * len(body["frames"])
        recipe = json.loads((ANIMS / f"{approved[name]['recipe']}.json").read_text())
        frs = rig.resolve_frames(recipe)
        for k, i in enumerate(recipe.get("sequence", list(range(len(frs))))):
            eye = [p["part"] for p in frs[i]["parts"] if p["part"].startswith("olho")]
            eyes[k] = eye[0] if eye else None
        for k, fr in enumerate(body["frames"]):
            got = build(fr, eye=eyes[k])
            for suf, img in (("", got), ("_esquerda", got.transpose(Image.FLIP_LEFT_RIGHT)),
                             ("_contorno", outline(got)),
                             ("_contorno_esquerda", outline(got).transpose(Image.FLIP_LEFT_RIGHT))):
                ref = crop(meta["animations"][name + suf]["frames"][k])
                if img.tobytes() != ref.tobytes():
                    raise SystemExit(f"camadas não batem com {name}{suf} frame {k}")
                checked += 1
    print(f"camadas: {len(bodies)} corpos, {len(head_meta)} cabeças; montagem confere com {checked} frames finais")

    meta["camadas"] = {
        "_como_montar": ("corpo em (0,0); cabeça em pescoco - ancora + off (off = cabeca_off do frame, ou o 'off' "
                         "da expressão de cabeça que estiver tocando, no relógio dela); olho do piscar em posição "
                         "da cabeça + olho; pra esquerda espelhe o quadro pronto; taskbar escura: contorno G "
                         "(pixel vazio com vizinho opaco em cima/baixo/lados) antes de espelhar"),
        "corpos": bodies,
        "cabecas": head_meta,
        "expressoes_cabeca": expr,
    }
    meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
