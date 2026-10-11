# C2 16x16 — log das rodadas

Origem: `../C2_32_opus/base_o5_castanho.txt` (32x32 aprovado). Letras permitidas: K X T D G W E B.
`guia.txt` = reducao automatica 2x2 (so guia, ficou borrado: orelhas viram 2 blocos, olho some,
focinho vira mancha). Tudo abaixo foi redesenhado pixel a pixel por cima.

Proporcao usada (32 -> 16): orelhas y0-3, cabeca y3-7, tronco y7-10 (linha do dorso em y7),
pernas y11-15. Orelhas abrem pra fora na base (quase morcego). Cabeca virada pra direita.

## r1 (exploracao em rascunhos v1..v5 antes de salvar)
- v1: copia direta do guia (cabeca 5 linhas, tronco 4, pernas 4) -> pernas curtas demais,
  orelhas pequenas, corpo "bloco".
- v2: orelhas abertas na base (3 px na ponta de baixo, 4 px na base) -> leu melhor.
- v3/v4: testei tronco mais baixo e pernas mais longas (5 linhas) -> proporcao do 32 volta,
  pernas finas de verdade.
- v5/m3: cabeca 5 linhas com queixo; focinho G/W; patas com dedinho pra direita.
- Salvo como r1: olho E de 1px, focinho W W X + G G, pernas T.
- Problemas vistos na folha: olho E (marrom sobre preto) quase invisivel em 1x/2x; focinho
  "bloco branco"; pernas traseiras sem volume; so 1 cor de pata.

## r2
- Olho: E + B (brilho) a direita, com G em cima/esquerda (sobrancelha e anel grisalho).
  Um pixel preto de ponte (12,5) separa o brilho do focinho (no 32 tem X no mesmo lugar).
- Focinho alongado ate x15 (focinho fino): W W + nariz X na ponta; G embaixo (mandibula/queixo).
- Coxa traseira: pixel K extra em (3,11) pra perna de tras nao ficar fininha igual a da frente.
- Pernas longe (x1 e x8) com K 2 linhas e tan so embaixo; pernas perto (x4, x11) com tan de y12.

## r3 (final do 16)
- Orelha de tras (esquerda) continua em tan atras da cabeca (7,4): vira a orelha maior, como no 32
  (la ela desce ate y7 ao lado do cranio).
- D (tan escuro) em (9,9): sombra no peito, ao lado da mancha creme, igual ao 32 ("tDWtt").
- Testei D logo abaixo do olho (como no 32) e ficou parecendo olho maior/lagrima: descartado.
- Testei orelhas estreitas (1 px de tan no meio): ficaram finas, tipo chifre; fiquei com as abertas (mais "orelhao").
- Testei a orelha de tras com 6 linhas (tan ate y5): ficou comprida demais; fiquei com 5.
- Testa ficou toda preta (sem pontinhos, sem cristinha), como pedido.
- lint: 0 erros, 0 avisos.
