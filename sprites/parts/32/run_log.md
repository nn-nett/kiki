# Correndo / galope v4 + cabeça de corrida (6 frames) 32x32 - log

## Histórico curto

- **v1 (reprovada)**: `upper` rígido, só as pernas mudavam ("faltou o tronco inclinar"). Commit 04b1f9d.
- **v2**: um tronco por pose, inclinando por degraus; corpo de 21 a 25 col. O dono gostou do tronco. Commit 6f1ae48.
- **v3**: dianteiras a 45° sem passar do focinho, traseiras esticando pra trás, patas se encontrando no recolhido,
  toquinho por pose seguindo a coluna, cachorra 1 px à direita. Depois o diretor arredondou o bumbum do último frame
  (pedido do dono: "a bundinha expandia"). Commits fdbfd89 e 171b643.
- **v4 (esta)**: guiada pela referência de pixel art que o dono mandou ("se liga nessa ref"; cachorro 45x45, 6 poses,
  em `sprites/extern/refs_correr/`, só estudada, nenhum pixel copiado). O que faltava: o corpo esticar e encolher
  muito mais (bola de costas arqueadas no recolhido, comprido, baixo e reto no esticado), pernas curtas trabalhando
  embaixo do corpo, cabeça e rabo acompanhando.
- **Cabeça de corrida (rodada atual)**: o dono está "entre a v3 e a v4" e pediu: "na corrida o cachorro deixa o
  focinho esticado à frente, as orelhas meio que vão pra trás, e a cabeça desce pra ficar um pouco mais alinhada com o
  corpo". Referência: cão em desenho 2D, 7 frames (`refs_correr/cao_desenho_*`), só estudada. Aplicada em duas bases
  pro dono escolher: **v4 + cabeça** (`anims/run.json`, no repo) e **v3 + cabeça** (`anims/run_v3c.json`).

## Cabeça de corrida (`head_run.txt`), versão 2

**Por que refiz.** Na primeira versão o dono reclamou: "acho que você mudou o tamanho do focinho; além disso ela tá
parecendo que tem nanismo, kk. Cadê o pescoço?". Os problemas eram três:
- o focinho tinha 1 col. a mais;
- o crânio tinha 1 linha a menos em cima;
- a cabeça descia 7 px e encostava direto nas costas, sem o toco do pescoço, cobrindo o peito.

**A peça agora.** `head_run.txt`, 21x13, `@anchor 9,12`, `@role cabeca`. `head.txt` e `head_bark*` não mudaram.
- Crânio e rosto copiados **pixel a pixel** das linhas 5-14 da `head.txt`: o mesmo focinho (grisalho G/W, nariz, boca,
  queixo), o mesmo olho com brilho B, a mesma sobrancelha, bochecha e garganta. Mesma altura (10 linhas) e mesma
  largura sem as orelhas. A âncora é a mesma (4,14) deslocada junto: com offset [0,0] o rosto cai exatamente onde
  fica na pose parada.
- Só as orelhas mudam: deitadas pra trás a ~35°, grandes.
  - A de trás é um triângulo com o castanho dentro e borda X dos dois lados.
  - A da frente fica escura (com um pixel D) por cima do crânio.
  - Tirei dois pixels da base das orelhas em pé: o tan da linha 5 e o X da linha 6 viraram K, porque eram o pé das
    orelhas antigas.
- Comparação em `scratchpad/run6/cabecas.png` (14x, alinhadas pelo olho): a ponta do focinho (vermelho), o alto do
  crânio (azul) e o queixo (verde) da nova batem com a original. A anterior passava 1 px do focinho.

**Posição.**
- A cabeça desce só 3 px em relação à pose parada (antes eram 7). Fica 1 col. à frente, com o focinho na col. 31.
- Offsets da cabeça:
  - v4: [1,3] em todos os frames;
  - v3c: [1,3], [1,2], [1,2], [1,2], [1,3], [1,3].
- O alto do crânio fica nas linhas 9-10-10-9-8-9 (v4) e 8-9-9-8-8-8 (v3c): no máximo 1 px por frame.
- Com isso a mancha clara do peito volta a aparecer embaixo do queixo, com a garganta tan descendo do queixo pro peito.

**Pescoço.**
- O toco do pescoço voltou para os `torso_run_*` das duas versões.
- Ganhou uma cunha preta da cernelha até a nuca, numa rampa de 2:3 (1,5 col. por linha), desenhada no tronco: a linha
  das costas sobe dos ombros até a cabeça e as orelhas deitam por cima dela.
- Os X do toco que ficaram por dentro do pescoço viraram K.
- Os entalhes de 1 px na junção orelha/pescoço foram fechados com K.

**Corpo.** Não deslizei o corpo pra trás. Na v4 (F0 e F1) e na v3, a garupa está na col. 3 e o toquinho de 3 px já
encosta na col. 0: 1-2 px pra trás cortariam o rabo. Como a cabeça desce menos, o pescoço aparece sem isso.

**Receita.** `"part": "head_run"`; torso `offset [0, C]`; a cabeça encaixa em `torso.pescoco` com os offsets acima.
`sim_page.py --run run` confere: "camadas recompõem walk, bark, run".

### v3 + cabeça (`run_v3c`)
- Peças da v3 (commit 171b643, com o bumbum arredondado) em `sprites/candidates/correndo_v3c/parts/`: os
  `torso_run_*` com o pescoço novo e os `legs_run*` sem mudança.
- Receita no repo: `anims/run_v3c.json`, com os mesmos nomes de peça da v4. Ela só vale com uma pasta de peças =
  `parts/32` + `candidates/correndo_v3c/parts` por cima (montada em `scratchpad/run6/parts_v3c/`).

### Conferência (as duas versões)
- Rig == gerador nos 6 frames das duas. Faixas de pernas idênticas às de antes (conferido).
- Lint: normal e esquerda só com "silhueta some na taskbar escura"; contorno "nenhum problema" nas duas.
- `problems()`: 0 buracos e 0 pixels soltos nas três variantes das duas. Entalhes só entre as patas:
  - v4: F0 (24,30);
  - v3c: F0 (1,27) e (26,30), F5 (26,29).
- Maior mudança entre frames com contorno: 31% (v4 e v3c).

## Arquivos

- `torso_run_{estendido,frente_baixa,arqueando,recolhido,frente_alta,esticando}.txt` (reescritos): o tronco de cada
  pose, com o toquinho. x do quadro, y normalizado no pescoço; `@socket.pescoco 20,14` em todos.
- `legs_run0..5.txt` (reescritos): linhas 19-31, fundo do corpo + pernas curtas.
- `../../anims/run.json` (reescrita): legs `at [0,19]`, torso `offset [0, C]`, cabeça (`head_run` desde a rodada da
  cabeça de corrida) em `torso.pescoco` com offset próprio por frame. 6 frames de 70 ms (420 ms), `airborne` nos frames 0 e 3, variantes `contorno` e `esquerda`.
- Gerador de apoio fora do repo: `scratchpad/run4/v4.py` + `export4.py` (usa `run2/lib.py` e os toquinhos de
  `run3/tails.py`). O render do rig bate pixel a pixel com o gerador. Fonte editável: os `.txt`.
- Não foram tocados: `upper`, `torso`, `head`, `head_bark*`, `legs_base`, `legs_trotB*`, receitas stand/walk/latir,
  paleta, ferramentas.

## Como o corpo muda de forma (sem rotação)

Molde = `torso.txt` + fundo de barril (barriga reta com X embaixo) + toquinho da pose. Por frame:
1. **Comprimento**: tira ou repete colunas do meio (só barriga e dorso), até ±5 colunas.
2. **Inclinação**: cada coluna desce `dy`, interpolado entre garupa (R), meio (M) e peito (C).
3. **Arco**: no compacto e na bola, as costas ganham um bojo (1 px a mais só na linha de cima, com o pico no lombo).
   Assim o corpo fica mais alto no meio, como a bola da referência. A barriga continua reta.
4. **Bumbum arredondado** em todos os frames: o canto de baixo/atrás da garupa é aparado no padrão que o diretor usou
   no `legs_run5` da v3 (3 px na coluna de trás e 2 na seguinte). Nenhum frame desce reto da garupa até a pata.
5. Posição: garupa na col. Rx, peito na col. Cx. A cabeça vai pelo topo (linha) e pelo focinho (col.), independente
   do pescoço; o toco do pescoço tapa o vão.

| frame | pose (ref.) | garupa-peito | comprimento | R/M/C | bojo | cabeça topo / focinho | toquinho | no ar |
|---|---|---|---|---|---|---|---|---|
| 0 | esticado no ar | 3-26 | 24 | 1/1/1 | 0 | 1 / 31 | pra trás, levemente pra cima | sim |
| 1 | dianteira pousa | 3-26 | 24 | 0/1/2 | 0 | 3 / 31 | 45° pra cima (garupa alta) | não |
| 2 | compacto (dianteiras empurram) | 5-26 | 22 | 1/0/2 | 1 | 4 / 31 | pra trás | não |
| 3 | bola (recolhido) | 6-24 | 19 | 2/-1/1 | 1 | 3 / 30 | pra trás e pra baixo | sim |
| 4 | traseiras pousam | 4-24 | 21 | 2/1/0 | 0 | 2 / 30 | pra trás e pra baixo | não |
| 5 | empurrão (comprido e baixo) | 4-26 | 23 | 2/2/1 | 0 | 1 / 31 | pra trás | não |

- Comprimento: 19 na bola e 24 no esticado (v3: 21 a 25).
- Bola: costas ~4 px mais altas no meio do que na garupa.
- Cabeça: mais alta no esticado e no empurrão (topo 1), mais baixa no compacto (4), na bola (3) e no pouso (3). Na
  bola e no pouso das traseiras ela fica 1 px mais à frente do peito.
- Receita: torso `offset [0, C]`; cabeça `offset [focinho - 30, topo - C]`, ou seja [1,0], [1,1], [1,2], [0,2],
  [0,2] e [1,0].
- Orelhas nunca passam da linha 0. Toquinho encosta na col. 0 no frame 0, focinho na col. 31.

Por que não chegou a 26-27 no esticado: o focinho já está na col. 31 e o peito não pode passar de ~5 col. atrás dele.
Com o peito na col. 28 testado, ele fica saltado embaixo da cabeça, porque a cabeça não pode ir mais pra frente. Atrás,
o toquinho de 3 px precisa das col. 0-2, então a garupa não sai da col. 3.

## Pernas (curtas, embaixo do corpo)

- Mesmas regras da v3: perna de perto `t` com borda X; de longe `T`, atrás, com a 1ª linha preta e sem castanho colado
  na barriga; diagonal a 45° em faixa de 2 px; nada de diagonal de 1 px.
- F0: dianteiras a 45°, patas embaixo do focinho; traseiras pra trás quase rente, a de longe colada embaixo da de perto.
- F1: dianteira de perto pousa à frente do peito, a de longe chegando; traseiras ainda pra trás.
- F2: dianteira de perto quase reta e a de longe apoiada atrás; traseiras dobrando pra frente embaixo da barriga.
- F3: bola. Traseiras pra frente e dianteiras dobradas pra trás; as patas quase se tocam embaixo do meio da barriga.
- F4: traseiras pousam embaixo do quadril, joelho pra frente; dianteiras a 45°.
- F5: traseiras empurram em diagonal pra trás saindo da coxa (o bumbum faz a curva antes); dianteiras a 45°.

## Anti-patinação (conferido no render; linha 30 = tan, linha 31 = sola)

A janela anda 2 px do sprite por frame; pata plantada recua exatamente 2 px por frame.

| perna | F0 | F1 | F2 | F3 | F4 | F5 |
|---|---|---|---|---|---|---|
| dianteira de perto | ar | tan 25, sola K 24 + XXX | tan 23, sola K 22 + XXX | ar | ar | ar |
| dianteira de longe | ar | ar | tan 18, sola K 17 + XX | ar | ar | ar |
| traseira de perto | ar | ar | ar | ar | tan 7, sola KK 7-8 | tan 5, sola KK 5-6 |
| traseira de longe | ar | ar | ar | ar | T 9, sola X 9 + K 10 | T 7, sola X 7 + K 8 |

O peito fica na mesma coluna no apoio das dianteiras (F1->F2) e a garupa na mesma coluna no das traseiras
(F4->F5): a perna plantada gira 2 px de verdade. O corpo dá o "bote" no empurrão (peito +2 col.).

## Rodadas da v4

1. **Forma do corpo.** Montei o gerador novo (comprimento por colunas do meio, inclinação, bojo nas costas,
   bumbum arredondado) e testei comprimentos 26-28 no esticado. Com o peito além da col. 26 ele salta embaixo da
   cabeça (o focinho já está na col. 31), então o esticado ficou em 24. A primeira bola, com inclinação forte
   (meio 3 px acima), fez a barriga em escada e um "esporão" na garupa. Troquei por inclinação leve + bojo só nas costas.
2. **Pernas curtas e lint.** Pernas novas embaixo do corpo. O contorno passou de 35% de pixels mudando de F3->F4
   (38%) e F4->F5 (40%), porque cabeça e peito mexiam muito de uma vez. Suavizei a cabeça (topo 1-3-4-3-2-1, focinho
   31-31-31-30-30-31), deixei o empurrão com o peito 1 px mais alto e o pouso das traseiras com o peito 1 col. à
   frente. Máximo com contorno: 32,6%.
3. **Entalhes e bolsões.** Fechados: rump/coxa (F0), costas antes do pescoço (F1, F2, F3), nuca onde o toco do pescoço
   aparece com a cabeça baixa (F1: tirei o pixel; F3 e F4: preenchi), junção peito-dianteira (F2, F3, F4), degrau
   da barriga (F4) e a cunha entre traseira de longe e dianteira de longe no F2 (traseira de longe reta, sem bolsão
   no contorno). Traseira de perto do F5 começa mais à frente na coxa, pra o bumbum fazer a curva antes da perna.
4. **Leitura (8x, 2x na taskbar clara, v3 x v4 e lado a lado com a referência).** A bola ficou "corcunda" com o pico
   muito atrás; com a garupa mais baixa (R 2) e o meio 1 px acima, as costas viram um arco do toquinho ao pescoço.
   O F0 tinha castanho da perna de longe colado na barriga (a perna começava na linha da barriga); desci as duas
   pernas de longe 1 linha. No F3 também tirei um
   pixel que sobrava embaixo da garupa.

## Conferência final

- Rig == gerador nos 6 frames. `sim_page.py --run run`: "camadas conferidas: recompõem walk, bark, run pixel a pixel".
- Lint: `run` e `run_esquerda` só com "silhueta some na taskbar escura" (esperado, 6 frames cada); `run_contorno`
  "nenhum problema" (0 erros, 0 avisos).
- `problems()`: 0 buracos e 0 pixels soltos em `run`, `run_esquerda` e `run_contorno`. Único entalhe: F0 (24,30),
  entre as patas das dianteiras. Nenhum na barriga, no peito, nas costas, na garupa ou em volta do toquinho.
- Pernas de longe sem castanho colado na barriga (conferido por script); bordas de baixo em X; pés no chão (linha 31)
  nos frames 1, 2, 4 e 5.

## Pontos pro diretor

- Esticado em 24 col. (alvo 26-27): limite do quadro com a cabeça na col. 31. Pra ganhar mais, só deixando o peito
  saltar embaixo da cabeça ou cortando o toquinho na borda.
- 6 frames mantidos: a referência usa 6 poses e o ciclo lê; com 8, as mudanças de forma por frame ficariam menores.
- A cabeça agora sobe e desce 3 px no ciclo (v3: 2). O pescoço engrossa 1 px atrás na bola e no pouso das traseiras
  (a cabeça fica 1 px à frente do toco); em 2x não aparece.
