"""Ajusta as proporções das peças do rig: pernas mais longas e corpo mais comprido.

Pernas +N: tira N linhas da barriga (a partir de --body-row) da peça de cima e
repete N vezes uma linha da coxa (--leg-row) em cada faixa de pernas. A cabeça,
o dorso e as patas não mudam de lugar; a cachorra fica mais "pernuda" e menos
funda, sem crescer o quadro.

Corpo +M: repete M vezes uma coluna do meio do corpo (--col), em todas as
peças, no mesmo x. Escolha uma coluna que seja só barriga/dorso e esteja vazia
na região das pernas em todos os frames.

Grava as peças novas em outra pasta e uma receita stand.json + walk.json
ajustadas (y da faixa de pernas e deslocamento horizontal, se precisar).

Uso:
  python3 sprites/tools/proportion.py sprites/parts/32 saida_dir --legs 2 --body 2
"""
import argparse
import json
from pathlib import Path

from common import SPRITES_DIR, parse_matrix, parse_tags, write_matrix

LEG_BAND_Y = 20


def stretch_cols(rows, col, m):
    return [r[:col] + r[col] * m + r[col:] for r in rows]


def header_of(path):
    return [l for l in Path(path).read_text().splitlines() if l.lstrip().startswith("#")]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("parts", help="pasta das peças de origem (ex.: sprites/parts/32)")
    ap.add_argument("out", help="pasta de saída (peças + receitas)")
    ap.add_argument("--legs", type=int, default=0, help="linhas a mais nas pernas")
    ap.add_argument("--body", type=int, default=0, help="colunas a mais no corpo")
    ap.add_argument("--col", type=int, default=12, help="coluna do corpo repetida")
    ap.add_argument("--body-row", type=int, default=16, help="1ª linha da barriga removida")
    ap.add_argument("--leg-row", type=int, default=6,
                    help="linha da faixa de pernas repetida (igual em todos os frames)")
    ap.add_argument("--canvas", type=int, default=32)
    args = ap.parse_args()

    src, out = Path(args.parts), Path(args.out)
    (out / "parts").mkdir(parents=True, exist_ok=True)
    n, m = args.legs, args.body

    for path in sorted(src.glob("*.txt")):
        rows, _ = parse_matrix(path)
        tags = parse_tags(path)
        role = tags.get("role")
        if role == "torso":
            rows = rows[: args.body_row] + rows[args.body_row + n :]
        elif role == "pernas":
            r = args.leg_row
            rows = rows[: r + 1] + [rows[r]] * n + rows[r + 1 :]
        else:
            continue
        rows = stretch_cols(rows, args.col, m)
        write_matrix(out / "parts" / path.name, rows,
                     header_of(path) + [f"# proporção: pernas +{n}, corpo +{m} (proportion.py)"])

    # desloca pra esquerda só o necessário pra caber com 1 px de contorno à direita
    shift = max(0, m - 2)
    for name in ("stand", "walk"):
        recipe_path = SPRITES_DIR / "anims" / f"{name}.json"
        recipe = json.loads(recipe_path.read_text())
        for fr in recipe["frames"]:
            for p in fr.get("parts", []):
                if "at" in p:
                    x, y = p["at"]
                    if p.get("id") == "legs":
                        y = LEG_BAND_Y - n
                    p["at"] = [x - shift, y]
        (out / f"{name}.json").write_text(json.dumps(recipe, indent=2) + "\n")
    print(f"peças e receitas em {out} (pernas +{n}, corpo +{m}, deslocamento {shift})")


if __name__ == "__main__":
    main()
