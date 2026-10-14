# Dormindo (32x32), 1 frame pra validar: log

Pedido do dono: "faz um frame da Kiki deitada dormindo e vamos validar esse frame". É **um frame
parado**; a respiração (2-3 frames) só vem depois, se ele aprovar. Versão **sem contorno** (o contorno
G sai pelo filtro, variante `contorno`).

## Arquivos

- `dormir_A.txt`: opção A, **deitada de barriga, esticadinha**. Peça inteira 32x32, `@anchor 0,0`, `@role corpo`.
- `dormir_B.txt`: opção B, **enrolada** (como na foto `kiki_dormindo_enrolada.jpg`). Mesmo formato.
- Receitas `../../anims/dormir_A.json` e `dormir_B.json`: 1 frame, peça em `at [0,0]`, 1000 ms, loop,
  variantes `contorno` (outline G) e `esquerda` (mirror), como em `walk_b.json`.
- Não mexi em nenhuma peça ou receita existente, na paleta nem nas ferramentas.

## Referências usadas

- `reference/kiki_dormindo_enrolada.jpg` (espelhada pra olhar pra direita): cabeça deitada no chão, olhos
  fechados (fresta escura no meio do grisalho), orelha de longe em pé, orelha de perto tombada pra trás, corpo
  arredondado atrás da cabeça e risco tan na parte de trás da coxa dobrada.
- `reference/kiki_deitada_lingua.jpg`: patas da frente esticadas pra frente (tan), traseira dobrada.
- `sprites/base/kiara_32.txt` / `parts/32/head.txt`: a cabeça é a mesma, linhas 5-14 do `head.txt`
  (crânio, focinho W, nariz, bochecha tan, sobrancelha G, queixo G). Mudou só o olho e as orelhas.

## Decisões

- **Mesma cabeça da aprovada**, sem rotação: o focinho fica na horizontal como na pose em pé (A apoiada nas
  patas, B direto no chão). Assim fica claro que é a mesma cachorra.
- **Olho fechado**: no lugar do olho castanho E + brilho B ficou a pálpebra grisalha G (3 px) com uma
  linha escura X embaixo (3 px, a ponta da frente sobe 1 px, que dá um leve "sorriso" ‿). O D (tan escuro)
  logo abaixo do olho virou t e o K ao lado virou G: o D, sozinho debaixo da linha, parecia uma íris
  aberta. Testei 12 variantes de olho (grisalho em cima/linha embaixo, linha G clara sob pálpebra preta,
  linha `e` etc.); essa foi a que leu "olho fechado" mais claro a 2x e 3x e mantém o grisalho ao redor do olho.
- **Orelhas relaxadas**: as duas tombam pra trás. A de perto mantém o tamanho (8 linhas, miolo tan) e inclina
  ~45° (1 px pra trás por linha); a de longe tem 6 linhas, a base no mesmo lugar da pose em pé e a ponta
  2 px pra trás. São as mesmas peças nas duas opções. Borda X dos dois lados.
- **A (esticadinha)**: corpo longo e baixo (colunas 1-20, linhas 20-31) com a anca um pouco mais alta
  (perna de trás dobrada), toquinho em pé na traseira (3 px, igual ao aprovado), coxa marcada por um risco
  tan (borda da frente da coxa, como o tan da perna de trás na pose em pé) e canela/pata de trás no chão
  pra frente. Pata da frente esticada pra frente (linha tan com borda X em cima e embaixo, pata 2 px na
  ponta) e o queixo apoiado nela; o queixo ganhou 1 px G na frente pra fechar o vão entre a boca e a pata.
- **B (enrolada)**: corpo em bola (meia elipse, colunas 1-20, topo na linha 18), mais alto que a cabeça,
  que fica deitada no chão na frente. Sem pata da frente esticada: só a patinha encolhida debaixo do
  focinho (o focinho encosta nela). Coxa dobrada marcada pelo risco tan em "(" atrás, 1 px pra dentro da
  borda (como na foto), e a pata de trás no chão. Sem toquinho (enrolada, fica escondido); dá pra pôr se
  o dono quiser.
- Bordas de baixo em X (a linha 31 inteira), pernas de longe escondidas atrás do corpo, sem cor nova.

## Rodadas (rascunhos no scratchpad da sessão)

- **A1**: primeira montagem (cabeça da aprovada abaixada sobre a pata). Lia como deitada, mas a orelha de
  perto encolheu (5 linhas), o corpo era um retângulo e o tan de baixo virava uma faixa.
- **A2-A3**: orelha de perto de volta ao tamanho (8 linhas) inclinada 45°; anca arredondada; risco tan da
  coxa (A3). Olhei os olhos ampliados: o D sob o olho parecia íris aberta.
- **Olhos (E1-E6, F1-F6)**: quadro só dos olhos a 20x + 2x/3x; escolhida a F3 (acima).
- **A6-A8**: costas sem degrau, pata da frente com ponta, orelha de longe com a base alinhada (tirou um
  entalhe entre a orelha e o crânio), queixo fechando o vão sobre a pata. A8 = `dormir_A.txt`.
- **B1-B3**: monte + cabeça no chão com a orelha de perto deitada por cima do corpo: a orelha virava uma
  faixa tan (lia como alça/coleira) e o corpo ficava quadrado.
- **B4-B8**: corpo por elipse (redondo), orelha deitada em triângulo; B8b lia bem a orelha, mas a silhueta
  ficava igual à A sem as patas.
- **B9**: teste de "anel" (traseira enrolada na frente do focinho, toquinho do lado direito). Ficou confuso
  a 2x (descartado, mas é uma ideia se o dono quiser "focinho na traseira" literal).
- **B10-B14**: corpo mais alto e redondo + orelha de perto a 45° saindo por cima do corpo: a 2x passou a
  ler "bolinha com cabeça e orelhonas". Testei a bola mais baixa (B14/B14b): parece só deitada, então ficou
  a mais alta. B13 = `dormir_B.txt`.
- Autocrítica final (quadro a 10x + 2x nas duas taskbars, ao lado das fotos e da aprovada): as duas leem
  como cachorra deitada dormindo na taskbar clara a 2x; orelhonas, grisalho no focinho e tan aparecem;
  A e B têm silhuetas diferentes (comprida e baixa / bola).

## Conferência

- Render: `rig.py sprites/anims/dormir_{A,B}.json --parts sprites/parts/32` (normal, contorno, esquerda).
- `lint.py --size 32 32`: normal e esquerda só com "silhueta some na taskbar escura" (esperado sem
  contorno); `dormir_A_contorno` e `dormir_B_contorno` limpos (borda visível no escuro 69% / 66%).
- `tweak.problems()`: normal e esquerda com 0 buracos, 0 pixels soltos e 0 entalhes. Nas `_contorno` o
  filtro fecha 1 pixel entre as orelhas (A: 22,17; B: 18,19), o mesmo efeito do contorno da pose em pé
  aprovada (que tem 3 buracos entre as pernas).

## Pra depois (se aprovar)

- Respiração: 2-3 frames subindo 1 px o alto das costas/anca (A) ou o alto da bola (B), cabeça parada.
- "zZz" opcional (G/W) em cima da cabeça, como peça separada (tipo `bark_fx`).
- O papel é `corpo` (não `torso`), então o filtro do suéter não pega nessas peças ainda.

---

# Rodada 2: o travesseiro (C e D)

O dono ainda não escolheu entre A e B. Ele mandou 6 fotos novas dela dormindo e sugeriu: "acho que ela precisa de
um travesseiro pra ela subir e dormir". Padrão das fotos: cabeça quase sempre apoiada numa almofada bege ou no
braço do sofá, patas da frente esticadas (às vezes uma por cima da almofada), orelhas relaxadas, uma meio em pé.

## Arquivos

- `travesseiro.txt`: almofada 24x8, `@role objeto`.
- `dormir_C.txt`, `dormir_D.txt`: a cachorra, peça do tamanho do quadro (44x32), `@role corpo`.
- Receitas `../../anims/dormir_C.json` e `dormir_D.json`: quadro **44x32**, travesseiro em `at [16,24]` e
  a cachorra em `[0,0]` por cima. 1 frame de 1000 ms, loop, variantes `contorno` (outline G) e `esquerda` (mirror).
- `../../palette.json`: grupo novo **`travesseiro`** no fim, sem mexer nos outros grupos:
  - `Q` #d1c9bc claro: parte iluminada da almofada de `kiki_dormindo_de_lado_cobertor.jpg`;
  - `q` #b29e8b médio e `Z` #96795f sombra/borda/costura: almofada de `kiki_dormindo_abracando_almofada.jpg`
    (agrupamento de cores só na área da almofada).
- Fotos usadas: `kiki_dormindo_abracando_almofada.jpg` (cor e jeito: peito, cabeça e pata esticada por cima),
  `kiki_dormindo_de_lado_sofa.jpg` (patas esticadas, cabeça no encosto), `kiki_dormindo_cabeca_nas_patas_sofa.jpg`
  (queixo nas patas), `kiki_dormindo_enrolada_colo.jpg` (bola com as orelhas em pé, pro D).

## Decisões

- **Travesseiro**: vista de lado, cantos arredondados, em cima claro (Q), lateral média (q) e borda Z dos dois
  lados. A borda escura faz ele aparecer na taskbar clara; o miolo claro, na escura. Na linha do meio tem uma
  costura pontilhada (Z a cada 3 px) e as pontinhas dos cantos saem 1 px pra fora, como almofada de verdade.
  Testei 6 desenhos: liso, com costura cheia, com costura pontilhada e com dobra/afundado em cima. O liso parecia
  um sabonete e o afundado um pão. O claro Q fica longe do W do focinho porque a borda Z separa os dois.
- **Mesmo quadro e mesma posição do travesseiro nas duas** (44x32, travesseiro em [16,24]): assim a transição
  usa o travesseiro parado e só a cachorra se mexe.
- **C**: traseira deitada no chão como na A (anca, risco tan da coxa, canela no chão, toquinho). As costas sobem
  até os ombros e a barriga sobe do chão (linha 31) até o travesseiro (linha 24) numa diagonal com borda X. O
  vão entre a barriga e o travesseiro fica aberto embaixo, então não prende transparência. O peito afunda no alto
  do travesseiro. A pata da frente vai esticada por cima dele (borda X, pata 2 px na ponta) e o queixo fica
  apoiado nela. Cabeça e orelhas são iguais às da A (olho fechado).
- **D**: a opção B inteira (mesma bola e mesma cabeça), deslocada +15,-6. Ela afunda 2 px no travesseiro (o alto
  dele some debaixo dela, parece fofo) e a cabeça fica na beirada: queixo na quina, focinho pra fora. A patinha
  encolhida da B virou a pata da frente esticada debaixo do queixo, com a ponta caindo pela beirada. Pra fechar
  entalhes, coloquei 1 px X na traseira (que afunda no canto esquerdo) e tirei 1 px da ponta da pata.
- Tamanho da cachorra igual ao das outras poses: o primeiro D1 encolhia a bola pra caber no travesseiro e ela
  ficava parecendo filhote, então descartei. Na D, a traseira passa 2-3 px da quina esquerda.

## Rodadas

- Travesseiro: P1-P6 (acima), escolhida a P5 com a costura simétrica.
- C1: buraco entre o pescoço e a cabeça (o corpo parava antes da nuca) e as costas retas. C2: corpo por baixo
  da nuca, costas inclinadas, anca com dobra, 1 entalhe na nuca fechado.
- D1 (bola encolhida, descartada), D2/D2b (a B por cima, afundando 1 px ou 2 px), D3 (sem/com pata),
  D4 = D3 com pata e entalhes fechados.
- Autocrítica no quadro (8x + 2x nas duas taskbars, ao lado das fotos): C lê "deitada com a cabeça no
  travesseiro"; D lê "deitada em cima da almofada". O travesseiro bege não se mistura com a cachorra preta a 2x.

## Conferência

- `rig.py` = rascunho, pixel a pixel (0 diferença).
- `lint.py --size 44 32`: normal e esquerda só com "silhueta some na taskbar escura" (sem contorno, esperado).
  A borda visível no escuro já sobe pra 23% na C e 34% na D por causa do travesseiro. `_contorno`: limpas.
- `problems()`: normal e esquerda com 0 buracos, 0 soltos e 0 entalhes (travesseiro e cachorra juntos). Nas
  `_contorno` o filtro fecha 1 px entre as orelhas (C 27,10; D 33,13), igual à A/B e à pose em pé.

## Pensando no "subir" (andando, subindo, deitando)

- O travesseiro fica parado em [16,24] no quadro 44x32 e a cachorra em pé (32x32) chega pela esquerda andando.
  Primeiro ela põe as patas da frente no alto plano do travesseiro (colunas 21-34, pé na linha 24, ou seja,
  frente 7 px mais alta, corpo inclinado), depois puxa as de trás (pulinho de 1 frame no ar).
- Já em cima, ela abaixa até a D (2 frames: senta e deita). Pra C, ela só sobe com a frente e deita a traseira
  no chão. Os frames de transição reaproveitam pernas e tronco do trote B com o tronco inclinado, como na corrida.
