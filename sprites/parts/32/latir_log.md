# Latido (32x32) - log das rodadas

Pedido do dono: "pega o pescoço dela pra cima e vamos articular agora um latido. A língua dela é rosa."
Versão SEM contorno (critério atual do dono). Nada de rotação: cada pose da cabeça é desenhada.

## Arquivos

- `torso.txt` (corpo + toquinho + toco do pescoço, `@socket.pescoco 20,14`) e `head.txt`
  (do pescoço pra cima, `@anchor 4,14`), tirados do `upper.txt` sem mudar pixel.
  Receita `../../anims/stand_head.json` (legs_base + torso + head).
- `head_bark1.txt`: boca entreaberta (fresta escura, sem língua), usada no "prepara" e no "fechando".
- `head_bark2.txt`: "AU!" (boca bem aberta, língua rosa P, focinho 1 px mais alto na ponta).
- `bark_fx.txt` (opcional): 2 risquinhos de som em G, encaixam em `head.boca`.
- Receitas: `../../anims/latir.json` (recomendada), `latir_tranco.json` (opção com tranco do corpo),
  `latir_fx.json` (opção com os risquinhos).
- `upper.txt`, `legs_*.txt`, `stand.json`, `walk_b.json`, paleta e ferramentas: intocados.

## Corte do pescoço

- Cabeça = tudo das linhas 0-14 nas colunas 16-31 (orelhas, rosto, focinho, queixo e o alto do
  pescoço/garganta). 16x15 px, âncora (4,14) = ponto (20,14) do quadro.
- Torso = o resto (linhas 15-20, toquinho nas linhas 12-14) + um **toco do pescoço** repetido por baixo
  da cabeça: linha 11 col. 18-21, linha 12 col. 18-23, linhas 13-14 col. 17-25 (mesmos pixels do upper).
  Na pose parada a cabeça cobre o toco inteiro; quando a cabeça anda 1 px (pra frente ou pra baixo)
  o toco aparece atrás da nuca e não abre buraco.
- Encaixe: `{"part": "head", "attach": "torso.pescoco"}`. Pra migrar as outras receitas basta trocar
  `upper` por `torso` (mesmo "at"/"offset") + a cabeça presa no pescoço; o offset do torso leva a cabeça junto.
- Efeito colateral bom: a máscara de papel "torso" (usada pelo filtro do suéter) agora não inclui a cabeça
  (a cabeça tem `@role cabeca`).

## Prova de igualdade do stand_head

Renderizado com o `rig.py` e comparado pixel a pixel (RGBA) por script:
- `stand_head_0.png` vs `stand_0.png`: 0 pixels diferentes;
- `stand_head_contorno_0.png` vs `stand_contorno_0.png`: 0;
- `stand_head_0.png` vs `base/kiara_32.png`: 0;
- frame 0 do latido vs `stand_0.png`: 0.

## Desenho do ciclo (`latir.json`)

| frame | cabeça | offset da cabeça | duração | o que acontece |
|---|---|---|---|---|
| F0 | head | 0,0 | 300 ms | parada, boca fechada (= stand) |
| F1 | head_bark1 | 0,+1 | 90 ms | prepara: cabeça abaixa 1 px, boca abre uma fresta escura |
| F2 | head_bark2 | +1,0 | 170 ms | "AU!": cabeça projeta pra frente/cima, boca bem aberta, língua rosa |
| F3 | head_bark1 | 0,0 | 100 ms | fechando |

Sequência `0,1,2,3,1,2,3` = dois latidos seguidos ("au-au") e pausa de 300 ms no loop. Esquerda por espelho.

- head_bark2: o focinho foi redesenhado com a ponta 1 px mais alta (nariz nas linhas 9-11) = a cabeça
  "levanta o focinho" pra latir sem rotação e sem cortar a orelha (que continua na linha 0). Mandíbula 2 px
  abaixo: interior escuro N, língua P (3 px), queixo grisalho G (com ponta X), e um vão transparente na
  frente da boca, que deixa a silhueta ler "boca aberta" até na taskbar escura. Orelhas, olho castanho com
  brilho, sobrancelha cinza e grisalho do focinho iguais à pose base.
- head_bark1: mandíbula 1 px abaixo, só fresta escura (N + lábio K) e queixo G uma linha abaixo.
  **Sem língua de propósito**: o rosa só aparece no "AU!", então o latido "pisca" no ritmo.
- Ponta da língua no quadro: coluna 30 (31 é o vão da boca); nada sai do 32x32.

## Conferência

- `lint.py --size 32 32`: latir, latir_esquerda, latir_tranco, latir_fx e stand_head só acusam
  "silhueta some na taskbar escura" (esperado sem contorno). latir_contorno e latir_tranco_contorno: 0 erros.
- Buracos presos (flood fill da borda) e pixels soltos (opaco sem vizinho-4): 0 em todos os frames de
  latir, latir_esquerda, latir_tranco(_esquerda), stand_head. Única exceção: o frame "AU!" do latir_fx tem
  4 "soltos" = os próprios risquinhos do efeito (separados do corpo de propósito).
- Na variante com contorno aparecem 3 buracos entre as patas traseiras (5,27-29); já existem iguais no
  `stand_contorno` (vêm do filtro de contorno nas pernas, não da cabeça).

## Rodadas

1. Mandíbula descendo reta (A) e em cunha (B, B2): lia como "língua pra fora" (blep), e o interior preto
   grudava no nariz preto virando uma mancha só.
2. Cunha mais inclinada (D, E, F): a mandíbula ficava curta e virava uma faixa cinza vertical embaixo da
   bochecha; ainda lia como lambida.
3. Vão transparente na frente, interior castanho escuro (D) e dente branco: o dente W virou um pixel
   perdido; o interior D virou um bloco marrom. Vão na frente aprovado.
4. Mandíbula comprida até a col. 29 (L "caixa"): primeira que leu "boca aberta", mas parada demais
   (faixas W / preto / rosa / cinza empilhadas).
5. Focinho levantado 1 px na ponta (T1-T3): com o vão na frente (T3) lê como latido em 2x e 3x, clara e escura.
   Escolhido pro F2.
6. Ciclo montado: no F1 (cabeça 1 px abaixo) a garganta castanha da peça descia e emendava no peito,
   apagando a faixa escura do pescoço -> tirei a garganta da linha 15 do head_bark1.
7. Efeito de som (v1-v4): v1 encostava na testa (parecia espinho), v3 (tracinhos verticais) parecia borda,
   v4 (3 riscos) poluído -> v2 (2 diagonais soltas, acima do nariz e abaixo do queixo).
8. Tranco do corpo: torso +1 pra frente (T1) lê como "investida", com 1 degrau de 1 px no bumbum (linhas
   19-20 ficam com as pernas); torso 1 px pra cima esticava o corpo; cabeça +1,+1 perdia energia.
   Ficou como opção (`latir_tranco.json`); a receita principal mexe só a cabeça (corpo idêntico ao stand).
9. Com língua no F1/F3 a boca parecia aberta em 6 dos 7 frames -> head_bark1 sem língua; o rosa só no F2.

## Dúvidas pro diretor / dono

- O focinho levantado 1 px no "AU!" ainda é a Kiara? (alternativa: focinho igual ao da base e só a
  mandíbula caindo, versão L da rodada 4, mais "boca aberta" que "latido").
- Tranco do corpo (latir_tranco) ou só a cabeça (latir)?
- O efeito de som fica apertado na borda do 32x32 (col. 30-31). Se o dono quiser, fica melhor desenhado
  pelo app fora do sprite.
- Olho apertado no "AU!": não fiz (mantive olho aberto com brilho).
- Durações (pausa de 300 ms, 2 latidos por ciclo) dependem de como o app vai usar.
