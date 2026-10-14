# Correndo / galope v2 (6 frames, tronco inclinando) 32x32 - log das rodadas

## v1 (reprovada) em uma linha

Galope rotativo com o `upper` inteiro rígido (só subia 1 px nos frames apoiados) e só as pernas mudando. O dono: "é
assim que você acha que cachorro corre? kkk faltou o tronco inclinar na corrida". A v1 está no git (commit 04b1f9d) e
renderizada em `scratchpad/run/final/run/`.

## Arquivos da v2

- `torso_run_estendido.txt`, `torso_run_frente_baixa.txt`, `torso_run_arqueando.txt`, `torso_run_recolhido.txt`,
  `torso_run_frente_alta.txt`, `torso_run_esticando.txt` (novos): o tronco inclinado de cada frame, tirado do
  `torso.txt` (toquinho, garupa, costas, peito com a mancha W, toco do pescoço). `@socket.pescoco 20,14` em todos.
- `legs_run0..5.txt` (reescritos): faixa das linhas 19-31 com o fundo do corpo inclinado (barriga e peito com borda X)
  e as quatro pernas, casada com o tronco daquele frame.
- `../../anims/run.json` (reescrita): `legs` em `at [0,19]`, `torso` (`torso_run_*`) e `head` (`head.txt`) encaixada
  em `torso.pescoco`. 6 frames de 70 ms (420 ms o ciclo), `airborne` nos frames 0 e 3, variantes `contorno` (G) e
  `esquerda` (mirror). `upper`, `torso`, `head`, `legs_base`, `legs_trotB*`, paleta e ferramentas não foram tocados.
- Os `.txt` são a fonte editável. Foram gerados por um script de apoio (fora do repo, `scratchpad/run2/export.py` +
  `lib.py`/`d5-d7.py`) e conferidos: o render do rig é igual, pixel a pixel, ao do gerador.

Render: `python3 sprites/tools/rig.py sprites/anims/run.json --parts sprites/parts/32 --out <saída> --gif`.

## Como o tronco inclina (sem rotação)

1. Base: `torso.txt` + um fundo de barril (linhas 21-24 da pose parada sem as pernas, barriga reta com X embaixo).
2. Cisalhamento em degraus: cada coluna desce `dy` px. `dy` vem de 3 pontos de controle na pose parada: garupa (col. 5)
   = R, meio (col. 12) = M, peito/pescoço (col. 19 em diante) = C, interpolado e arredondado. Dá degraus de 1 px a cada
   ~4-7 colunas, no máximo 2 px entre garupa e peito. Arqueado = meio 1 px acima das pontas.
3. Comprimento: repete (estica) ou tira (encolhe) colunas na col. 12 (só barriga/dorso), como o `proportion.py --body`;
   a garupa anda `dxr` e o peito `dxc` (esticado: garupa 1 pra trás e peito 1 pra frente).
4. Limpeza à mão: degraus das costas sem dente antes do pescoço, borda X da barriga/peito contínua, junção peito-perna
   fechada com X, toco do pescoço aparado na nuca quando a cabeça desce 1 px.
5. Cada peça `torso_run_*` é guardada normalizada no pescoço (o socket fica no 20,14 de sempre); o `offset` do torso na
   receita é [dxc, C] e leva o pescoço pra posição do frame. Assim a cabeça acompanha o peito.

Em vez de "abaixar a cachorra inteira" com um offset fixo, o abaixamento está no cisalhamento: garupa e peito só descem
(0 a 2 px) em relação à pose parada, nunca sobem. A orelha só encosta na linha 0 no frame 4 (frente alta), igual à
pose parada; nos outros fica 1-2 px abaixo.

| frame | pose | R/M/C (desce) | costas (garupa/meio/peito) | corpo (col.) | offset torso | offset cabeça | topo | no ar |
|---|---|---|---|---|---|---|---|---|
| 0 | estendido | 0/0/0 | 15/15/15 reto | 2-26 (25) | [1, 0] | [-1, 1] | 1 | sim |
| 1 | dianteira pousa | 0/1/2 | 15/16/17 frente pra baixo | 2-26 (25) | [1, 2] | [-1, 0] | 2 | não |
| 2 | dianteiras empurram | 1/0/2 | 16/15/17 começa a arquear | 3-25 (23) | [0, 2] | [0, 0] | 2 | não |
| 3 | recolhido | 1/0/1 | 16/15/16 arqueado | 4-24 (21) | [-1, 1] | [1, 0] | 1 | sim |
| 4 | traseiras pousam | 2/1/0 | 17/16/15 frente pra cima | 4-24 (21) | [-1, 0] | [1, 0] | 0 | não |
| 5 | traseiras empurram | 1/1/0 | 16/16/15 voltando a esticar | 3-25 (23) | [0, 0] | [0, 1] | 1 | não |

Cabeça: o x dela fica sempre o da pose parada (offset x = -dxc) e só o y balança (topo 1, 2, 2, 1, 0, 1). Ela desce com
o peito no pouso das dianteiras e sobe com ele no pouso das traseiras; no frame 0 fica 1 px abaixo do pescoço
("projetada", em linha com as costas). Motivo do x fixo: com a cabeça andando junto com o peito, a variante com contorno
passava do limite de 35% de pixels mudando entre frames (F4->F5 e F5->F0) e a cabeça do cachorro real é a parte mais
estável do galope.

## Pernas (faixas legs_run)

- Estilo: perna de perto `t` com contorno X; de longe `T`, atrás da barriga/peito, com a 1ª linha preta (K): sem
  castanho da perna de longe colado na barriga. A dianteira de perto também nasce preta (o castanho começa abaixo do
  peito, como na pose parada). Diagonal a 45° = faixa de 2 px de tan (`XttX`), vertical = 1 px (`XtX`), 2:1 = degraus
  de 2 px. Nada de diagonal de 1 px (o "arame" com xadrez de X da v1).
- F0 estendido: dianteiras esticadas pra frente em paralelo (de perto até a col. 30, de longe 1 linha abaixo, até a
  29), traseira de perto esticada pra trás até a col. 0, a de longe mais curta; nada toca o chão.
- F1 dianteira pousa: dianteira de perto inclinada pra frente com a pata no chão (sola K na col. 24); a de longe
  chegando no ar; traseiras ainda atrás, começando a dobrar.
- F2 dianteiras empurram: de perto quase reta (recuou 2 px), de longe apoiada atrás (sola K na col. 17); traseiras
  dobradas em "<" (joelho pra frente) vindo por baixo da barriga.
- F3 recolhido: traseiras pra frente por baixo da barriga, dianteira de perto dobrada pra trás com a pata virada, a de
  longe curta à frente; vão aberto entre o grupo de trás e o da frente (sem "cesto").
- F4 traseiras pousam embaixo da barriga (tan da linha 30 nas col. 11 e 13), dianteiras se abrindo pra frente no ar.
- F5 traseiras empurram (col. 9 e 11), dianteiras esticando pra frente.

## Anti-patinação (conferido no render; linha 30 = tan, linha 31 = sola)

A janela anda 2 px do sprite por frame; pata plantada recua exatamente 2 px por frame.

| perna | F0 | F1 | F2 | F3 | F4 | F5 |
|---|---|---|---|---|---|---|
| dianteira de perto | ar | tan 25, sola K 24 + XXX | tan 23, sola K 22 + XXX | ar | ar | ar |
| dianteira de longe | ar | ar | tan 18, sola K 17 + XX | ar | ar | ar |
| traseira de perto | ar | ar | ar | ar | tan 11, sola KK 11-12 | tan 9, sola KK 9-10 |
| traseira de longe | ar | ar | ar | ar | T 13, sola X 13 + K 14 | T 11, sola X 11 + K 12 |

## Rodada 1 (rascunho: blocos + fitas)

Cisalhamento em 3 blocos (garupa/meio/peito) e pernas por polilinha. A inclinação já lia (F1 frente pra baixo, F4 pra
cima), mas o tronco virou um "tijolo em degraus", a cachorra ficava baixa demais nos frames no ar (abaixamento fixo) e as
pernas diagonais de 1 px viraram arame com xadrez de X; o recolhido fechava um cesto. Mudei: cisalhamento interpolado
por pontos de controle, frames no ar mais altos e frente ainda baixa no F2, pernas por runs explícitos (2 px nas
diagonais, 1 px nas verticais).

## Rodada 2 (buracos e leitura das pernas)

`problems()` achou bolsões entre pernas que divergem (a borda X de uma fechava o vão da outra): F0 dianteiras, F1
traseiras, F3 entre traseiras e dianteiras, F4 e F5 dianteiras. Redesenhei: F2 traseiras em "<", F3 com vão aberto entre
os grupos, F1 traseira de longe mais vertical; 1ª linha das pernas de longe e da dianteira de perto em preto. Vãos de
1 px que fecham embaixo viram X (junção escura entre as pernas).

## Rodada 3 (entalhes, lint e contorno)

Entalhes na borda: debaixo da barriga entre as traseiras (F0, F1, F2, F3), junção peito-dianteira (F0, F4, F5), dente
nas costas antes do pescoço (F1, F3) e na nuca (toco do pescoço aparecendo quando a cabeça desce: F0, F5). Todos
fechados. O lint da `run_contorno` deu aviso de >35% de pixels mudando (F4->F5 35%, F5->F0 37%) e o contorno G fechava
um bolsão entre as traseiras no F0. Cabeça com x fixo + F1 sem abaixar a cabeça a mais: máximo 31% com contorno. Traseira
de longe do F0 1 coluna pra frente. F0 com as duas dianteiras em paralelo (antes a de longe era um toco).

## Rodada 4 (2x na taskbar clara + v1 x v2)

Em 2x sobre #f3f3f3: dá pra ver o tronco descendo na frente (F1) e subindo (F4), o corpo comprido no F0 (25 col.) e
curto no F3/F4 (21 col.), e a corcova das costas no F2/F3. Continua a Kiara: cabeça idêntica (orelhões, grisalho, olho
castanho), mancha W do peito e toquinho viajando com o tronco. Perto x longe se distinguem pela cor (t x T) e pela
ordem. Último ajuste: dianteira de longe do F3 era um pixel castanho solto embaixo do peito; virou uma perninha curta.

## Conferência final

- Rig == gerador nos 6 frames.
- Lint: `run` e `run_esquerda` só com "silhueta some na taskbar escura" (esperado, 6 frames cada); `run_contorno`
  "nenhum problema" (0 erros, 0 avisos).
- `problems()`: 0 buracos e 0 pixels soltos em `run`, `run_esquerda` e `run_contorno`. Entalhes que sobraram: o
  embaixo do toquinho (o mesmo da pose parada aprovada, (3,16) lá) e vãos entre pernas, longe da barriga (F1 (6,26),
  F2 (10,28), F4 (22,28)). Nenhum na borda da barriga, do peito ou das costas.
- Pés no chão: linha 31 em todos os frames apoiados (1, 2, 4, 5).

## Pontos pro diretor

- A inclinação é de 2 px (garupa x peito) nos extremos. Dá pra testar 3 px no F1/F4, mas as pernas ficam com 4 linhas
  embaixo da barriga.
- A cabeça não vai pra frente em x (fica no x da pose parada); o "projetada" do F0 é só ela 1 px mais baixa, em linha
  com as costas. Com ela 1 px à frente no F0/F1 o contorno volta a dar aviso de 35-37%.
- Nos frames 3 e 4 o pescoço fica 1 px mais grosso atrás (o toco aparece com borda X ao lado da borda da cabeça);
  em 2x não se vê.
- Mantive 6 frames de 70 ms: o ciclo lê inteiro e cada frame já muda 1 px de inclinação. Com 8 frames os passos de 1 px
  ficariam repetidos (2 frames iguais de inclinação) e a anti-patinação a 2 px/frame pediria pernas mais compridas.
- A dianteira de longe só toca o chão no F2 (como na v1).
