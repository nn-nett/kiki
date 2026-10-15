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
