# Correndo / galope (6 frames, articulado) 32x32 - log das rodadas

Arquivos: `legs_run0..5.txt` (esta pasta) e `../../anims/run.json`. `upper.txt`, `legs_base.txt`, `legs_trotB*.txt`,
a paleta e as ferramentas não foram tocados. Sequência 0..5, 70 ms por frame (420 ms o ciclo), `legs` em `at [0,19]`,
`upper` com `offset` [0,0] nos frames 0, 3 e 5 e [0,1] nos 1, 2 e 4. `airborne: true` nos frames 0 e 3. Variantes
`contorno` (G) e `esquerda` (mirror). Os `.txt` são a fonte editável; foram montados por um gerador de apoio (faixas
diagonais por linha + remendos de 1 px, no scratchpad) e conferidos por script. Critério visual do dono: versão SEM
contorno (o lint dela só acusa "silhueta some na taskbar escura", esperado; a `run_contorno` dá "nenhum problema").

Atenção ao renderizar: as peças estão em `sprites/parts/32`, então o comando precisa de `--parts sprites/parts/32`
(sem isso o rig procura em `sprites/parts/` e dá "peça não encontrada").

## Desenho do ciclo (galope rotativo)

- Par da frente (FN = dianteira de perto, FF = de longe) pousa e empurra junto nos frames 1-2; par de trás (RN =
  traseira de perto, RF = de longe) pousa e empurra junto nos frames 4-5; frames 0 e 3 são as duas fases no ar.
- F0 estendido no ar: dianteiras esticadas pra frente em diagonal (patas nas colunas ~23-30, sola na linha 29, a 2 px do
  chão), traseiras esticadas pra trás (patas nas colunas 0-6, solas nas linhas 28-29). Faixa de 2 px a 45 graus. A
  traseira de perto tem uma dobra leve no jarrete (tíbia mais rasa, metatarso mais íngreme). Barriga com X de 7 px.
- F1 dianteira de perto pousa: faixa diagonal pra frente (cotovelo no alto, antebraço, pata) com a pata no chão em
  col. 28 (sola `KXXX`, linha 31); a de longe chega logo atrás (sola na linha 30, 1 px acima do chão); traseiras
  dobradas vindo pra frente no ar: "<" com o jarrete pra trás (col. 3, linha 25) e a pata pra frente, a de longe
  parcialmente atrás da de perto.
- F2 dianteiras apoiadas: de perto em col. 26 (recuou 2 px), de longe plantada em col. 22; as duas com a parte de cima em
  diagonal de 2 px e a canela/pata de 1 px (`XtX`, como no trote B). Traseiras já embaixo da barriga, dobradas em "L"
  (canela quase vertical, metatarso pra frente), solas na linha 30 (quase tocando).
- F3 recolhido no ar: dianteiras dobradas pra trás (cotovelo pra baixo, antebraço pra trás, patas nas colunas 16-22,
  sola na linha 29); traseiras esticadas pra frente em diagonal com um zigue-zague no jarrete (patas nas colunas 9-12,
  sola na linha 28-29). Barriga curta (X de 4 px). Sobra um vão de 2-3 colunas entre as patas de trás e as da frente
  (sem bolsão).
- F4 traseiras pousam: de longe em col. 13 e de perto em col. 11 (a de perto com Z: coxa, jarrete atrás, metatarso
  pra frente), dianteiras se abrindo pra frente no ar (faixa de 2 px, solas na linha 29).
- F5 traseiras empurram: col. 11 e 9 (recuaram 2 px), canelas de 1 px bem separadas (`XtXTX`), dianteiras mais
  esticadas pra frente, no ar. Rabo/garupa 1 px mais pra trás (coluna 2), como no frame 0 do trote B.
- Profundidade como no trote B: de perto `t` com contorno `X`; de longe `T` (e `K` no topo), sem castanho na altura da
  barriga (nenhum T/D nas linhas <= 23; a traseira de longe só tem T a partir da linha 25, a dianteira de longe a
  partir da 24). Barriga até a linha 24 com X embaixo e peito até a 23 com X embaixo em todos os frames.

## Anti-patinação (conferido por script, linha 30 = coluna do tan, linha 31 = sola)

A janela anda 2 px do sprite por frame; toda pata plantada recua exatamente 2 px por frame no chão.

| perna | F0 | F1 | F2 | F3 | F4 | F5 |
|---|---|---|---|---|---|---|
| FN dianteira de perto | ar | 28 (sola 27-30) | 26 (sola 25-28) | ar | ar | ar |
| FF dianteira de longe | ar | ar (sola linha 30) | 22 (sola 21-23) | ar | ar | ar |
| RN traseira de perto | ar | ar | ar (sola linha 30) | ar | 11 (sola 11-12) | 9 (sola 9-10) |
| RF traseira de longe | ar | ar | ar (sola linha 30) | ar | 13 (sola 13-14) | 11 (sola 11-12) |

FN 28 -> 26 (-2), RN 11 -> 9 (-2), RF 13 -> 11 (-2). FF só toca em um frame (F2), então não há o que patinar.
Nos frames 0 e 3 nada toca o chão (por isso `airborne`).

## Rodada 1 (rascunho automático com pernas de 1 px)

Primeira versão por gerador de polilinhas (1 px de tan + contorno nos 4 vizinhos). Visto na folha ampliada: o galope já
lia (estendido, pousando, recolhido), mas as pernas diagonais viraram "fio de arame" com um xadrez de X (contorno em 45
graus), mais finas que as do trote, e o frame 3 virou um "cesto": traseiras indo pra frente e dianteiras indo pra trás se
cruzavam embaixo da barriga e fechavam um bolsão. Refiz as pernas como faixas de 2 px de tan (contorno X só à esquerda e
à direita de cada linha), no estilo da traseira de perto do trote B (`Xtt`), e no frame 3 deixei um vão entre as patas.

## Rodada 2 (conferência por script: buracos presos e entalhes de 1 px)

Script (flood fill a partir da borda, 4-vizinhos, mais "entalhe" = pixel transparente com 3 vizinhos opacos nas linhas
22-25, colunas 3-26) achou: F0 bolsão de 1 px entre as dianteiras (as inclinações eram diferentes); F1 bolsão (3 a 9 px, conforme a variante) entre
as duas traseiras em "<"; F2 entalhe na garupa (4,24); F3 bolsão de 6 px entre as traseiras e as dianteiras; F4 bolsão
entre as dianteiras e entalhes embaixo da barriga (12,25) e (22,25). Corrigi com inclinações iguais no par da frente,
traseira de longe parcialmente atrás da de perto (sem bolsão) ou bem afastada, vão de 2 colunas entre patas no frame 3 e
remendos de 1 px nas pontas cegas: F0 (6,24) X, F1 (6,25) K, F2 (4,24) X, F3 (12,25) e (17,25) X, F4 (12,25) X.
Resultado: 0 buracos e 0 entalhes nos 6 frames.

## Rodada 3 (leitura em 2x na taskbar clara + articulação)

Em 2x sobre #f3f3f3 o ciclo lia como cachorro correndo, mas as pernas apoiadas estavam pesadas: no frame 5 a traseira de
perto e a de longe viravam um pilar único de 5 px, e no frame 2 as traseiras se fundiam numa mancha. Decisões: pernas
apoiadas com a canela/pata de 1 px (`XtX`, `XTX`, como no trote B) e só a parte de cima em faixa de 2 px; no frame 2 as
traseiras viraram dois "L" separados, cada um com a sua sola (`KKK.KK`); no frame 5 as canelas ficaram a 1 coluna uma da
outra com um X só no meio (`XtXTX`); no frame 0 a traseira de perto ganhou a dobra do jarrete; no frame 3 a traseira de
perto ganhou o Z e a dianteira de perto o cotovelo (antes eram varetas retas); no frame 4 o Z da traseira de perto.
Testei também afilar a ponta de todas as pernas (últimas 2-3 linhas de 1 px): nas diagonais do frame 0 fica "arame"
de novo, então só as pernas apoiadas afinam.

## Rodada 4 (conferência final)

Re-rodei buracos/entalhes (0/0), a regra das pernas de longe (nenhum T/D nas linhas <= 23, nenhum na traseira de longe
na linha 24), a barriga (X >= 4 px na linha 24) e o peito (X >= 3 px na linha 23), a anti-patinação (tabela acima), a
conectividade (1 só mancha por frame, 8-vizinhos) e o lint. Lint: `run` e `run_esquerda` só com "silhueta some na
taskbar escura" (esperado, 6 frames cada); `run_contorno` com 0 erros e 0 avisos. Ajustes finais: remendo do F1 de X
pra K (some no corpo) e sola do F2 separada. Folha final: `quadro.png` (8x sobre #f3f3f3, fora do repositório).

## Pontos pro diretor

- Patas traseiras no pouso: ficaram nas colunas 11 e 13 (F4) e 9 e 11 (F5), um pouco mais atrás que o "~11-15" pedido.
  Com a garupa na coluna 3-5, patas em 13-15 deixam a perna comprida demais pra frente e o "empurrar" (F5) lê como freada.
  Dá pra deslocar tudo +2 (e F5 em 11/13) se preferir; muda só as colunas das pernas de trás nos frames 4 e 5.
- Balanço do corpo: só 1 px de diferença entre alto e baixo (as orelhas na linha 0 impedem subir). Se quiser mais peso na
  pisada, o frame 2 aguenta `offset [0,2]` (a faixa das pernas não muda).
- Ciclo de 6 x 70 ms = 420 ms; a janela anda 2 px do sprite por frame (4 px de tela em 2x): 12 px do sprite por ciclo, o
  que é lento pra galope. Se o app quiser correr mais, o certo é acelerar o ciclo e andar mais px por frame, mas aí a
  anti-patinação pede pernas recuando junto (refazer as colunas das pernas apoiadas).
- Dianteira de longe só toca o chão no frame 2 (1 frame); a de perto toca em 2 (1 e 2). Se preferir as duas em 2 frames,
  a de longe pousaria no 1 em col. 24 e recuaria pra 22.
