"""Alonga o corpo de uma animação N px sem redesenhar.

Pedido do dono: "na corrida aumenta uns 3-4 pixels pro corpo". Em cada frame o
script acha uma coluna do tronco por onde só passa o corpo (borda das costas e
da barriga retas ali, nenhuma perna embaixo) e repete essa coluna N vezes. Nas
linhas em que a coluna não atravessa o corpo (acima das costas, abaixo da
barriga), a parte da frente só anda N px pra direita, então pernas, peito,
pescoço e cabeça vão juntos, sem esticar nada além do tronco. O quadro fica N px
mais largo; o socket do pescoço anda junto, então a cabeça acompanha sozinha.

Gera peças <peça>_<sufixo>.txt (na mesma pasta das peças) e
anims/<receita>_<sufixo>.json, e diz a coluna usada em cada frame.

Uso:
  python3 sprites/tools/alongar.py run 3 --sufixo c3
  python3 sprites/tools/alongar.py run 4 --sufixo c4 --cols 10,11,14,14,12,15

Quando as pernas se cruzam embaixo da barriga (frame recolhido do galope), não há
coluna só de tronco: passe --cols e acerte as linhas das pernas à mão (no galope:
as patas de trás ficam e as da frente andam junto com o peito).
"""
import argparse
import json
from pathlib import Path

from PIL import Image

from common import SPRITES_DIR, parse_matrix
from rig import Rig

PARTS = SPRITES_DIR / "parts" / "32"
ANIMS = SPRITES_DIR / "anims"


def body_parts(frame):
    """Peças que esticam (tronco e pernas); a cabeça só acompanha pelo socket."""
    return [p for p in frame["parts"] if not p["part"].startswith(("head", "olho"))]


def composite(rig, frame, canvas):
    """Tronco + pernas do frame num quadro (com offsets) e a posição x de cada peça."""
    img = Image.new("RGBA", canvas, (0, 0, 0, 0))
    origins = rig.origins(frame["parts"])
    xs = {}
    for p in body_parts(frame):
        pid = p.get("id", p["part"])
        ox, oy = origins[pid]
        img.alpha_composite(rig.part(p["part"]).image, (ox, oy))
        xs[pid] = ox
    return img, xs


def column_run(img, x):
    """Linhas opacas da coluna x, se formarem um trecho só (senão None)."""
    ys = [y for y in range(img.height) if img.getpixel((x, y))[3]]
    if not ys or ys[-1] - ys[0] + 1 != len(ys):
        return None
    return ys[0], ys[-1]


def good_cuts(img, limit):
    """Colunas c em que c e c+1 são um trecho só e igual (costas e barriga retas ali) e o
    fundo do trecho é a barriga: nenhuma coluna vizinha (c-3..c+4) acaba mais acima, ou
    seja, não tem perna pendurada embaixo de c."""
    cols = [x for x in range(img.width) if any(img.getpixel((x, y))[3] for y in range(img.height))]
    runs = {x: column_run(img, x) for x in range(img.width)}
    out = []
    for c in range(cols[0] + 2, min(limit, img.width - 1)):
        a, b = runs[c], runs[c + 1]
        if not a or a != b:
            continue
        near = [runs[x][1] for x in range(max(0, c - 3), min(img.width, c + 5)) if runs[x]]
        if a[1] <= min(near):
            out.append(c)
    return out


def stretch_rows(rows, cut, n):
    """Repete a coluna `cut` n vezes onde ela atravessa o corpo; senão abre n colunas vazias."""
    out = []
    for row in rows:
        if cut < 0:
            out.append("." * n + row)
        elif cut >= len(row) - 1:
            out.append(row)
        else:
            fill = row[cut] * n if row[cut] != "." and row[cut + 1] != "." else "." * n
            out.append(row[:cut + 1] + fill + row[cut + 1:])
    return out


def write_part(src, dst, cut, n, note):
    lines = src.read_text().splitlines()
    rows, _ = parse_matrix(src)
    header = []
    for line in lines:
        if not line.lstrip().startswith("#"):
            break
        if line.startswith("# @socket.") and cut >= 0:
            tag, xy = line[2:].split(" ", 1)
            x, y = (int(v) for v in xy.split(","))
            line = f"# {tag} {x + n if x > cut else x},{y}"
        header.append(line)
    header.append(f"# {note}")
    dst.write_text("\n".join(header + stretch_rows(rows, cut, n)) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("recipe")
    ap.add_argument("n", type=int, help="quantos px a mais de corpo")
    ap.add_argument("--sufixo", required=True)
    ap.add_argument("--cols", default="", help="coluna do corte por frame (vírgulas); padrão: automática")
    ap.add_argument("--parts", default=str(PARTS))
    args = ap.parse_args()

    parts_dir = Path(args.parts)
    rig = Rig(parts_dir)
    recipe = json.loads((ANIMS / f"{args.recipe}.json").read_text())
    canvas = tuple(recipe.get("canvas", (32, 32)))
    frames = rig.resolve_frames(recipe)
    forced = [int(c) for c in args.cols.split(",")] if args.cols else None

    # coluna do corte por frame: a mesma em todos se der, perto do meio do tronco
    imgs, options = [], []
    for fr in frames:
        img, xs = composite(rig, fr, canvas)
        neck = min((x + s[0] for p in body_parts(fr) for k, s in rig.part(p["part"]).sockets.items()
                    for x in [xs[p.get("id", p["part"])]]), default=canvas[0]) - 4
        imgs.append((img, xs))
        options.append(good_cuts(img, neck))
    if forced:
        cuts = forced
    else:
        common = set(options[0]).intersection(*options[1:])
        mid = sum(sum(o) / len(o) for o in options if o) / len(options)
        if common:
            cuts = [min(common, key=lambda c: abs(c - mid))] * len(frames)
        else:
            cuts = [min(o, key=lambda c: abs(c - mid)) if o else None for o in options]
    for i, (c, o) in enumerate(zip(cuts, options)):
        if c is None:
            raise SystemExit(f"frame {i}: nenhuma coluna só de tronco; passe --cols")
        if c not in o:
            print(f"aviso: frame {i}, coluna {c} passa por perna ou borda torta (boas: {o}); confira no quadro")

    # peças novas (uma peça usada em frames com cortes diferentes não dá)
    done, rename = {}, {}
    for i, fr in enumerate(frames):
        _, xs = imgs[i]
        for p in body_parts(fr):
            name, pid = p["part"], p.get("id", p["part"])
            cut = cuts[i] - xs[pid]
            if name in done and done[name] != cut:
                raise SystemExit(f"a peça {name} aparece em frames com cortes diferentes")
            if name not in done:
                new = f"{name}_{args.sufixo}"
                write_part(parts_dir / f"{name}.txt", parts_dir / f"{new}.txt", cut, args.n,
                           f"alongada {args.n} px (tools/alongar.py, corte na coluna {cuts[i]} do quadro): "
                           f"pedido do dono, corpo mais comprido na corrida")
                done[name], rename[name] = cut, new

    def swap(obj):
        if isinstance(obj, dict):
            return {k: (rename.get(v, v) if k == "part" else swap(v)) for k, v in obj.items()}
        if isinstance(obj, list):
            return [swap(v) for v in obj]
        return obj

    out = swap(recipe)
    out["name"] = f"{recipe['name']}_{args.sufixo}"
    out["canvas"] = [canvas[0] + args.n, canvas[1]]
    path = ANIMS / f"{args.recipe}_{args.sufixo}.json"
    path.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
    print(f"cortes por frame: {cuts}")
    print(f"peças: {', '.join(rename.values())}")
    print(f"receita: {path} (quadro {out['canvas'][0]}x{out['canvas'][1]})")


if __name__ == "__main__":
    main()
