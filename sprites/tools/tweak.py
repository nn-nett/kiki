"""Ajuste fino de pixels nas peças do rig, com variantes lado a lado.

É o ciclo que o dono pede o tempo todo ("esse pixel tá estranho", "deixa 1 px
maior"): mexer em poucos pixels, ver em todos os frames, conferir buracos e
aplicar a escolhida. Coordenadas sempre no QUADRO 32x32, na posição da peça na
pose parada (sem offset), então batem com o que se vê na imagem ampliada.

Subcomandos:

  show PEÇA [--rows 20-26] [--cols 0-18]
      Mostra a matriz da peça com o número da linha e da coluna no quadro.

  try SAIDA VARIANTE... [--from PASTA] [--recipes stand walk_b] [--crop x0,y0,x1,y1] [--zoom 8]
      VARIANTE = "nome" (sem mudança, vira a linha de base) ou
                 "nome=peça@x,y:velho>novo peça@x,y:velho>novo ..."
        x e y aceitam faixa (12-16); velho = letras aceitas antes da troca
        (ex.: ".K"; "*" aceita qualquer uma). A peça pode ser "legs_trotB*"
        (todas as que casam) e a troca só vale onde a letra é "velho".
      Monta cada variante (cópia das peças de --from, padrão sprites/parts/32),
      renderiza as receitas, procura buracos presos, pixels soltos e entalhes
      NOVOS (comparando com a 1ª variante) e grava SAIDA/quadro.png
      (linhas = variantes, colunas = frames).

  apply SAIDA/nome --note "texto"
      Copia as peças que mudaram pra sprites/parts/32 (com o comentário) e
      regenera sprites/base/kiara_32.{txt,png,_contorno.png} a partir de stand.json.

Exemplo (barriga 1 px mais funda em todos os frames do trote):
  python3 sprites/tools/tweak.py try /tmp/t antes "gorda=legs_*@12-16,24:.>K"
"""
import argparse
import fnmatch
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from common import SPRITES_DIR, TASKBAR_LIGHT, image_to_matrix, parse_matrix, upscale, write_matrix
from rig import Rig

PARTS = SPRITES_DIR / "parts" / "32"
ANIMS = SPRITES_DIR / "anims"
TOOLS = SPRITES_DIR / "tools"


# ---------- posição das peças no quadro ----------

def part_origins(parts_dir=PARTS):
    """{peça: (x, y)} do canto da peça no quadro, sem offset, pela 1ª receita que a usa."""
    rig = Rig(parts_dir)
    found = {}
    for path in sorted(ANIMS.glob("*.json")):
        try:
            frames = rig.resolve_frames(json.loads(path.read_text()))
        except Exception:
            continue
        for fr in frames:
            parts = [{k: v for k, v in p.items() if k != "offset"} for p in fr["parts"]]
            try:
                origin = rig.origins(parts)
            except Exception:
                continue
            for p in parts:
                found.setdefault(p["part"], origin[p.get("id", p["part"])])
    return found


def data_lines(path):
    lines = Path(path).read_text().splitlines()
    return lines, [i for i, l in enumerate(lines) if not l.lstrip().startswith("#")]


# ---------- show ----------

def span(text, default):
    if not text:
        return default
    a, _, b = text.partition("-")
    return int(a), int(b or a)


def cmd_show(args):
    origin = part_origins(args.parts)
    if args.part not in origin:
        sys.exit(f"'{args.part}' não aparece em nenhuma receita de {ANIMS}")
    ox, oy = origin[args.part]
    rows, _ = parse_matrix(Path(args.parts) / f"{args.part}.txt")
    width = max(len(r) for r in rows)
    y0, y1 = span(args.rows, (oy, oy + len(rows) - 1))
    x0, x1 = span(args.cols, (ox, ox + width - 1))
    print(f"{args.part}: canto no quadro ({ox},{oy})")
    print("    " + "".join(str(x % 10) for x in range(x0, x1 + 1)))
    for y in range(y0, y1 + 1):
        r = rows[y - oy] if 0 <= y - oy < len(rows) else ""
        print(f"{y:3d} " + "".join(r[x - ox] if 0 <= x - ox < len(r) else " " for x in range(x0, x1 + 1)))


# ---------- try ----------

def parse_variant(text):
    name, _, specs = text.partition("=")
    edits = []
    for spec in specs.split():
        part, _, rest = spec.partition("@")
        pos, _, change = rest.partition(":")
        old, _, new = change.partition(">")
        xs, _, ys = pos.partition(",")
        if not (part and xs and ys and len(new) == 1):
            sys.exit(f"troca inválida: {spec!r} (use peça@x,y:velho>novo)")
        edits.append((part, span(xs, None), span(ys, None), old, new))
    return name, edits


def apply_edits(parts_dir, edits, origin):
    log = []
    for pattern, (xa, xb), (ya, yb), old, new in edits:
        names = sorted(n for n in origin if fnmatch.fnmatch(n, pattern)
                       and (Path(parts_dir) / f"{n}.txt").exists())
        if not names:
            sys.exit(f"nenhuma peça casa com '{pattern}'")
        for name in names:
            path = Path(parts_dir) / f"{name}.txt"
            lines, data = data_lines(path)
            ox, oy = origin[name]
            hits = []
            for y in range(ya, yb + 1):
                i = y - oy
                if not 0 <= i < len(data):
                    continue
                row = list(lines[data[i]])
                for x in range(xa, xb + 1):
                    j = x - ox
                    if 0 <= j < len(row) and (old == "*" or row[j] in old) and row[j] != new:
                        row[j] = new
                        hits.append((x, y))
                lines[data[i]] = "".join(row)
            path.write_text("\n".join(lines) + "\n")
            if hits:
                log.append(f"  {name}: {len(hits)} px {hits if len(hits) <= 8 else ''}")
    return log


def render(recipe, parts_dir, out):
    subprocess.run([sys.executable, str(TOOLS / "rig.py"), str(ANIMS / f"{recipe}.json"),
                    "--parts", str(parts_dir), "--out", str(out)], check=True, stdout=subprocess.DEVNULL)


def frame_files(out, recipes):
    files = []
    for r in recipes:
        name = json.loads((ANIMS / f"{r}.json").read_text())["name"]
        man = json.loads((Path(out) / name / "manifest.json").read_text())
        files += [(f"{r} {i}", Path(out) / name / f["file"]) for i, f in enumerate(man["frames"])]
    return files


def problems(img):
    """(buracos presos, pixels soltos, entalhes) de um frame."""
    rows = image_to_matrix(img, snap=True)
    h, w = len(rows), len(rows[0])
    opaque = lambda x, y: 0 <= x < w and 0 <= y < h and rows[y][x] != "."
    outside, stack = set(), [(x, y) for x in range(w) for y in (0, h - 1)] + \
        [(x, y) for y in range(h) for x in (0, w - 1)]
    while stack:
        x, y = stack.pop()
        if (x, y) in outside or not (0 <= x < w and 0 <= y < h) or opaque(x, y):
            continue
        outside.add((x, y))
        stack += [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    n4 = ((1, 0), (-1, 0), (0, 1), (0, -1))
    holes = [(x, y) for y in range(h) for x in range(w) if not opaque(x, y) and (x, y) not in outside]
    loose = [(x, y) for y in range(h) for x in range(w)
             if opaque(x, y) and not any(opaque(x + dx, y + dy) for dx, dy in n4)]
    notches = {(x, y) for y in range(h) for x in range(w)
               if not opaque(x, y) and sum(opaque(x + dx, y + dy) for dx, dy in n4) >= 3}
    return holes, loose, notches


def font(size):
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)
    except OSError:
        return ImageFont.load_default()


def board(rows, crop, zoom, out):
    """rows = [(rótulo, [(rótulo_frame, Image)])] -> quadro com linhas = variantes."""
    w, h = crop[2] - crop[0], crop[3] - crop[1]
    cw, rh, lw = w * zoom + 8, h * zoom + 10, 150
    ncol = max(len(fr) for _, fr in rows)
    img = Image.new("RGB", (lw + ncol * cw, 34 + len(rows) * rh), TASKBAR_LIGHT)
    d, F = ImageDraw.Draw(img), font(18)
    for j, (lab, _) in enumerate(rows[0][1]):
        d.text((lw + j * cw + 4, 8), lab, font=F, fill=(40, 40, 40))
    for i, (lab, frames) in enumerate(rows):
        d.multiline_text((8, 34 + i * rh + rh // 3), lab.replace(" ", "\n", 1), font=F, fill=(40, 40, 40))
        for j, (_, im) in enumerate(frames):
            big = upscale(im.convert("RGBA").crop(crop), zoom, bg=TASKBAR_LIGHT).convert("RGB")
            img.paste(big, (lw + j * cw, 34 + i * rh))
    img.save(out)


def cmd_try(args):
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    src = Path(args.from_ or PARTS)
    origin = part_origins(src)
    rows, base_notches = [], None
    for k, text in enumerate(args.variants):
        name, edits = parse_variant(text)
        vdir = out / name
        if vdir.exists():
            shutil.rmtree(vdir)
        shutil.copytree(src, vdir / "parts", ignore=shutil.ignore_patterns("*.md", "*.png"))
        log = apply_edits(vdir / "parts", edits, origin)
        for r in args.recipes:
            render(r, vdir / "parts", vdir / "out")
        print(f"== {name}" + ("" if edits else " (base)"))
        print("\n".join(log) if log else "  sem mudanças")
        frames = [(lab, Image.open(f)) for lab, f in frame_files(vdir / "out", args.recipes)]
        found = [problems(im) for _, im in frames]
        if base_notches is None:
            base_notches = [n for _, _, n in found]
        for (lab, _), (holes, loose, notches), bn in zip(frames, found, base_notches):
            new = sorted(notches - bn)
            for kind, items in (("BURACO", holes), ("pixel solto", loose), ("entalhe novo", new)):
                if items:
                    print(f"  {kind} em {lab}: {items}")
        rows.append((name, frames))
    crop = tuple(int(v) for v in args.crop.split(",")) if args.crop else (0, 0, 32, 32)
    board(rows, crop, args.zoom, out / "quadro.png")
    print(f"quadro: {out / 'quadro.png'}")


# ---------- apply ----------

def cmd_apply(args):
    vdir = Path(args.variant)
    changed = []
    for path in sorted((vdir / "parts").glob("*.txt")):
        dst = PARTS / path.name
        new_rows, _ = parse_matrix(path)
        if dst.exists() and parse_matrix(dst)[0] == new_rows:
            continue
        lines, data = data_lines(path)
        if args.note:
            lines.insert(data[0], f"# {args.note}")
        dst.write_text("\n".join(lines) + "\n")
        changed.append(path.name)
    print("peças atualizadas:", ", ".join(changed) or "nenhuma")
    rebase(args.note)


def rebase(note=None):
    """Regenera sprites/base/kiara_32.* a partir de anims/stand.json."""
    base = SPRITES_DIR / "base" / "kiara_32"
    with tempfile.TemporaryDirectory() as tmp:
        render("stand", PARTS, tmp)
        img = Image.open(Path(tmp) / "stand" / "stand_0.png")
        rows = [r.replace("O", "B") for r in image_to_matrix(img, snap=True)]  # brilho do olho é B
        old, _ = parse_matrix(f"{base}.txt")
        diff = sum(a != b for ro, rn in zip(old, rows) for a, b in zip(ro, rn))
        header = [l[2:] if l.startswith("# ") else l[1:]
                  for l in Path(f"{base}.txt").read_text().splitlines() if l.startswith("#")]
        if note and diff:
            header.insert(len(header) - 1, note)
        write_matrix(f"{base}.txt", rows, header)
        img.save(f"{base}.png")
        contorno = Path(tmp) / "stand_contorno" / "stand_contorno_0.png"
        if contorno.exists():
            Image.open(contorno).save(f"{base}_contorno.png")
    print(f"pose base regenerada ({diff} px mudaram)")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("show")
    s.add_argument("part")
    s.add_argument("--rows")
    s.add_argument("--cols")
    s.add_argument("--parts", default=str(PARTS))
    t = sub.add_parser("try")
    t.add_argument("out")
    t.add_argument("variants", nargs="+")
    t.add_argument("--from", dest="from_")
    t.add_argument("--recipes", nargs="+", default=["stand", "walk_b"])
    t.add_argument("--crop", help="x0,y0,x1,y1 do recorte no quadro (padrão: tudo)")
    t.add_argument("--zoom", type=int, default=8)
    a = sub.add_parser("apply")
    a.add_argument("variant", help="SAIDA/nome de um try")
    a.add_argument("--note", default="")
    args = ap.parse_args()
    {"show": cmd_show, "try": cmd_try, "apply": cmd_apply}[args.cmd](args)


if __name__ == "__main__":
    main()
