# Correndo / galope v3 (6 frames, tronco inclinando + pernas e toquinho novos) 32x32 - log

## Histórico curto

- **v1 (reprovada)**: `upper` rígido, só as pernas mudavam. Dono: "faltou o tronco inclinar na corrida". Commit 04b1f9d.
- **v2**: um tronco por pose (`torso_run_*`, cisalhamento em degraus), corpo estica (25 col.) e encolhe (21), frente
  desce no pouso das dianteiras e sobe no das traseiras, cabeça só sobe e desce. O dono gostou do tronco. Commit 6f1ae48.
- **v3 (esta)**: pedidos do dono sobre a v2: "as patas da frente tão muito à frente; as patas de trás não tão fiéis a
  toda extensão que um cachorro tem ao correr; parece que as patinhas da frente e de trás quase tocam também" e "o rabo
  do cachorro também acompanha a coluna, né, quando tá correndo". Referências: ciclos de corrida de cão realista, cães
  cartoon e lobo.

## Arquivos

- `torso_run_{estendido,frente_baixa,arqueando,recolhido,frente_alta,esticando}.txt`: mesmos troncos inclinados da v2,
  agora com o toquinho desenhado por pose e no x do quadro (ver "Deslocamento").
- `legs_run0..5.txt`: faixa das linhas 19-31 (fundo do corpo inclinado com borda X + pernas novas).
- `../../anims/run.json`: legs em `at [0,19]`, torso com `offset [0, C]`, `head` em `torso.pescoco` com `offset [1, y]`.
  6 frames de 70 ms (420 ms), `airborne` nos frames 0 e 3, variantes `contorno` (G) e `esquerda` (mirror).
- Fonte editável: os `.txt`. Gerador de apoio fora do repo: `scratchpad/run3/v3.py` + `tails.py` + `export3.py`
  (usa `scratchpad/run2/lib.py`). O render do rig bate pixel a pixel com o gerador.
- Não foram tocados: `upper`, `torso`, `head`, `head_bark*`, `legs_base`, `legs_trotB*`, receitas stand/walk/latir,
  paleta, ferramentas.

Render: `python3 sprites/tools/rig.py sprites/anims/run.json --parts sprites/parts/32 --out <saída> --gif`.

## O que mudou na v3

### Dianteiras (estavam "muito à frente")
Agora vão pra frente e pra baixo em diagonal de 45° (faixa `XttX`), com a pata embaixo da cabeça, no máximo na linha
do focinho. Antes (F0/F4/F5) elas esticavam quase na horizontal e passavam do focinho. As duas dianteiras andam em
paralelo, a de longe 3 colunas atrás e com a 1ª linha preta.

### Traseiras ("toda a extensão")
- F0 (esticado no ar): diagonal longa e reta saindo da garupa, bem pra trás, com a pata no alto atrás do toquinho
  (col. 0); a de longe em paralelo, 4 linhas abaixo.
- F1: ainda esticadas pra trás (45°), juntas (de perto e de longe lado a lado, borda X em comum).
- F5 (empurrão): plantadas em diagonal pra trás, do alto da coxa até a pata atrás do quadril (tan da linha 30 nas
  col. 5 e 7).
- F4 (pouso): embaixo do quadril, com o joelho pra frente (perna dobrada absorvendo o pouso), col. 7 e 9.
- F2: vindo pra frente por baixo da barriga.

### Recolhido (patas se encontram)
F3: traseiras pra frente e dianteiras dobradas pra trás formam um V embaixo da barriga; as patas se encontram no meio e
a traseira de perto passa por baixo/na frente da dianteira de perto (cruzando). As pernas de longe ficam no meio do V
(sem bolsão). No F2 as traseiras já chegam perto das dianteiras.

### Toquinho acompanha a coluna
Mesmo tamanho aprovado (3 px de comprimento, 2 de espessura, preto, borda X do lado de baixo/de trás), só degraus de
pixel. Fica na peça do tronco, então viaja com a garupa no cisalhamento.

| frame | pose | toquinho |
|---|---|---|
| 0 | esticado no ar | pra trás, levemente pra cima (ponta 1 px acima da base) |
| 1 | frente baixa / garupa alta | 45° pra trás e pra cima, inclinado junto com a garupa |
| 2 | arqueando | pra trás, reto (prolonga as costas) |
| 3 | recolhido | pra trás e pra baixo (acompanha a curva) |
| 4 | garupa baixa / frente alta | pra trás e pra baixo (prolonga a linha das costas) |
| 5 | empurrão | pra trás, reto |

### Deslocamento e encaixe (mudou da v2)
- A cachorra inteira está **1 px à direita** da pose parada em todos os frames (cabeça incluída), pra caber o toquinho
  deitado pra trás e as traseiras esticadas até a col. 0. O focinho chega na col. 31.
- O frame 5 andou mais 1 px (garupa na mesma coluna do frame 4): durante o empurrão a garupa não recua, então a perna
  plantada gira 2 px de verdade.
- Peças `torso_run_*` no x do quadro; só o y é normalizado no pescoço (`offset [0, C]`). `@socket.pescoco 20,14` em
  todas (a simulação `sim_page.py` conta com o socket no lugar da pose parada) e a cabeça encaixa com `offset [1, y]`.
  `sim_page.py --run run` confere as camadas com o rig: ok.

| frame | R/M/C (desce) | corpo | toquinho | offset torso | offset cabeça | topo | no ar |
|---|---|---|---|---|---|---|---|
| 0 | 0/0/0 | col. 3-27 (25) | tras_cima | [0, 0] | [1, 1] | 1 | sim |
| 1 | 0/1/2 | col. 3-27 (25) | diag | [0, 2] | [1, 0] | 2 | não |
| 2 | 1/0/2 | col. 4-26 (23) | tras | [0, 2] | [1, 0] | 2 | não |
| 3 | 1/0/1 | col. 5-25 (21) | tras_baixo | [0, 1] | [1, 0] | 1 | sim |
| 4 | 2/1/0 | col. 5-25 (21) | tras_baixo | [0, 0] | [1, 0] | 0 | não |
| 5 | 1/1/0 | col. 5-27 (23) | tras | [0, 0] | [1, 1] | 1 | não |

## Anti-patinação (conferido no render; linha 30 = tan, linha 31 = sola)

A janela anda 2 px do sprite por frame; pata plantada recua exatamente 2 px por frame.

| perna | F0 | F1 | F2 | F3 | F4 | F5 |
|---|---|---|---|---|---|---|
| dianteira de perto | ar | tan 26, sola K 25 + XXX | tan 24, sola K 23 + XXX | ar | ar | ar |
| dianteira de longe | ar | ar | tan 19, sola K 18 + XX | ar | ar | ar |
| traseira de perto | ar | ar | ar | ar | tan 7, sola KK 7-8 | tan 5, sola KK 5-6 |
| traseira de longe | ar | ar | ar | ar | T 9, sola X 9 + K 10 | T 7, sola X 7 + K 8 |

## Rodadas da v3

1. **Pernas novas sobre os troncos da v2.** Dianteiras a 45° com a pata embaixo da cabeça, traseiras esticadas, patas
   se encontrando no F3. Faltava espaço atrás da garupa (col. 2) pra esticar a traseira e deitar o toquinho, então
   desloquei tudo 1 px pra direita. `problems()` achou bolsões no F1 (entre as traseiras) e no F2 (entre a traseira de
   longe e as dianteiras): no F1 juntei as traseiras com borda X em comum e no F2 encurtei a traseira de longe, com o
   vão aberto pra baixo.
2. **Empurrão de verdade.** No F5 a traseira ficava quase reta (pata embaixo do quadril), porque a garupa recuava
   enquanto a pata estava no chão. Passei o F5 1 px pra frente e as patas pra col. 5/7 (pouso em 7/9): a perna sai do
   alto da coxa e vai pra trás. No F0 a traseira começa mais atrás na coxa (antes parecia sair da barriga).
3. **Toquinho por pose** (pedido novo do dono): 5 desenhos (de pé, 45°, pra trás levemente pra cima, pra trás reto, pra
   trás e pra baixo). O "45°" com 1 px de K ficou fino demais e ganhou mais 1 px de K. Fechados os entalhes novos (dente
   da barriga no F2 e no F4, junção peito-dianteira no F4 e no F5, costas antes do pescoço no F3).
4. **Leitura (8x e 2x na taskbar clara, v2 x v3).** No F3 a dianteira de perto era um toquinho dobrado; virou uma
   perna dobrada pra trás que encontra a traseira (opção B de 4 testadas). No F4 a traseira reta parecia uma estaca;
   ganhou o joelho pra frente (opção D). A simulação recusava as camadas com o socket andando, então o socket voltou
   pro 20,14 e a cabeça leva o offset +1.

## Conferência final

- Rig == gerador nos 6 frames; `sim_page.py --run run`: camadas recompõem walk, bark e run.
- Lint: `run` e `run_esquerda` só com "silhueta some na taskbar escura" (esperado, 6 frames cada); `run_contorno`
  "nenhum problema" (0 erros, 0 avisos; maior mudança entre frames com contorno 31%).
- `problems()`: 0 buracos e 0 pixels soltos em `run`, `run_esquerda` e `run_contorno`. Entalhes só entre pernas, longe
  da barriga: F0 (1,27) e (26,30), F5 (26,29). Nenhum em volta do toquinho, na barriga, no peito ou nas costas (o
  entalhe embaixo do toquinho de pé da pose parada sumiu, porque o toquinho agora deita).
- Pernas de longe sem castanho colado na barriga; pés no chão (linha 31) nos frames 1, 2, 4 e 5.

## Pontos pro diretor

- Do F3 (patas da traseira lá na frente, no ar) pro F4 (pouso embaixo do quadril) a traseira volta ~9 px de uma vez.
  É o preço do empurrão comprido no F5 com só 2 frames de apoio. Dá pra pousar mais à frente (col. 9/11 e 7/9), mas a
  perna do empurrão volta a ficar quase reta.
- "Pata atrás e acima do toquinho": a pata esticada do F0 fica atrás do toquinho (col. 0) e no alto (6 linhas acima do
  chão), mas não acima da altura dele (isso desmontaria a perna em 32 px).
- A cachorra ficou 1 px à direita da pose parada e o focinho encosta na borda (col. 31). Na troca parada -> correndo
  ela pula 1 px; se incomodar, dá pra compensar no app.
- O toquinho deitado muda a silhueta da garupa em todos os frames; o de pé (aprovado) segue na pose parada e no trote.
