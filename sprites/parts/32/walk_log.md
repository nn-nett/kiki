# Andando (trote) 32x32 — log das rodadas

Arquivos: `legs_walk0..3.txt` (esta pasta) e `../../anims/walk.json`. A peça `upper.txt` e a
`legs_base.txt` não foram tocadas. Origem de tudo: `legs_base.txt`, redesenhada só nas pernas.

## Desenho do ciclo (valem para as 4 rodadas)

- Pares diagonais: A = dianteira de perto + traseira de longe; B = dianteira de longe + traseira de perto.
- Sequência 0,1,2,3 em loop, 130 ms por frame. Frames 1 e 3: `upper` com `offset [0,-1]`.
- Perna parada = topo fixo (as 2–3 primeiras linhas debaixo do corpo) e o resto "entorta" 1px a cada ~3 linhas.
  Perna levantada = 2 linhas a menos na canela, pata mais curta e 1px pra frente.
- Deslocamento do pé (coluna, relativo à base; na linha 31):

  | perna | frame 0 | frame 1 | frame 2 | frame 3 |
  |---|---|---|---|---|
  | dianteira de perto (A) | +2 | +1 | 0 | levantada |
  | traseira de longe (A)  | +1 | 0 | -1 | levantada |
  | dianteira de longe (B) | -2 | levantada | 0 | -1 |
  | traseira de perto (B)  | -2 | levantada | 0 | -1 |

  Toda pata plantada recua exatamente 1px por frame (não escorrega); as levantadas só avançam.
- Por que a passada é só de 1px por frame: as 4 pernas da base têm só 1–2 colunas de vão entre elas
  (traseira de perto/de longe: 2; dianteira de longe/de perto: 1). Com 2px por frame as patas se
  tocam e fecham buracos transparentes dentro da silhueta. As dianteiras foram deslocadas 1px
  pra fora da posição da base (dianteira de longe pra trás, de perto pra frente) e a traseira
  de perto 1px pra trás, pra ganhar espaço. Por isso o frame 2 fica parecido com a pose parada.
- Linhas 20–21 da faixa (o corpo): a 20 repete a 21 e a 21 afina a mancha do peito (`tWtX`).
  Quando o corpo sobe 1px, a linha 21 aparece de verdade; com a linha 21 da base, a mancha ficava
  com duas linhas iguais seguidas, e o X da coluna 23 da linha 20 ficava solto fora do peito.
  Nos frames 0 e 2 essas linhas ficam tapadas pela peça de cima.

## Rodada 1 (primeiro rascunho: dianteira de perto -2/0/+2, traseira de longe -1/0/+1, dianteira de longe e traseira de perto -2/-1/0)

Visto: pares diagonais certos (frame 1 levanta dianteira de longe + traseira de perto; frame 3,
dianteira de perto + traseira de longe); pés na linha 31 em todos os frames; peça de cima idêntica
à base (0 px diferentes nas linhas 0–19).
Problemas:
1. Frame 2: com a dianteira de perto recuada 2px e a de longe na posição da base, as duas se
   tocavam embaixo (coluna 17|18) e sobrava um buraco transparente preso de 3 px (coluna 18,
   linhas 24–26), com um blob preto no pé.
2. Frames 1 e 3: sobrava 1 px solto (X em 23,20) engrossando o contorno do peito.
3. A dianteira de perto andava 2px por frame e as outras 1px (escorregava em relação às demais).
Lint: só o erro esperado "silhueta some na taskbar escura" (4 frames); contorno limpo.

## Rodada 2 (a que ficou)

Mudanças: dianteira de perto passou a +2/+1/0 nos frames 0/1/2 (1px por frame como as outras, sem tocar a
dianteira de longe no frame 2); linha 20 = 21 e linha 21 afinada. Checagem por script: nenhum buraco transparente preso nos 4 frames; peça de cima
idêntica à base nas linhas 0–19 (frames 1 e 3 deslocados 1px pra cima); cada pé recua 1px/frame.
Lint: igual ao da rodada 1 (só o erro esperado); `walk_contorno` limpo.
Visto na folha: o frame 0 abre as pernas (A à frente, B atrás), o 2 fecha (B à frente), e os
frames 1 e 3 mostram dois pares levantados em diagonal. Peito afinado ficou bom.

## Rodada 3 (experimento, descartado)

Tentei dobrar a pata levantada da dianteira de longe (frame 1) 1px pra frente. Fechou um buraco
preso de 5 px (coluna 18, linhas 24–28) contra a dianteira de perto. Voltei ao desenho da rodada 2
(arquivos idênticos, conferido com diff).

## Rodada 4 (conferência final)

Corrigi uma linha com 33 colunas (a linha 21 das faixas, 1 coluna a mais que o resto, sem efeito no
desenho porque a coluna extra era transparente). Rodei tudo de novo: rig, lint (walk, walk_contorno,
walk_esquerda), folha de revisão e as checagens de script (peça de cima, buracos, pés).
Lint `walk_contorno`: 0 erros, 0 avisos. Lint `walk` e `walk_esquerda`: só "silhueta some na
taskbar escura", que é esperado na versão sem contorno.

## Pontos que ficam pro diretor decidir

- **Pontas das orelhas cortadas nos frames 1 e 3.** A linha 0 da peça de cima tem as pontas das
  duas orelhas (4 px). Com `offset [0,-1]` elas saem do quadro (o rig avisa "4 px fora do quadro")
  e a orelha esquerda fica com o topo chato por 130 ms. Saídas: (a) aceitar; (b) inverter a
  oscilação: corpo 1px mais baixo nos frames 0 e 2 (`offset [0,+1]`) e normal nos 1 e 3, o que é
  até mais natural (corpo mais baixo no contato, mais alto na passagem), mas exige refazer as linhas
  22–24 das faixas dos frames 0 e 2.
- **Velocidade do chão:** cada pata plantada recua 1px por frame, ou 7,7 px/s no sprite. Na
  taskbar (ampliado 2x) a janela tem que andar 2 px de tela por frame, cerca de 15 px/s, pra ela
  não "patinar".
- **Patas de longe não são mais escuras na base** (só o pixel D em 9,25 da traseira de longe).
  Mantive igual à base. Se quiserem profundidade, trocar o tan `t` das patas de longe por `T`
  nas 4 faixas e na `legs_base`.

## Revisão do Opus
- Oscilação do corpo invertida: em vez de subir 1px nas passagens (cortava a ponta das
  orelhas, que estão na linha 0), o corpo desce 1px nos contatos (frames 0 e 2) e fica
  na altura normal nas passagens. Mais natural e sem nada fora do quadro.
- Juiz Haiku (frame a frame): mesma cachorra em todos, nada pula, pernas alternam,
  sem buracos. Lint da versão com contorno: 0 erros, 0 avisos.
