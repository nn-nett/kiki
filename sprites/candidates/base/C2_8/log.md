# C2 8x8 — log das rodadas

Origem: `../C2_32_opus/base_o5_castanho.txt`. So 3 cores: K T G. `guia.txt` = reducao 4x4
(so guia: virou uma mancha preta com 3 pontos).

Proporcao (16 -> 8): orelhas y0-1, cabeca y2-4 (4 px de largura, x4-7), tronco y4-5, pernas y6-7.
Dorso em y4; rabo = 1 px em (0,3); quatro pernas em x0, x2, x4, x6 (pernas de perto com tan nas 2 linhas,
pernas de longe com K em cima e tan na pata).

## r1
- Exploracoes antes de salvar: 4 layouts (orelhas de 1 px so com ponta, orelhas com base de 2 px,
  cabeca de 2 ou 3 linhas, tronco de 2 ou 3 linhas, rabo em x0 ou x1, focinho G em L ou 2x2).
  Escolhido: cabeca 3 linhas sobreposta ao tronco de 2 linhas, orelha K com T dentro, focinho G 2x2,
  peito T, pernas T (tronco de 3 linhas deixava as pernas curtas demais).
- Problemas: sem olho, cara "sem rosto"; focinho grande demais e sem nariz.

## r2
- Olho = pixel T (castanho) em (5,3), colado no focinho G (o T e a unica cor marrom da paleta
  de 3 cores); bochecha virou preto, a mancha tan fica so no peito (5,5).
- Testei G em (5,2) como sobrancelha: lia como "pontinho na testa" (o dono ainda vai decidir a testa)
  -> descartado. Testei coluna tan olho+bochecha+peito: lia como listra, nao como olho -> descartado.

## r3
- Nariz K na ponta (7,3) e mandibula G em (6,4),(7,4) + G (6,3): leitura de "focinho com nariz escuro"
  em vez de bloco claro.
- lint passou a acusar so "silhueta some na taskbar escura" (33%), esperado (nariz K some no escuro).

## r4 (final do 8)
- Orelha de tras (esquerda) mais larga, K T K com a ponta no meio (x2-4), como no 32 onde a orelha
  de tras e maior; orelha da frente continua K T. Silhueta de 2 orelhas diferentes = "orelhao".
- lint: unico erro e "silhueta some na taskbar escura" (32%), ignorado conforme combinado.
