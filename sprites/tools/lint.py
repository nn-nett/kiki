"""Checagens objetivas dos frames de sprite (o "lint" antes de qualquer olho humano).

Cada pasta (ou lista de arquivos) é tratada como UMA animação.

Por frame (ERRO): tamanho certo, só alpha 0 ou 255, só cores da paleta, frame
não vazio, e contraste da borda contra a taskbar escura/clara do Windows 11
(WCAG: borda "visível" = razão >= 1.6; erro se < 35% da borda é visível).

Por animação: ERRO se os pés (linha opaca mais baixa) não ficam na mesma linha
em todos os frames não-airborne; AVISO se mais de 35% do canvas muda entre frames
consecutivos (o "pulo de desenho") ou se a área da silhueta varia > 20%.

Entradas aceitas: pasta com manifest.json (usa a ordem e os flags do manifest),
pasta sem manifest (todos os .png em ordem natural; subpastas também são
varridas), ou lista de arquivos .png/.txt (na ordem dada).

Uso:
  python3 sprites/tools/lint.py sprites/out/walk
  python3 sprites/tools/lint.py sprites/out                 # varre as subpastas
  python3 sprites/tools/lint.py f0.png f1.png f2.png --size 24 24
  python3 sprites/tools/lint.py sprites/out --json          # problemas em JSON

Sai com código 1 se houver algum erro (2 se a entrada não existir ou estiver vazia).
"""
import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

from PIL import Image

from common import (
    TASKBAR_DARK,
    TASKBAR_LIGHT,
    load_palette,
    matrix_to_image,
    nearest_letter,
    parse_matrix,
    rgb2hex,
)

MIN_CONTRAST = 1.6      # razão WCAG mínima pra um pixel de borda contar como visível
MIN_VISIBLE = 0.35      # fração mínima da borda visível num fundo
MAX_CHANGE = 0.35       # fração do canvas que muda entre frames consecutivos
MAX_AREA_CHANGE = 0.20  # variação da área da silhueta entre frames consecutivos

BACKGROUNDS = (
    ("escura", TASKBAR_DARK, "silhueta_some_escura"),
    ("clara", TASKBAR_LIGHT, "silhueta_some_clara"),
)


def plural(n, one, many):
    return f"{n} {one if n == 1 else many}"


# ---------- leitura de sprites e de animações (reaproveitado por review/compare)

def natural_key(path):
    """Ordem natural: walk_2.png antes de walk_10.png."""
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", Path(path).name)]


def load_sprite(path, palette=None):
    """.png (ou outra imagem) -> RGBA; .txt -> matriz de letras convertida em RGBA."""
    path = Path(path)
    if path.suffix.lower() == ".txt":
        rows, _ = parse_matrix(path)
        return matrix_to_image(rows, palette)
    return Image.open(path).convert("RGBA")


def read_manifest(path):
    """manifest.json -> {name, loop, entries=[(arquivo, airborne)...], problems}."""
    path = Path(path)
    anim = {"name": path.parent.name, "loop": True, "entries": [], "problems": []}
    try:
        data = json.loads(path.read_text())
        anim["name"] = data.get("name") or anim["name"]
        anim["loop"] = bool(data.get("loop", True))
        for fr in data["frames"]:
            anim["entries"].append((path.parent / fr["file"], bool(fr.get("airborne", False))))
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as e:
        anim["entries"] = []
        anim["problems"].append(("erro", "manifest_invalido", f"manifest.json ilegível: {e!r}", path))
    return anim


def discover(folder):
    """Animações de uma pasta: manifest.json, ou os .png dela; depois as subpastas."""
    folder = Path(folder)
    manifest = folder / "manifest.json"
    if manifest.is_file():
        return [read_manifest(manifest)]
    found = []
    pngs = sorted(folder.glob("*.png"), key=natural_key)
    if pngs:
        found.append({"name": folder.name, "loop": True, "problems": [],
                      "entries": [(p, False) for p in pngs]})
    for sub in sorted(p for p in folder.iterdir() if p.is_dir() and not p.name.startswith(".")):
        found += discover(sub)
    return found


def collect_animations(paths):
    """Lista de caminhos (pastas, manifests, arquivos soltos) -> lista de animações."""
    anims, loose = [], []
    for raw in paths:
        p = Path(raw)
        if p.is_dir():
            anims += discover(p)
        elif p.suffix.lower() == ".json":
            anims.append(read_manifest(p))
        else:
            loose.append(p)
    if loose:
        if len(loose) == 1:
            name = loose[0].stem
        else:
            parents = {p.parent for p in loose}
            name = parents.pop().name if len(parents) == 1 else "arquivos"
        anims.append({"name": name or "arquivos", "loop": True, "problems": [],
                      "entries": [(p, False) for p in loose]})
    return anims


# ---------- geometria

class Frame:
    def __init__(self, path, img):
        self.path, self.label = Path(path), Path(path).name
        self.w, self.h = img.size
        self.px = list(zip(*[iter(img.tobytes())] * 4))  # [(r, g, b, a), ...]
        rows = [i // self.w for i, p in enumerate(self.px) if p[3] > 0]
        self.area = len(rows)
        self.bottom = max(rows) if rows else None  # linha opaca mais baixa


def border_colors(fr):
    """Cores dos pixels de borda: opacos com algum vizinho-4 transparente/fora."""
    out = []
    for i, p in enumerate(fr.px):
        if p[3] == 0:
            continue
        y, x = divmod(i, fr.w)
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if not (0 <= nx < fr.w and 0 <= ny < fr.h) or fr.px[ny * fr.w + nx][3] == 0:
                out.append(p[:3])
                break
    return out


def luminance(rgb):
    def lin(c):
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (lin(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(c1, c2):
    a, b = sorted((luminance(c1), luminance(c2)), reverse=True)
    return (a + 0.05) / (b + 0.05)


def visible_fraction(colors, bg):
    return sum(1 for c in colors if contrast_ratio(c, bg) >= MIN_CONTRAST) / len(colors)


def padded(fr, w, h):
    if (fr.w, fr.h) == (w, h):
        return fr.px
    out = [(0, 0, 0, 0)] * (w * h)
    for y in range(fr.h):
        out[y * w : y * w + fr.w] = fr.px[y * fr.w : (y + 1) * fr.w]
    return out


def change_fraction(a, b):
    """Pixels que mudam / pixels do canvas (transparente vs. transparente não muda)."""
    w, h = max(a.w, b.w), max(a.h, b.h)
    changed = sum(
        1 for pa, pb in zip(padded(a, w, h), padded(b, w, h))
        if pa != pb and (pa[3] or pb[3])
    )
    return changed / (w * h)


# ---------- checagens

def analyze(anim, size, palette, loop):
    """Roda todas as checagens de uma animação. Retorna (problemas, linhas_info)."""
    problems, info = [], []

    def add(nivel, codigo, msg, fr=None, **dados):
        problems.append({
            "anim": anim["name"], "frame": fr.label if fr else None,
            "arquivo": str(fr.path) if fr else None,
            "nivel": nivel, "codigo": codigo, "mensagem": msg, **({"dados": dados} if dados else {}),
        })

    for nivel, codigo, msg, path in anim["problems"]:
        problems.append({"anim": anim["name"], "frame": None, "arquivo": str(path),
                         "nivel": nivel, "codigo": codigo, "mensagem": msg})

    frames, seq = {}, []  # frames: caminho -> Frame (1 por arquivo); seq: [(Frame, airborne)]
    for path, airborne in anim["entries"]:
        if path not in frames:
            try:
                frames[path] = Frame(path, load_sprite(path, palette))
            except (OSError, ValueError) as e:
                msg = "arquivo não existe" if not path.exists() else f"não consegui ler: {e}"
                problems.append({"anim": anim["name"], "frame": path.name, "arquivo": str(path),
                                 "nivel": "erro", "codigo": "arquivo_invalido", "mensagem": msg})
                frames[path] = None
        if frames[path]:
            seq.append((frames[path], airborne))
    loaded = [f for f in frames.values() if f]
    palette_rgb = set(palette.values())
    info.append(f"{plural(len(loaded), 'arquivo', 'arquivos')}, "
                f"{plural(len(seq), 'frame', 'frames')} na sequência, "
                f"{'loop' if loop else 'sem loop'}, esperado {size[0]}x{size[1]}")

    # --- por frame
    for fr in loaded:
        if (fr.w, fr.h) != tuple(size):
            add("erro", "tamanho", f"tamanho {fr.w}x{fr.h}, esperado {size[0]}x{size[1]}", fr)
        semi = sum(1 for p in fr.px if 0 < p[3] < 255)
        if semi:
            add("erro", "semitransparencia",
                f"{plural(semi, 'pixel semitransparente', 'pixels semitransparentes')} "
                f"(alpha entre 1 e 254); só vale 0 ou 255", fr, pixels=semi)
        off = Counter(p[:3] for p in fr.px if p[3] == 255 and p[:3] not in palette_rgb)
        if off:
            top = ", ".join(f"{rgb2hex(c)} x{n} (perto de {nearest_letter(c, palette)})"
                            for c, n in off.most_common(6))
            extra = f" e mais {len(off) - 6} cores" if len(off) > 6 else ""
            add("erro", "cor_fora_da_paleta",
                f"{plural(sum(off.values()), 'pixel', 'pixels')} com "
                f"{plural(len(off), 'cor', 'cores')} fora da paleta: {top}{extra}", fr,
                cores={rgb2hex(c): n for c, n in off.items()})
        if fr.area == 0:
            add("erro", "vazio", "frame vazio (nenhum pixel visível)", fr)
            continue

        border = border_colors(fr)
        pcts = []
        for nome, bg, codigo in BACKGROUNDS:
            frac = visible_fraction(border, bg)
            pcts.append(f"{nome} {frac * 100:.1f}%")
            if frac < MIN_VISIBLE:
                add("erro", codigo,
                    f"silhueta some na taskbar {nome} ({frac * 100:.1f}% da borda visível)", fr,
                    borda_visivel=round(frac, 3), pixels_de_borda=len(border))
        info.append(f"{fr.label}: borda visível (razão >= {MIN_CONTRAST}) na taskbar " + " | ".join(pcts))

    # --- por animação: pés no chão
    ground = {fr.path: fr for fr, airborne in seq if not airborne and fr.bottom is not None}
    if len({fr.bottom for fr in ground.values()}) > 1:
        counts = Counter(fr.bottom for fr in ground.values())
        ref = max(counts, key=lambda r: (counts[r], r))
        for fr in ground.values():
            if fr.bottom != ref:
                d = fr.bottom - ref
                como = f"flutua {-d}px acima" if d < 0 else f"fica {d}px abaixo"
                add("erro", "pes_no_chao",
                    f"pés na linha {fr.bottom}, mas {counts[ref]} frames têm os pés na linha {ref} ({como})",
                    fr, linha=fr.bottom, linha_esperada=ref)

    # --- por animação: pares consecutivos (inclui último -> primeiro se loop)
    pairs = [(a, b, False) for (a, _), (b, _) in zip(seq, seq[1:])]
    if loop and len(seq) > 1:
        pairs.append((seq[-1][0], seq[0][0], True))
    seen = set()
    for a, b, wrap in pairs:
        key = frozenset((a.path, b.path))
        if a is b or key in seen:
            continue
        seen.add(key)
        par = f"{a.label} -> {b.label}" + (" (fim -> início do loop)" if wrap else "")
        frac = change_fraction(a, b)
        if frac > MAX_CHANGE:
            problems.append({
                "anim": anim["name"], "frame": b.label, "arquivo": str(b.path), "nivel": "aviso",
                "codigo": "pulo_de_desenho", "dados": {"de": a.label, "para": b.label, "fracao": round(frac, 3)},
                "mensagem": f"{frac * 100:.0f}% dos pixels mudam em {par} (limite {MAX_CHANGE * 100:.0f}%)"})
        if a.area and b.area:
            var = abs(a.area - b.area) / max(a.area, b.area)
            if var > MAX_AREA_CHANGE:
                problems.append({
                    "anim": anim["name"], "frame": b.label, "arquivo": str(b.path), "nivel": "aviso",
                    "codigo": "area_varia", "dados": {"de": a.label, "para": b.label, "variacao": round(var, 3)},
                    "mensagem": f"área da silhueta varia {var * 100:.0f}% em {par} "
                                f"({a.area} -> {b.area} pixels; limite {MAX_AREA_CHANGE * 100:.0f}%)"})
    return problems, info


def main():
    ap = argparse.ArgumentParser(description="Checagens objetivas dos frames de sprite.")
    ap.add_argument("paths", nargs="+",
                    help="pastas (com ou sem manifest.json) ou arquivos .png/.txt; "
                         "cada pasta, e a lista de arquivos soltos, é uma animação")
    ap.add_argument("--size", nargs=2, type=int, default=[24, 24], metavar=("L", "A"),
                    help="tamanho esperado dos frames (padrão: 24 24)")
    ap.add_argument("--sem-loop", action="store_true",
                    help="não compara o último frame com o primeiro (manifest com loop:false já faz isso)")
    ap.add_argument("--json", action="store_true", help="imprime só a lista de problemas em JSON")
    args = ap.parse_args()

    missing = [p for p in args.paths if not Path(p).exists()]
    anims = [] if missing else collect_animations(args.paths)
    if missing or not anims:
        motivo = f"não existe: {', '.join(missing)}" if missing else "nenhum frame encontrado nas entradas"
        print(f"ERRO: {motivo}", file=sys.stderr)
        sys.exit(2)

    palette = load_palette()
    all_problems = []
    for anim in anims:
        problems, info = analyze(anim, args.size, palette, anim["loop"] and not args.sem_loop)
        all_problems += problems
        if args.json:
            continue
        print(f"== {anim['name']}  ({info[0]})")
        for line in info[1:]:
            print(f"   info   {line}")
        for p in problems:
            onde = p["frame"] or "animação"
            print(f"   {p['nivel'].upper():<6} {onde}: {p['mensagem']}")
        if not problems:
            print("   ok     nenhum problema")

    erros = sum(p["nivel"] == "erro" for p in all_problems)
    avisos = sum(p["nivel"] == "aviso" for p in all_problems)
    if args.json:
        print(json.dumps(all_problems, ensure_ascii=False, indent=2))
    else:
        print(f"\n{plural(erros, 'erro', 'erros')}, {plural(avisos, 'aviso', 'avisos')}")
    sys.exit(1 if erros else 0)


if __name__ == "__main__":
    main()
