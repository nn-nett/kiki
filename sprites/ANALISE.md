# Análise das animações aprovadas (15/10)

Pedido do dono: "faz uma análise das animações e dos frames aprovados. O que tem em comum? O que pode ser
replicável?". Base: os frames finais (`sprites/final/`), as receitas (`sprites/anims/`) e o histórico de
aprovações e reprovações (`CLAUDE.md`, logs em `sprites/parts/32/*_log.md`).

Aprovadas: parada, andando (trote B), latindo (com tranco), piscando, ofegante (parada, em revisão) e andando
ofegante (corpo do andar + boca ofegante).

## Medidas (pixels que mudam de um frame pro outro, frames finais 32x32)

| Animação | Durações (ms) | O que muda por frame | Onde |
|---|---|---|---|
| andando | 100 × 6 | 107-233 px | pernas sempre (76-95 px); cabeça, tronco e rabo só nos 4 frames em que o corpo sobe/desce 1 px |
| latindo | 300, 90, 170, 100, 90, 170, 100 | 84-168 px | quase tudo na cabeça (76-125 px); tronco 8-35 px no tranco de 1 px |
| piscando | 1500, 60, 110, 60 | 2-5 px | só o olho |
| ofegante (versão antiga) | 130 × 2 | 55 px | tronco + rabo + cabeça: o corpo inteiro descia 1 px (o dono reprovou) |

Deslocamentos usados nas receitas: andar = tronco/cabeça +1 px pra baixo (frames 1 e 4); latido = cabeça +1 px
pra baixo na preparação e tronco +1 px pra frente no AU!; ofegante = queixo 1 px a mais na expiração, peito 1 px.

## O que tem em comum

1. **Todo movimento é de 1 px.** Balanço do trote, tranco do latido, queixo e peito do ofegante, pálpebra do
   piscar. Quando algo pulou 2 px de uma vez (a língua do primeiro andar ofegante) o dono achou estranho.
2. **Só mexe a parte que tem motivo pra mexer.** Piscar mexe 2-5 px, todos no olho. Latido concentra a mudança na
   cabeça. O ofegante foi reprovado quando o corpo inteiro (costas e rabo) descia ("o movimento é mais no
   peito/torso/queixo, o resto não mexe tanto") e depois a barriga também saiu ("ela respira pelo peito").
3. **É sempre a mesma cachorra.** Todas as cabeças (normal, latido, ofegante, corrida) têm o rosto copiado pixel a
   pixel, a mesma âncora no pescoço (4,14) e o olho no mesmo ponto (6,9). As reprovações mais fortes foram quando a
   identidade mudou: "mudou o tamanho do focinho", "cadê o pescoço", "parece que ela tem dwarfismo" (corrida com
   pernas curtas e corpo compacto).
4. **Ritmo de ação = preparação curta, pico mais longo, volta curta.** Latido 90 → 170 → 100 ms; piscar
   60 → 110 → 60 ms. O momento mais "forte" (AU!, olho fechado) é o que fica mais tempo na tela.
5. **Pausa antes da ação.** Latido começa com 300 ms parada; o olho fica aberto 1,5 s (e na simulação o piscar
   vem a cada 2,5-7 s, sorteado). Isso deixa a ação legível e evita parecer tique.
6. **Ciclos com ritmo fixo e cada parte no seu relógio.** Andar 100 ms, ofegar 130 ms, piscar sorteado. O dono
   pediu explicitamente que a respiração e o passo não fossem sincronizados.
7. **Regras de desenho que se repetiram em todas:** borda de baixo em X (barriga, peito, pernas); perna de longe
   atrás da barriga, com a primeira linha em K; nada de pixel solto, buraco ou orelha sem borda; só cores da
   paleta (a pele clara na barriga foi reprovada); rosa só na língua; patas na linha 31; o passo da janela é
   igual ao recuo da pata no chão (não patina).
8. **Variações de graça.** Esquerda (espelho) e taskbar escura (contorno G) saem por filtro; a montagem por
   camadas dá exatamente os mesmos frames (conferido nos 80).

## O que dá pra replicar

| Receita que já funciona | Onde foi usada | Dá pra usar em |
|---|---|---|
| **Remendo pequeno + âncora por frame + relógio próprio** | piscar (olho), ofegante andando (boca) | orelha mexendo, lamber o focinho, farejar (nariz 1 px), olho fechado de sono, sobrancelha de "pidão" |
| **Troca de cabeça (expressão de cabeça)** | latir, ofegante | bocejo (boca abrindo devagar, como o AU! mais lento), comer (cabeça baixa), cheirar o chão |
| **Corpo em ciclo: faixa de pernas por frame + balanço de 1 px** | andando | passeio de coleira (trote + peitoral/guia por cima), suéter e noturna por filtro, "andar devagar" com o mesmo ciclo em 150 ms |
| **Respiração de 1 px no peito** | ofegante parado | sentada/idle e dormindo: o mesmo bombear, mais lento (400-600 ms), com o piscar por cima |
| **Preparação → pico → volta** | latido, piscar | reação ao toque (pulinho), saltar, abanar o toquinho |
| **Peça separada com âncora** (cabeça, olho) | camadas | **rabo** como peça própria (hoje está dentro do tronco): abanar o toquinho em qualquer estado, igual ao piscar |
| **Transição curta com peças existentes** | ainda não feita | parado → andando = 1ª faixa do trote com o tronco parado; andando → parado = último passo + 1 frame de assentar |

## Lições pra corrida (ainda não aprovada)

A corrida quebrou a regra 3 (mesma cachorra): o corpo encolhia até virar bola (19 colunas) e as pernas ficavam
curtas, então ela parecia outra cachorra ("dwarfismo", "o corpo tá muito compacto"). O redesenho (v5) parte das
medidas da pose parada: pernas do mesmo comprimento, corpo comprido em todos os frames, cabeça igual, e mantém as
outras regras (1 px de cada vez na cabeça, toquinho acompanhando a coluna, bordas X).

## Próximos passos sugeridos

1. Separar o **toquinho do rabo** como peça (como a cabeça), pra abanar em qualquer estado.
2. **Sentada/idle** e **dormindo** com a respiração de 1 px no peito + piscar (reaproveita o ofegante e o olho
   fechado).
3. **Reação ao toque** no ritmo preparação → pico → volta, com o rabo abanando.
4. **Transições** de 1-3 frames com as faixas de pernas que já existem.

## Reanálise geral (11/11)

Pedido do dono: "dá uma reanalisada em tudo". Olhei de novo todos os frames aprovados e os pendentes, ampliados e em
tamanho real (2x e 3x, fundo claro e escuro), com a ferramenta nova `tools/bancada.py`.

### Aprovadas: continuam de pé

Parada, andando, latindo e piscar passam nas oito regras acima e não precisam de retoque. Dois pontos pra decisão do
dono, sem mexer em nada por enquanto:

- **Orelha por dentro.** No perfil aprovado é castanha; nas fotos de frente é escura com a base castanha. Enquanto ela
  só existia de perfil isso não aparecia; na meia-volta a orelha muda de cor no caminho. Dá pra deixar (lê como a
  orelha virando) ou escurecer a parte de cima da orelha do perfil.
- **Ofegante parada (A2, meio-termo, A3).** As três diferem em 2 a 6 pixels da barriga. Em tamanho real não dá pra
  distinguir uma da outra. Sugestão: fechar com o meio-termo, que foi o último pedido, e seguir.

### Pendentes

- **Galope.** Nenhuma das duas versões está certa, e pelo mesmo motivo com sinais trocados. A v4 encolhe o corpo até
  19 colunas (bola) e encurta as pernas: daí o "dwarfismo". A v5 corrigiu demais: o corpo fica com 27-30 colunas em
  todos os frames (parada tem 23), com as costas retas, e os frames f4/f5 parecem ela parada de pernas abertas. O que
  faz um galope ler é a alternância entre dois momentos: recolhida (costas arqueadas, patas de trás passando por baixo
  das da frente) e esticada (tudo no ar, patas pra frente e pra trás), com o comprimento do corpo oscilando em volta
  do comprimento da parada (uns 21 a 26), nunca 30. Proposta: refazer começando só pelas duas poses-chave, aprovar as
  duas, e só então desenhar os frames do meio.
- **Dormindo.** As quatro opções leem como "cachorra deitada". A D (inteira em cima do travesseiro) é a mais compacta e
  a que melhor lê em tamanho real; a A é a melhor sem travesseiro. Falta a escolha do dono.
- **Olhar pro outro lado.** Refeito na rodada 5 (`parts/32/virar_log.md`, seção 10).

### O que mudou no jeito de trabalhar (vale pras próximas animações)

1. **Decidir em tamanho real.** Várias rodadas reprovadas pareciam boas a 10x, onde ruído de pixel passa por detalhe.
   A bancada mostra sempre o ampliado e o tamanho real juntos.
2. **Vista intermediária = híbrido das duas pontas aprovadas.** A cabeça meio de lado só funcionou quando deixou de
   ser um desenho novo: metade da cabeça de frente, metade do perfil. Vale pra corpo 3/4 e pra transições.
3. **Posição por medida, não no olho.** Escolher o eixo do giro (o pescoço), calcular onde caem olho e nariz em cada
   ângulo e conferir a coluna do brilho do olho frame a frame.
4. **Uma marca é a mesma em todas as vistas.** A mancha clara do peito existe no perfil, então tem que existir de
   frente e no 3/4, no lugar que a geometria manda. É a regra 3 (mesma cachorra) aplicada às marcações.
5. **Poses-chave primeiro.** Aprovar as duas ou três poses que definem a animação antes de desenhar os frames do meio.
