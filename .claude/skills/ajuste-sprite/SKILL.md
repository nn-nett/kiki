---
name: ajuste-sprite
description: Ciclo de ajuste fino de pixels nos sprites da Kiara (32x32) — use quando o dono apontar um detalhe ("esse pixel tá estranho", "deixa 1 px maior/mais gordinha", "falta borda", "tem um buraco"), pedir pra testar variações de uma peça, ou aprovar uma animação pra salvar nos arquivos finais. Cobre localizar o pixel, gerar variantes em todos os frames, conferir buracos/entalhes, mostrar (quadro + HTML offline + página animada), aplicar, salvar em sprites/final e commitar.
---

# Ajuste de sprite da Kiara

O dono é iniciante e vê pelo celular: ele aponta o problema com um print ou uma frase
curta. O trabalho é achar os pixels certos, mostrar opções em TODOS os frames afetados
e só aplicar o que ele escolher. Regra de ouro do `CLAUDE.md`: nada vira oficial sem
aprovação visual dele (um pedido direto e claro, tipo "tira esse pixel", já é aprovação
pra aplicar; "deixa X só pra eu ver" é teste e NÃO mexe nas peças oficiais).

## 1. Localizar
- Peças em `sprites/parts/32/` (`upper.txt` = cabeça+corpo+toquinho; `legs_*.txt` = faixas
  de pernas em y=19; ver as receitas em `sprites/anims/`). O mesmo detalhe costuma existir
  em várias peças (pose parada + 6 frames do trote), então pense em "todas as faixas".
- `python3 sprites/tools/tweak.py show PEÇA --rows a-b --cols c-d` mostra a matriz com as
  coordenadas do quadro 32x32 (as mesmas da imagem ampliada).
- Print do dono: compare com um recorte ampliado seu (`upscale` de `tools/common.py`,
  fundo #f3f3f3, grade) até ter certeza de qual pixel é. Pergunte só se for ambíguo.

## 2. Variantes
```
python3 sprites/tools/tweak.py try SCRATCH/teste antes \
    "A=upper@24,3:.>X upper@24,4:.>X" "B=legs_*@12-16,24:.>K" \
    --recipes stand walk_b --crop 0,12,28,32 --zoom 8
```
- `peça@x,y:velho>novo`, x/y aceitam faixa (12-16), peça aceita curinga (`legs_trotB?`),
  "velho" lista as letras que podem ser trocadas (protege contra apagar o que não devia).
- `--from SCRATCH/teste/A/parts` encadeia em cima de outra variante.
- Ele imprime BURACO (transparente preso), pixel solto e entalhe NOVO (vão de 1 px criado
  pela mudança). Buraco e pixel solto = conserte antes de mostrar; entalhe novo = olhe:
  entre pernas é normal, na barriga/peito/borda o dono enxerga como "espaço branco".
- Abra `SCRATCH/teste/quadro.png` (Read) e escolha uma recomendação. Mostre 2-3 opções no
  máximo, com a recomendada primeiro.

Coisas que o dono já ensinou (não repetir):
- bordas de baixo (barriga, peito, pernas) em `X`, o preto mais escuro;
- perna de longe fica ATRÁS da barriga/peito: sem castanho dela nessa altura;
- nada de pixel solto nem orelha sem borda dos dois lados;
- cor nova só se pedir (a pele `p` na barriga foi reprovada);
- trabalhar sem o contorno grisalho nos previews (o contorno sai por filtro no final).

## 3. Mostrar
- Quadro(s) PNG do `try` + HTML offline (abre no celular sem internet):
  `python3 sprites/tools/preview_html.py --out sprites/previews/<anim>/kiara_<anim>_offline.html --title ... --intro ... "Nome|nota|SCRATCH/teste/A/out/walk_b|SCRATCH/teste/A/out/stand/stand_0.png" ...`
- Página animada (artifact): `python3 sprites/tools/page.py --out SCRATCH/page/kiara_andando.html --title ... --intro ... [--step 2] "Nome|nota|pasta|parada.png" ...`
  e publique com a ferramenta Artifact SEMPRE no mesmo caminho de arquivo (mantém o link
  que está no `CLAUDE.md`). `--step` = px do sprite por frame na taskbar (andar 1, correr 2).
- Mande os arquivos com SendUserFile (quadro de perto + HTML offline).

## 4. Aplicar (só a escolhida)
- `python3 sprites/tools/tweak.py apply SCRATCH/teste/A --note "o que mudou (pedido do dono)"`
  copia as peças mudadas e regenera `sprites/base/kiara_32.{txt,png,_contorno.png}`.
- Lint: `python3 sprites/tools/lint.py --size 32 32 <saídas do rig>` — sem contorno, o único
  erro aceito é "silhueta some na taskbar escura"; a variante `_contorno` tem que passar limpa.
- Animação aprovada pelo dono → adicionar em `sprites/final/aprovadas.json` (receita +
  `step_px`) e rodar `python3 sprites/tools/export_final.py` (gera `sprites/final/` e refaz a
  galeria `sprites/final/galeria.html`). Republique a galeria com a ferramenta Artifact usando
  esse mesmo arquivo (mantém o link do `CLAUDE.md`) e mande o link pro dono: ele pediu pra ver
  sempre o que já está guardado.
- Atualizar `CLAUDE.md` (estado, decisão, checklist), commit pequeno com o motivo
  ("pedido do dono: ...") e push na branch da sessão.

## 5. Responder
Em português simples: o que era o problema (1 frase), o que mudou, onde ver, e a pergunta
de escolha/aprovação. Sem jargão de código.
