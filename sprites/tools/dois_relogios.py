"""Prévia de corpo e cabeça em relógios separados (expressão desacoplada).

Pedido do dono: "mantém o ritmo da respiração na cabeça e o ritmo do andar,
coisas diferentes". O corpo segue a receita dele (ex.: trote, 100 ms por
frame) e a cabeça troca no ritmo da receita da expressão (ex.: ofegante,
130 ms por frame), sem sincronizar. No app isso são duas animações tocando
juntas; aqui o script monta a linha do tempo inteira (até os dois ciclos se
repetirem juntos) pra caber num preview comum: uma pasta igual à do rig.py, com
cada combinação corpo x cabeça renderizada uma vez, "step" por frame (ela só
anda quando o passo troca) e "spritemap" com as combinações.

Uso:
  python3 sprites/tools/dois_relogios.py --corpo andar_ofegante_W1 --cabeca ofegante_A3 \
      --step 1 --out /tmp/andar_resp
"""
import argparse
import json
import math
import shutil
import tempfile
from pathlib import Path

from common import SPRITES_DIR
from rig import Rig

PARTS = SPRITES_DIR / "parts" / "32"
ANIMS = SPRITES_DIR / "anims"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpo", required=True, help="receita do corpo (dá o passo e o ritmo do corpo)")
    ap.add_argument("--cabeca", required=True, help="receita da expressão (dá a cabeça e o ritmo dela)")
    ap.add_argument("--head-id", default="head")
    ap.add_argument("--step", type=int, default=1, help="px do sprite que ela anda a cada frame do corpo")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    rig = Rig(PARTS)
    body_rec = json.loads((ANIMS / f"{args.corpo}.json").read_text())
    head_rec = json.loads((ANIMS / f"{args.cabeca}.json").read_text())
    body = rig.resolve_frames(body_rec)
    heads = rig.resolve_frames(head_rec)
    bseq = body_rec.get("sequence", list(range(len(body))))
    hseq = head_rec.get("sequence", list(range(len(heads))))

    def head_of(fr):
        return next(p for p in fr["parts"] if p.get("id", p["part"]) == args.head_id)

    # cada combinação (frame do corpo, frame da cabeça) vira um frame do rig
    combos, frames = {}, []
    for bi in sorted(set(bseq)):
        for hi in sorted(set(hseq)):
            parts = [dict(p) for p in body[bi]["parts"] if p.get("id", p["part"]) != args.head_id]
            h = dict(head_of(body[bi]))
            src = head_of(heads[hi])
            h["part"] = src["part"]
            bo, ho = h.get("offset", [0, 0]), src.get("offset", [0, 0])
            h["offset"] = [bo[0] + ho[0], bo[1] + ho[1]]
            combos[(bi, hi)] = len(frames)
            frames.append({"duration": 100, "parts": parts + [h]})
    canvas = body_rec.get("canvas", [32, 32])
    out = Path(args.out)
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    with tempfile.TemporaryDirectory() as tmp:
        rig.build({"name": "c", "canvas": canvas, "loop": True, "frames": frames}, tmp)
        for (bi, hi), k in combos.items():
            shutil.copy(Path(tmp) / "c" / f"c_{k}.png", out / f"corpo{bi}_cabeca{hi}.png")

    # linha do tempo: cada um no seu relógio, até os dois ciclos baterem juntos
    def edges(seq, frs):
        t, out_ = 0, []
        for i in seq:
            out_.append((t, i))
            t += frs[i]["duration"]
        return out_, t
    be, bl = edges(bseq, body)
    he, hl = edges(hseq, heads)
    total = bl * hl // math.gcd(bl, hl)
    cuts = sorted({k * bl + t for k in range(total // bl) for t, _ in be} |
                  {k * hl + t for k in range(total // hl) for t, _ in he} | {total})
    body_starts = {k * bl + t for k in range(total // bl) for t, _ in be}

    def at(edges_, length, t):
        t %= length
        return [i for s, i in edges_ if s <= t][-1]
    man = {"name": out.name, "loop": True, "frames": [],
           "spritemap": [{"label": f"corpo f{bi} + cabeça f{hi}", "file": f"corpo{bi}_cabeca{hi}.png"}
                         for (bi, hi) in combos]}
    for a, b in zip(cuts, cuts[1:]):
        man["frames"].append({"file": f"corpo{at(be, bl, a)}_cabeca{at(he, hl, a)}.png", "duration": b - a,
                              "step": args.step if a in body_starts else 0})
    (out / "manifest.json").write_text(json.dumps(man, indent=1))
    print(f"{len(combos)} combinações, ciclo completo {total} ms, {len(man['frames'])} trocas: {out}")


if __name__ == "__main__":
    main()
