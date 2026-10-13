"""Monta frames de animação encaixando peças ("boneco articulado").

Cada peça é uma matriz .txt em sprites/parts/ (mesmo formato do spritegen.py)
com tags de encaixe no cabeçalho:

    # @anchor 3,9          ponto da peça que encaixa no pai (ou no "at")
    # @socket.pescoco 14,4 ponto onde um filho pode encaixar
    # @role torso          papel da peça (vira máscara p/ filtros, ex. suéter)

A receita (sprites/anims/<nome>.json) diz, frame a frame, quais peças entram e
onde. A ordem da lista é a ordem de desenho (a última fica por cima):

{
  "name": "walk", "canvas": [24, 24], "loop": true,
  "sequence": [0, 1, 2, 3, 2, 1],          # opcional (padrão: 0..n-1)
  "variants": {"left": ["mirror"], "night": ["night"]},   # opcional
  "frames": [
    {"duration": 130, "parts": [
      {"id": "body", "part": "body_stand", "at": [12, 16]},
      {"part": "head_side", "attach": "body.pescoco", "offset": [0, -1]}
    ]},
    {"base": 0, "set": {"body": {"offset": [0, 1]}}}
  ]
}

- "at": posição no quadro onde fica o @anchor da peça.
- "attach": "<id>.<socket>" encaixa o @anchor no socket de outra peça do frame.
- "offset": deslocamento extra em pixels. Nunca há rotação: em sprite pequeno
  ela destrói a grade; movimento é deslocar 1px ou trocar a peça.
- "base"/"set": o frame copia as peças de outro frame e só altera o que está
  em "set" (por id); "set" com {"remove": true} tira a peça.
- "airborne": true marca frame no ar (o lint não exige pé no chão).

Saída em <out>/<nome>/: <nome>_<i>.png de cada frame + manifest.json com a
sequência de exibição. Cada variante sai em <out>/<nome>_<variante>/.

Uso:
  python3 sprites/tools/rig.py sprites/anims/walk.json [--out sprites/out] [--gif]
"""
import argparse
import copy
import json
import sys
from pathlib import Path

from PIL import Image

from animate import save_gif
from common import SPRITES_DIR, load_palette, matrix_to_image, parse_matrix, parse_tags

PARTS_DIR = SPRITES_DIR / "parts"


class Part:
    def __init__(self, name, palette, parts_dir=PARTS_DIR):
        path = Path(parts_dir) / f"{name}.txt"
        if not path.exists():
            raise FileNotFoundError(f"peça não encontrada: {path}")
        rows, _ = parse_matrix(path)
        tags = parse_tags(path)
        self.name = name
        self.image = matrix_to_image(rows, palette)
        self.anchor = tags.get("anchor", (0, 0))
        self.sockets = {
            k.split(".", 1)[1]: v for k, v in tags.items() if k.startswith("socket.")
        }
        self.role = tags.get("role") if isinstance(tags.get("role"), str) else None


class Rig:
    def __init__(self, parts_dir=PARTS_DIR):
        self.parts_dir = parts_dir
        self.palette = load_palette()
        self._cache = {}

    def part(self, name):
        if name not in self._cache:
            self._cache[name] = Part(name, self.palette, self.parts_dir)
        return self._cache[name]

    def resolve_frames(self, recipe):
        """Expande "base"/"set" em listas completas de peças por frame."""
        resolved = []
        for i, fr in enumerate(recipe["frames"]):
            if "base" in fr:
                b = fr["base"]
                if not 0 <= b < i:
                    raise ValueError(f"frame {i}: base {b} precisa ser um frame anterior")
                parts = copy.deepcopy(resolved[b]["parts"])
                changes = fr.get("set", {})
                ids = [p.get("id", p["part"]) for p in parts]
                for pid, change in changes.items():
                    if pid not in ids:
                        raise ValueError(f"frame {i}: set em id inexistente '{pid}'")
                    if change.get("remove"):
                        parts = [p for p in parts if p.get("id", p["part"]) != pid]
                        ids = [p.get("id", p["part"]) for p in parts]
                    else:
                        parts[ids.index(pid)].update(change)
                parts += copy.deepcopy(fr.get("parts", []))
                duration = fr.get("duration", resolved[b]["duration"])
            else:
                parts = copy.deepcopy(fr["parts"])
                duration = fr.get("duration", 150)
            resolved.append({
                "parts": parts,
                "duration": duration,
                "airborne": fr.get("airborne", False),
            })
        return resolved

    def origins(self, parts):
        """Canto superior esquerdo de cada peça do frame, por id (resolve os encaixes)."""
        entries = {}
        for p in parts:
            pid = p.get("id", p["part"])
            if pid in entries:
                raise ValueError(f"id repetido no frame: '{pid}' (use \"id\" distintos)")
            entries[pid] = p

        # encaixes podem vir em qualquer ordem, então resolve por dependência
        origin = {}

        def place(pid, chain=()):
            if pid in origin:
                return origin[pid]
            if pid in chain:
                raise ValueError(f"encaixe circular: {' -> '.join(chain + (pid,))}")
            e = entries[pid]
            part = self.part(e["part"])
            dx, dy = e.get("offset", (0, 0))
            if "at" in e:
                ax, ay = e["at"]
            elif "attach" in e:
                parent_id, _, socket = e["attach"].partition(".")
                if parent_id not in entries:
                    raise ValueError(f"'{pid}' encaixa em '{parent_id}', que não está no frame")
                parent = self.part(entries[parent_id]["part"])
                if socket not in parent.sockets:
                    raise ValueError(
                        f"'{parent.name}' não tem socket '{socket}' "
                        f"(tem: {sorted(parent.sockets)})"
                    )
                px, py = place(parent_id, chain + (pid,))
                sx, sy = parent.sockets[socket]
                ax, ay = px + sx, py + sy
            else:
                raise ValueError(f"'{pid}' precisa de \"at\" ou \"attach\"")
            origin[pid] = (ax + dx - part.anchor[0], ay + dy - part.anchor[1])
            return origin[pid]

        for pid in entries:
            place(pid)
        return origin

    def render_frame(self, parts, canvas):
        """Desenha um frame. Retorna (imagem, máscaras por papel, avisos)."""
        w, h = canvas
        origin = self.origins(parts)

        img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        owner = [[None] * w for _ in range(h)]
        warnings = []
        for p in parts:
            pid = p.get("id", p["part"])
            part = self.part(p["part"])
            ox, oy = origin[pid]
            src = part.image.load()
            outside = 0
            for y in range(part.image.height):
                for x in range(part.image.width):
                    c = src[x, y]
                    if c[3] == 0:
                        continue
                    cx, cy = ox + x, oy + y
                    if not (0 <= cx < w and 0 <= cy < h):
                        outside += 1
                        continue
                    img.putpixel((cx, cy), c)
                    owner[cy][cx] = p.get("role", part.role) or pid
            if outside:
                warnings.append(f"'{pid}': {outside} px fora do quadro")

        masks = {}
        for y in range(h):
            for x in range(w):
                role = owner[y][x]
                if role is None:
                    continue
                if role not in masks:
                    masks[role] = Image.new("L", (w, h), 0)
                masks[role].putpixel((x, y), 255)
        return img, masks, warnings

    def build(self, recipe, outdir, gif=False, scale=8):
        name = recipe["name"]
        canvas = tuple(recipe.get("canvas", (24, 24)))
        frames = self.resolve_frames(recipe)
        rendered = [self.render_frame(f["parts"], canvas) for f in frames]
        sequence = recipe.get("sequence", list(range(len(frames))))

        variants = {"": []}
        variants.update(recipe.get("variants", {}))
        written = []
        for vname, chain in variants.items():
            folder = name if not vname else f"{name}_{vname}"
            dest = Path(outdir) / folder
            dest.mkdir(parents=True, exist_ok=True)
            files = []
            for i, (img, masks, warns) in enumerate(rendered):
                for wmsg in warns:
                    print(f"  aviso [{folder} frame {i}]: {wmsg}", file=sys.stderr)
                out = apply_chain(img, masks, chain)
                fname = f"{folder}_{i}.png"
                out.save(dest / fname)
                files.append(fname)
            manifest = {
                "name": folder,
                "canvas": list(canvas),
                "loop": recipe.get("loop", True),
                "frames": [
                    {
                        "file": files[i],
                        "duration": frames[i]["duration"],
                        "airborne": frames[i]["airborne"],
                    }
                    for i in sequence
                ],
            }
            (dest / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
            if gif:
                imgs = [Image.open(dest / files[i]) for i in sequence]
                save_gif(imgs, dest / f"{folder}.gif",
                         [frames[i]["duration"] for i in sequence], scale=scale)
            written.append(dest)
        return written


def apply_chain(img, masks, chain):
    """Aplica filtros em sequência; "mirror" espelha imagem e máscaras juntos."""
    for step in chain:
        if step == "mirror":
            img = img.transpose(Image.FLIP_LEFT_RIGHT)
            masks = {k: m.transpose(Image.FLIP_LEFT_RIGHT) for k, m in masks.items()}
            continue
        import filters  # só carrega quando há filtro de verdade

        name, opts = (step, {}) if isinstance(step, str) else (step["filter"], step.get("opts", {}))
        if name not in filters.FILTERS:
            raise ValueError(f"filtro desconhecido: {name}")
        img = filters.FILTERS[name](img, masks=masks, **opts)
    return img


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("recipe", help="receita JSON (ex.: sprites/anims/walk.json)")
    ap.add_argument("--out", default=str(SPRITES_DIR / "out"), help="pasta de saída")
    ap.add_argument("--parts", default=str(PARTS_DIR), help="pasta das peças")
    ap.add_argument("--gif", action="store_true", help="gera GIF de preview")
    ap.add_argument("--scale", type=int, default=8, help="escala do GIF")
    args = ap.parse_args()

    recipe = json.loads(Path(args.recipe).read_text())
    try:
        for dest in Rig(args.parts).build(recipe, args.out, gif=args.gif, scale=args.scale):
            print(f"frames: {dest}")
    except (ValueError, FileNotFoundError) as e:
        sys.exit(f"ERRO: {e}")


if __name__ == "__main__":
    main()
