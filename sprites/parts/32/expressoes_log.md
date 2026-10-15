# Expressões desacopladas (piscar, ofegante): log

Ideia do dono: "aproveitar o dormindo pra ter animação de piscar, e deixar isso desacoplado do resto [...]
aproveitar o latir pra fazer a animação com aquela linguinha pra fora, fazendo aquela respiração
característica de cachorro". Versão SEM contorno (o contorno sai pelo filtro, variante `contorno`).

## Arquivos

- `olho_meio.txt` e `olho_fechado.txt`: remendos do olho (camada pequena por cima de qualquer cabeça).
- `@socket.olho` (só comentário) em `head.txt`, `head_bark1.txt`, `head_bark2.txt` (7,9) e `head_run.txt` (12,7).
- `../../anims/piscar.json`: pose parada (stand_head) + remendo em `head.olho`.
- `head_ofegante1.txt` (inspira) e `head_ofegante2.txt` (expira): mesmo `@anchor 4,14`, com `@socket.olho`
  e `@socket.boca`.
- `../../anims/ofegante.json` (pose parada) e `../../anims/andar_ofegante.json` (trote B + torso + cabeça
  ofegante, só receita).
- Nenhum pixel de peça existente mudou. Não mexi em `run*`, `torso_run*`, legs, torso, paleta nem ferramentas.

## 1. Piscar

**Encaixe.** O socket fica no canto de cima do olho castanho (o pixel E de cima): (7,9) nas cabeças em pé
e do latido, que é o ponto (23,9) do quadro; (12,7) na `head_run`, que é o mesmo pixel E (a cabeça de
corrida tem o rosto copiado da `head.txt`, com a âncora deslocada). Os remendos têm `@anchor 1,0` e cobrem
as colunas 22-25, linhas 9-11 (na pose parada). Onde o remendo tem `.`, fica o pixel da cabeça.

**Remendos** (olho aberto = `G E B X / G E e X / t D K G`):
- `olho_meio`: a pálpebra grisalha G desce sobre a linha de cima do olho (tapa o E e o brilho B);
  a linha de baixo (E e) continua. Só 2 px.
- `olho_fechado`: igual ao olho de dormir do `dormir_A/B` (pálpebra G de 3 px, linha escura X embaixo
  com a ponta da frente subindo 1 px, e o D da bochecha vira t, o K vira G, porque o D sozinho sob a
  linha parecia íris aberta).

**Receita** `piscar.json`: aberto 1500 ms, meio 60, fechado 110, meio 60 (loop). Variantes contorno/esquerda.

**Prova de que as cabeças não mudaram** (o socket é só comentário): renderizei `stand`, `stand_head`,
`latir_tranco` e `run` (com as variantes) antes e depois de pôr a linha: 34 PNGs comparados pixel a pixel,
0 diferenças. As matrizes das 4 peças (`parse_matrix`) são idênticas; a única tag nova é `socket.olho`.

**Sem desenho novo por pose** (`piscar_quadro.png`): os mesmos 2 remendos encaixados em `head.olho`
funcionam por cima de:
- parada (`head`);
- andando: receita do trote B com `torso` + `head` (a migração do `upper` dá 0 pixels diferentes do
  `walk_b` original) — o remendo acompanha o tronco subindo/descendo;
- correndo (`head_run`, com os offsets da corrida);
- latindo (`head_bark1`/`head_bark2`, com o tranco);
- ofegante (`head_ofegante1/2`).
Em todos: 0 buracos, 0 pixels soltos, 0 entalhes novos.

## 2. Ofegante

**Cabeça** (igual à `head.txt` até a linha 12: orelhas, olho com brilho, sobrancelha, focinho, nariz):
- boca entreaberta como no `head_bark1` (menos que no AU!): mandíbula 1 px abaixo, fresta escura N
  (cols 27-29) e lábio de baixo K;
- queixo GGG de 1 linha, do mesmo tamanho do original (só desce 1 px, como no head_bark1 aprovado);
- língua rosa P sai por cima do lábio de baixo (linha 14, col. 28) e fica pendurada na frente do queixo,
  com 2 px de largura (cols 29-30) e ponta de 1 px virada pra trás;
- `head_ofegante1` (inspira): ponta 2 px abaixo do queixo; `head_ofegante2` (expira): a língua desce
  1 px (3 px abaixo do queixo);
- a cabeça não cresce pra frente nem pra cima: largura e topo iguais à `head.txt`. O que passa do queixo é só
  a língua. O rosa aparece só na língua.

**Receita** `ofegante.json` (130 ms por frame, loop de 2: ~3,8 respirações por segundo):
- f0 inspira: `head_ofegante1`, torso [0,0];
- f1 expira: `head_ofegante2`, torso [0,1] (o peito/costas descem 1 px) e cabeça com offset [0,-1]
  (a cabeça fica parada; só a língua e o corpo mexem).
Variantes contorno/esquerda.

**Andando ofegante** (`andar_ofegante.json`, só receita): pernas do trote B + `torso` (com os offsets do
walk_b) + `head_ofegante1`, trocando pra `head_ofegante2` nos frames em que o corpo desce (1 e 4).
Assim a língua balança com a passada. Nenhum desenho novo.

## Conferência

- `lint.py --size 32 32`: piscar, ofegante e andar_ofegante (normal e esquerda) só acusam "silhueta some
  na taskbar escura" (esperado sem contorno); as três `_contorno` passam limpas.
- `tweak.problems()`: 0 buracos e 0 pixels soltos em todos os frames (normal e esquerda). Entalhes novos
  (comparados com o mesmo frame com a cabeça normal):
  - piscar: nenhum;
  - ofegante/andar_ofegante: só o vão da boca aberta na frente, entre o nariz e a língua, (30,13)/(30,14).
    É o mesmo recurso do "AU!" aprovado e é o que faz ler "boca aberta";
  - nas `_contorno`: o mesmo vão (31,13) e um vão de 1 px entre o contorno da língua e o do peito (27,17).
    Os buracos das `_contorno` (entre as patas) já existem iguais na pose parada/trote com contorno.
- Olhar ampliado: `ofegante_quadro.png` (8x, cabeça 14x, 2x/1x clara e escura, ao lado da foto
  `kiki_deitada_lingua.jpg`) e `piscar_quadro.png`.

## Rodadas

Piscar:
1. 6 olhos lado a lado (20x + 2x/3x): meio com pálpebra G (escolhido), pálpebra K (parecia o olho
   descendo), G + brilho na linha de baixo (parecia olhar pra baixo); fechado = olho de dormir (escolhido)
   e sem mexer na bochecha (o D sob a linha virava íris aberta, confirma a decisão do dormir).
2. Remendo aplicado nas 4 cabeças (parada, trote, corrida, latido) em todos os frames: encaixa sem desenho
   novo e sem buraco/entalhe.
3. Também por cima da ofegante: o meio-fechado + língua dá uma "carinha relaxada" (fica a ideia).

Ofegante:
1. Primeiros rascunhos (língua saindo reto pra frente, 1 a 2 px de largura): já liam "língua pra fora".
2. Sem baixar a mandíbula (O6) lia como "blep"/lambida; com a mandíbula 1 px abaixo (O7) lia como ofegante.
   No "inspira" com a língua subindo até o nariz, ela grudava no nariz e sumia a boca aberta; passei a
   mexer só o comprimento (ponta 1 px).
3. Comprimento: 1-2 px abaixo do queixo ficava tímido; 2-3 px (pedido) lê melhor a 2x. Ponta virada pra
   trás (pendurada) em vez de pra frente.
4. Respiração: tronco 1 px pra cima com a cabeça parada (inflar) abria um entalhe na nuca (18,9);
   tronco + cabeça descendo juntos sacudia a cabeça toda; só a língua ficava parado demais. Escolhido:
   tronco desce 1 px na expiração com a cabeça parada (sem entalhe; o detalhe da coxa na linha 21 some
   por 130 ms, coberto pela barriga).
5. Forma da língua: saindo por cima do lábio (escolhida) lê como língua que vem da boca; língua cobrindo
   o lábio todo virava faixa rosa; "colher" (mais larga embaixo) parecia uma botinha; borda X na língua
   comia 1 px do queixo.

## Dúvidas

- Na expiração o tronco desce 1 px e cobre por 130 ms o risco da coxa (linha 21). Se incomodar, dá pra
  tirar o movimento do peito (fica só a língua) ou fazer uma faixa de pernas própria.
- A língua é um bloco de 2 px de largura em P puro; a foto mostra uma língua mais larga e arroxeada.
  Um rosa mais escuro pra sombra da língua seria cor nova (só se o dono pedir).
- O ritmo de 130 ms em 2 frames é ofegante "de calor". Mais calmo: 180-200 ms.
- Combinações possíveis sem desenho novo: ofegante + `olho_meio` (cara relaxada/feliz), piscar durante
  o andar ou a corrida (no app, sorteando o remendo por cima de qualquer animação).

## Ajuste do dono (15/10)

- Piscar: "tem um pixel preto a mais à esquerda, tá indo além do olho" → `olho_fechado` linha do meio
  `XXXK` → `.XXK` (o pixel (22,10) volta a ser o G da cabeça; a linha escura fica só nas colunas 23-24).
- Ofegante: "senti falta do queixo dela descer" e "a língua tá pontuda, parecendo de cobra":
  - `head_ofegante1` (inspira): igual, sem o pixel da ponta da língua (29,17) → ponta reta de 2 px.
  - `head_ofegante2` (expira): mandíbula 2 px abaixo (fresta N nas linhas 13-14, lábio K e língua na 15,
    queixo GGG na 16) e a língua desce junto, também com a ponta reta de 2 px.
  - Opções B (ponta de 3 px) e C (língua curta) em `sprites/candidates/ofegante/`.
- Conferência: 0 buracos, 0 pixels soltos, 0 entalhes novos; lint só com "silhueta some na taskbar escura"
  nas versões sem contorno; `sim_page.py` recompõe piscar/ofegante/andar ofegante pixel a pixel.
- Spritemap e quadro em `sprites/previews/expressoes/`.

## Revisão do ofegante (15/10, depois de aprovado)

Dono: "ofegante, acho que tem coisa estranha aí: o movimento é mais no peito/torso/queixo, o resto não mexe tanto;
andando ofegante tá estranho também". O que estava errado: na expiração o tronco inteiro descia 1 px (costas, rabo,
garupa), e a linha da coxa piscava porque o tronco descido cobria a faixa das pernas.
- Parada: costas, rabo e pernas parados. Inspira = `legs_base_inspA` (barriga e fundo do peito 1 px mais fundos)
  ou `legs_base_inspB` (igual + a frente do peito 1 px pra fora nas linhas 21-22), com `head_ofegante1`;
  expira = `legs_base` normal com `head_ofegante2` (queixo desce mais). Receitas `anims/ofegante_A.json` e
  `ofegante_B.json`.
- Andando: `anims/andar_ofegante_W1.json` (cabeça ofegante 1 fixa: a língua só balança com o passo) e
  `andar_ofegante_W2.json` (alterna 1/2 a cada frame). Antes a boca abria só nos 2 frames em que o corpo desce, e a
  língua pulava 2 px de uma vez.
- Os finais (`sprites/final/`) seguem com a versão aprovada antes até o dono escolher; depois troca
  `ofegante.json`/`andar_ofegante.json` pela escolhida e roda o `export_final.py`.
- Quadros em `sprites/previews/expressoes/quadro_ofegante_peito.png` e `quadro_andar_ofegante.png`; spritemap em
  `spritemap_ofegante.png`.

### Segunda rodada (15/10)

Dono: "andando tá bom, faltou só a animação da boca descendo; a boca aberta tá com um pixel preto no queixo estranho;
a parada A tá boa, acho que vale expandir esses pixels à direita, os da quina, deixando o peito dela mais quadrado;
vamos derivar da parada A".
- Queixo: o lábio de baixo K virou G em `head_ofegante1` (27,14) e `head_ofegante2` (27,15). Vale pra todas as
  receitas que usam essas cabeças (inclusive as aprovadas antes, no próximo export).
- Parada **A2** (`anims/ofegante_A2.json`): inspira = `legs_base_inspA2` (a A + frente do peito reta na coluna 25,
  linhas 20-22, e quina de baixo em (24,23)) + `torso_insp` (o torso com a quina da linha 20 1 px pra frente,
  porque o torso cobre a linha 20); expira = `legs_base` + `torso` normais.
- Andando **W3** (`anims/andar_ofegante_W3.json`): cabeça ofegante 2 (boca mais aberta) nos frames 2 e 5, fora dos
  frames 1 e 4 em que o corpo desce: a língua mexe no máximo 1 px por frame.
- Conferência: 0 buracos, 0 pixels soltos; lint só com "silhueta some na taskbar escura" sem contorno.

### Terceira rodada (15/10)

Dono: "parada: só a barriga não expandir, entre as duas patas do meio pra trás, porque ela respira mais pelo peito;
quero ver com antes e depois" e "andando: você tá sincronizando a ofegação com o ritmo da andada; mantém o ritmo da
respiração na cabeça e o ritmo do andar, coisas diferentes".
- Parada **A3** (`anims/ofegante_A3.json`): inspira = `legs_base_inspA3` (só o peito: fundo do peito entre as patas
  da frente 1 px mais fundo e frente quadrada; a barriga fica igual à `legs_base`) + `torso_insp`.
- Andando com **relógios separados**: o corpo é o trote (100 ms por frame, `andar_ofegante_W1` = trote com a cabeça
  ofegante) e a cabeça troca no ritmo do `ofegante_A3` (130 ms). Não existe como receita única: no app são duas
  animações tocando juntas (corpo + cabeça). Pra prévia, `tools/dois_relogios.py` monta a linha do tempo inteira
  (7,8 s até os dois ciclos baterem juntos, 132 trocas de 12 combinações), com o passo só quando o corpo troca de
  frame. `page.py` aceita "step" por frame e o spritemap mostra as 12 combinações.
- Quando aprovar: export em camadas pro app (corpo andando + cabeça ofegante por cima, cada um no seu relógio) e a
  simulação com o mesmo esquema (o piscar já funciona assim).

### Quarta rodada (15/10)

- Andando com relógios separados **aprovado** ("andando tá ok, perfeito"). Export: a boca ofegante virou remendo
  (`final/expressoes/boca_ofegante1/2`, recorte 5x5 das cabeças ofegantes na área que muda; `_contorno` 7x7 com o
  contorno da língua) e cada frame ganhou `boca` (canto da cabeça + recorte; `null` quando a boca já mexe:
  latindo, ofegante). `andando_ofegante` em `aprovadas.json` virou `composicao` (corpo `andando` + expressão
  `ofegante`). Conferido no export: andando + remendo = trote com a cabeça ofegante do rig, 4 versões, 2 bocas.
- Parada: o dono pediu "um meio-termo entre esses dois" (A2 e A3) e ver os três: `ofegante_M`
  (`legs_base_inspM`: peito como na A3 e só as colunas 14-16 da barriga descem 1 px).
