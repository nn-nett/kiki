"""Rota B: foto real -> sprite em qualquer tamanho (8, 16, 32, 64...).

Usa a segmentação da foto lateral do similarity.py (cachorra recortada, guia
removida, peitoral e saia viram preto, espelhada pra olhar à direita). Cada
pixel da foto ganha uma letra da paleta e cada célula do sprite fica com a
letra mais votada. Quanto maior o tamanho, mais tons entram:

  tier  8: K T G                (3 cores: silhueta + tan + grisalho)
  tier 16: K k T D G W          (6)
  tier 32: X K k D T t G W      (8)
  tier 64: X K k D T t G W      (8, com mais detalhe por ter mais células)

Os tons dentro de cada classe (preto, tan, grisalho) saem dos percentis de
brilho da própria foto, então se adaptam à luz dela.

Uso:
  python3 sprites/tools/photo2sprite.py saida_prefixo --size 32 [--photo foto.jpg]
"""
import argparse

import cv2
import numpy as np
from PIL import Image

from common import TRANSPARENT, matrix_to_image, upscale, write_matrix
from similarity import CG, CK, CT, PHOTO, classify_pixels, segment

TIERS = {
    8: {CK: ["K"], CT: ["T"], CG: ["G"]},
    16: {CK: ["K", "k"], CT: ["D", "T"], CG: ["G", "W"]},
    32: {CK: ["X", "K", "k"], CT: ["D", "T", "t"], CG: ["G", "W"]},
    64: {CK: ["X", "K", "k"], CT: ["D", "T", "t"], CG: ["G", "W"]},
}
# peso do voto: classes raras e importantes (tan, grisalho) ganham empates
WEIGHT = {CK: 1.0, CT: 1.35, CG: 1.6}


def tier_for(size):
    return TIERS[min(TIERS, key=lambda t: abs(t - size))]


def letter_map(rgb, cls, fg, tones):
    """Letra de cada pixel da foto: classe + tom pelo percentil de brilho."""
    val = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)[..., 2].astype(np.float32)
    out = np.full(cls.shape, "", dtype="<U1")
    for c, letters in tones.items():
        sel = (cls == c) & fg
        if not sel.any():
            continue
        n = len(letters)
        cuts = np.percentile(val[sel], [100 * i / n for i in range(1, n)]) if n > 1 else []
        idx = np.digitize(val, cuts) if n > 1 else np.zeros(val.shape, int)
        for i, ch in enumerate(letters):
            out[sel & (idx == i)] = ch
    return out


def photo_to_rows(photo, size, thr=0.35):
    rgb = np.asarray(Image.open(photo).convert("RGB"))
    fg = segment(rgb)
    ys, xs = np.where(fg)
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    fg = fg[y0:y1, x0:x1][:, ::-1]
    rgb = np.ascontiguousarray(rgb[y0:y1, x0:x1][:, ::-1])
    cls, _ = classify_pixels(rgb, fg)
    tones = tier_for(size)
    letters = letter_map(rgb, cls, fg, tones)
    h, w = fg.shape

    # quadro quadrado: centralizado, pés na base
    L = max(w, h)
    ox, oy = (L - w) // 2, L - h

    def canvas(a):
        c = np.zeros((L, L), np.float32)
        c[oy:oy + h, ox:ox + w] = a
        return cv2.resize(c, (size, size), interpolation=cv2.INTER_AREA)

    mask = canvas(fg.astype(np.float32)) >= thr
    names = [ch for c in tones for ch in tones[c]]
    weights = np.array([WEIGHT[c] for c in tones for _ in tones[c]], np.float32)
    votes = np.stack([canvas((letters == ch).astype(np.float32)) for ch in names])
    best = np.argmax(votes * weights[:, None, None], axis=0)
    return [
        "".join(names[best[y, x]] if mask[y, x] else TRANSPARENT for x in range(size))
        for y in range(size)
    ]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("saida", help="prefixo de saída (gera .txt, .png e _x8.png)")
    ap.add_argument("--size", type=int, default=32, help="lado do quadro (8, 16, 32, 64)")
    ap.add_argument("--photo", default=str(PHOTO), help="foto lateral da Kiara")
    ap.add_argument("--thr", type=float, default=0.35,
                    help="cobertura mínima da célula pra virar cachorra")
    args = ap.parse_args()

    rows = photo_to_rows(args.photo, args.size, args.thr)
    write_matrix(f"{args.saida}.txt", rows, [
        f"Rota B: foto -> sprite {args.size}x{args.size} (photo2sprite.py)",
    ])
    img = matrix_to_image(rows)
    img.save(f"{args.saida}.png")
    upscale(img, max(1, 192 // args.size), bg="checker").save(f"{args.saida}_x8.png")
    print(f"gravado {args.saida}.txt/.png ({args.size}x{args.size})")


if __name__ == "__main__":
    main()
