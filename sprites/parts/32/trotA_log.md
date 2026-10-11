# Trote A (articulado) 32x32 — log das rodadas

Arquivos: `legs_trotA0..3.txt` (esta pasta) e `../../anims/walk_a.json`. `upper.txt` e `legs_base.txt` não foram
tocadas. Faixa de 13 linhas (19–31 do quadro), `legs` em `at [0,19]`, `upper` com `offset [0,1]` nos frames 0 e 2
e `[0,0]` nos 1 e 3, 130 ms/frame, sequência 0,1,2,3, variantes `contorno` (G) e `esquerda` (mirror).
Critério visual desta entrega: versão SEM contorno (pedido do dono). As pernas foram desenhadas por bloco
(uma perna por frame, empilhadas: traseira de longe, dianteira de longe, traseira de perto, dianteira de perto);
o gerador ficou no scratchpad, os `.txt` são a fonte editável.

## Desenho (valem para as 5 rodadas)

Pares diagonais: A = dianteira de perto (NF) + traseira de longe (FH); B = dianteira de longe (FF) + traseira de
perto (NH). Cada perna tem topo (ombro/quadril, linhas 21–25), meio (cotovelo/jarrete + canela, 25–29) e pata (30–31).

Coluna do tan da canela na linha 30 (= posição da pata), recuando exatamente 1 px por frame de apoio:

| perna | f0 | f1 | f2 | f3 |
|---|---|---|---|---|
| NF dianteira de perto (A) | 24 contato | 23 vertical | 22 empurrão | no ar (levantada 3 px) |
| FH traseira de longe (A) | 10 contato | 9 vertical | 8 empurrão | no ar (levantada 2 px) |
| FF dianteira de longe (B) | 15 empurrão | no ar (levantada 3 px) | 17 contato | 16 vertical |
| NH traseira de perto (B) | 2 empurrão | no ar (levantada 2 px) | 4 contato | 3 vertical |

- Dianteiras: topo `KKK` + cotovelo + antebraço + pata. No apoio a perna inclina (contato: topo 22, cotovelo 23,
  punho 24; empurrão: topo 22→21, antebraço 21, pata 22). No ar: cotovelo vai pra frente, antebraço dobra pra trás
  e a pata fica "curvadinha" (sola `KXXX` à frente do punho), 3 px acima do chão.
- Traseira de perto (NH): zigue-zague como no husky de referência: coxa preta com a faixa tan diagonal (joelho no
  alto, tíbia descendo pra trás até o jarrete) e metatarso vertical até a pata. Frame 0 (empurrão): glúteo mais
  volumoso e esticado pra trás (preto até a coluna 1), faixa mais deitada. Frame 2 (contato): glúteo recolhido
  (a linha 22 perde a coluna 3), faixa mais em pé, joelho à frente. Frame 1 (no ar): joelho à frente, jarrete
  dobrado (canela vai pra trás), pata sobe 2 px. Frame 3: a da base.
- Traseira de longe (FH): joelho/jarrete (`KKDXX`, `KKTK`) avança no contato (+1), recua no empurrão (−1) e no ar faz
  o Z (joelho à frente, jarrete atrás, pata à frente). Cores de longe: `T`/`D`.
- Pernas de longe um tom mais escuras (T/D no lugar de t). Nenhuma peça girada.

## Rodada 1 (primeiro rascunho)

Visto na folha ampliada: as 4 pernas já mudam de pose, mas FH/FF/NF eram cópias de um molde só (o frame 0 igual
ao 3, etc.), a faixa tan da traseira de perto quase não mudava de ângulo e o glúteo era fixo.
Buracos (script, 4-vizinhos): 0 sem contorno. Com contorno aparecem bolsões entre FH e FF (ver "Pontos abertos").

## Rodada 2 (dianteiras e traseiras com posições próprias; glúteo mexe)

Mudei: dianteiras com caminhos de coluna por linha (topo, cotovelo, punho, pata) em vez de uma coluna só;
FF recuada 1–2 px (topo em 16–17) pra não encostar na NF no frame 2; glúteo da NH variável por frame
(linha 22 começa na coluna 2/4/4/3, cunha preta mais larga no empurrão, menor no contato).
Visto: faixa deitada do frame 0 ficou como "barra" laranja solta (`tt` em duas linhas).

## Rodada 3 (faixa e passo da pata no ar)

Faixa do frame 0 passou a diagonal de ~1,5 coluna por linha (6,22)(4–5,23)(3,24)(2–3,25), sem a barra solta.
Script de articulação (linhas 21–25 por perna): as 4 pernas com 4/4 variantes distintas. Visto: a pata no ar da
NF ia pra trás do ponto de apoio e depois "pulava" pra frente (passo sem fluidez).

## Rodada 4 (fluidez do passo no ar + referências do dono)

Patas no ar agora andam pra frente entre o empurrão e o contato (NF 22→23→24, FF 15→16→17, NH 2→3→4, FH 8→9→10).
Conferido contra `husky_perfil_jarrete.png` (traseira em Z: coxa/joelho pra frente, canela inclinada pra trás até o
jarrete, metatarso vertical) e `cao_correndo_esticado.png` (dianteira esticada com cotovelo dobrado, traseira
estendida pra trás): a NH ficou assim (glúteo+faixa+jarrete mudam por frame, metatarso vertical no apoio, Z fechado
no ar). Folha: as 4 poses leem como trote (par A à frente no 0, par B no 2, passagens com um par dobrado).

## Rodada 5 (final)

Dianteiras no ar sobem 3 px (cotovelo mais dobrado, sola na linha 28); traseiras no ar 2 px (linha 29).
Checagens finais (scripts no scratchpad):
- Articulação, linhas 21–25 por perna: NH, FH, FF, NF = 4/4 variantes distintas (por camada e por janela de colunas
  do `.txt`); pares de frames diferem de 2 a 22 px por perna.
- Patas plantadas: recuo de exatamente 1 px por frame de apoio em linhas 30 e 31 (borda esquerda e direita).
- Pés na linha 31 em todo frame (12, 7, 12 e 5 px). Buracos sem contorno: 0 nos 4 frames (e no espelho).
- Lint sem contorno: só o erro "silhueta some na taskbar escura" (esperado, ignorado a pedido). Lint com contorno:
  0 erros, 0 avisos.

## Pontos abertos (pro diretor)

- **Passada x regra de não escorregar.** O pedido tinha "passadas de ±2–3 px nas patas" e "recua no máximo 1 px
  por frame". Cumpri a segunda (3 frames de apoio por perna = 2 px de recuo total) e as patas somam 2–3 px de
  excursão quando contamos o passo no ar. Se o dono quiser passada maior, é preciso aceitar 2 px/frame (e a janela
  andar 2 px por frame) ou subir pra 6 frames.
- **Contorno G: bolsões transparentes.** Com `outline`, o vão de 1–2 px entre a pata de longe traseira e a dianteira
  de longe (frames 0, 1, 3) é preenchido nas patas e deixa bolsões de 2–6 px transparentes entre as pernas. Sem
  contorno não há buraco. Resolver só se o contorno voltar a valer (afastar as patas em 2 px ou pintar o bolsão).
- **Dianteiras mais afastadas que na base** (FF topo em 15–17 em vez de 17–19) pra não encostar na NF nos contatos.
- Toquinho e `upper` intocados (o dono ajusta depois).
