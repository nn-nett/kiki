# Trote B (6 frames, articulado) 32x32 - log das rodadas

Arquivos: `legs_trotB0..5.txt` (esta pasta) e `../../anims/walk_b.json`. A peça `upper.txt` e a
`legs_base.txt` não foram tocadas. Sequência 0..5, 100 ms por frame. `upper` com offset [0,1] nos
frames 1 e 4 (apoio) e [0,0] nos outros. Os arquivos são gerados por um script de apoio (blocos por perna,
no scratchpad); o `.txt` é o formato editável final. Critério visual do dono: versão SEM contorno
(a variante "contorno" continua na receita; o lint da sem contorno só acusa "silhueta some na taskbar
escura", que é esperado).

## Desenho do ciclo

- Par A = dianteira de perto (FN) + traseira de longe (RF); par B = dianteira de longe (FF) + traseira de perto (RN).
- Cada par fica apoiado 4 frames (contato, apoio, passagem, empurrão) e no ar 2 frames.
  Frame 0 = contato A / B empurrando; 1 = apoio A / B saindo do chão; 2 = passagem A / B no ar;
  3 = contato B / A empurrando; 4 = apoio B / A saindo; 5 = passagem B / A no ar.
- Pata plantada recua exatamente 1 px por frame (conferido por script, colunas da linha 29 e da linha 31):
  FN 25-24-23-22 (frames 0-3), RF 10-9-8-7 (0-3), FF 18-17-16-15 (3,4,5,0), RN 5-4-3-2 (3,4,5,0).
- Articulação em 3 segmentos (topo se desloca 0-1 px, meio 1-2, pata 2-3):
  - Traseira de perto (RN): garupa/glúteo (contorno de trás, linhas 20-24), faixa tan da coxa (tíbia),
    jarrete (calombo atrás) e metatarso. A faixa muda de ângulo: frame 0 plana e longa (perna esticada pra trás,
    garupa sai 1 px, jarrete em col. 1), 3 quase vertical (perna sob o corpo, garupa "encolhe" em col. 4), 5 = base
    (diagonal de 45 graus). No ar o jarrete SOBE até a linha 22-23 (tíbia quase horizontal) e o metatarso balança
    pra frente com a pata a 2-3 px do chão (referência: husky - zigue-zague glúteo/joelho/jarrete/metatarso).
  - Traseira de longe (RF): bloco preto da coxa e faixa T deslocados 0/+1/+1/+2 (topo/meio/baixo) conforme
    contato/apoio/passagem/empurrão; no ar o jarrete sobe 1-2 linhas e a canela pende pra frente.
  - Dianteiras (FF, FN): bloco preto do ombro/braço, antebraço tan e pata inclinam como linha: pra frente no
    contato, retas na passagem, pra trás no empurrão; no ar o cotovelo vai pra frente, o antebraço dobra pra trás
    e a pata fica curvadinha, 2 px (frames 1 e 4) e 3 px (frames 2 e 5) acima do chão.
- Pernas de longe com T (e D no joelho da traseira) pra ler profundidade.

## Rodada 1 (rascunho)

Visto: pares diagonais certos e patas no chão em todos os frames, mas os deslocamentos da traseira de longe
estavam errados em 4 colunas (a de longe andava 4 px no frame 0), a dianteira de longe encostava na de perto no
frame 3 (massa preta de 6 px) e o ar da traseira só levantava a canela reta (não dobrava). Topo da perna
traseira quase igual em todos os frames.

## Rodada 2

Refiz a traseira de perto com a faixa tan em inclinações diferentes por frame (plana no empurrão, vertical
no contato) e o contorno de trás (garupa/jarrete) mudando de coluna; traseira de longe com deslocamentos
topo/meio/baixo por frame; janela da dianteira de longe afastada da de perto. Checagem por script:
RN 6/6 distintos, RF 5/6, FF 4/6, FN 6/6 nas linhas 21-25.

## Rodada 3 (retorno do dono + referências husky e cão correndo)

O dono pediu que a traseira articulasse tudo (glúteo, joelho/jarrete, pata) e mostrou o husky (zigue-zague da
perna traseira) e o cão correndo. Calculei os ângulos com uma cinemática de 3 elos (coxa, tíbia, metatarso) e
vi que no ar o jarrete sobe muito (linha 22-23), com a tíbia quase horizontal e o metatarso balançando pra frente.
Redesenhei RN/RF nos frames de ar (1, 2, 4, 5) assim. Antes o jarrete ficava fixo na linha 25 e só a canela subia.

## Rodada 4

Conferência com script: 3 buracos transparentes presos (frame 2: bolsão entre a pata no ar e a traseira de longe;
frames 2 e 3: bolsão entre as dianteiras). Corrigi: pata no ar da RN 1 px mais pra trás (abre o canal) e a
dianteira de longe afastada mais 2 px pra trás (janela 15-18), com o cotovelo no ar sem passar da coluna 19.
Resultado: 0 buracos presos nos 6 frames.

## Rodada 5

Garupa: frame 0 empurra o glúteo 1 px pra trás (coluna 2 nas linhas 20-23, único retoque nas linhas 19-20 da
faixa, que ficam por baixo do corpo) e no frame 3 a garupa recolhe (coluna 4 nas linhas 23-24). Lint da versão
com contorno: 0 erros, 0 avisos. Última folha: `review_r6.png` (6ª execução da ferramenta).

## Pontos pro diretor

- A ponta da orelha fica na linha 0 no frames sem oscilação; nos frames 1 e 4 o corpo desce e sobra a linha 0 livre.
- Velocidade do chão: a pata recua 1 px por frame no sprite; a janela deve andar ~1 px do sprite por frame
  (2 px de tela na taskbar a 2x) pra não patinar. Ciclo de 6 frames x 100 ms = 600 ms por ciclo de 2 passos.
- O toquinho do rabo (peça upper) não foi mexido; a garupa só se mexe nas linhas 20-23 da faixa.
