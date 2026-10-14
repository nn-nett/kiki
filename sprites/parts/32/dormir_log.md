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
