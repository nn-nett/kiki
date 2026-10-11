# Proporção — pernas mais longas e corpo mais comprido

Pedido do dono depois de ver o andar: "o corpo dela é um pouquinho maior e as perninhas
levemente mais longas". Confirmado pela foto de perfil `reference/kiki_perfil_potinho.jpg`
(pernas longas, barriga recolhida).

Geradas com `tools/proportion.py` a partir das peças aprovadas (`sprites/parts/32`):
pernas +N trocam N linhas da barriga por canela (cabeça, dorso e patas não mudam de
lugar, continua cabendo em 32x32); corpo +M repete a coluna 12, que é só corpo e está
vazia na região das pernas em todos os frames do andar.

| Pasta | Pernas | Corpo |
|---|---|---|
| `P1/` | +1 | +2 |
| `P2/` | +2 | +2 |

(Uma P3 com corpo +3 cortava 1 px de pata no frame 0 e foi descartada.)
Cada pasta tem as peças (`parts/`), as receitas e a saída (`out/`: parada e andando,
com e sem contorno). Página de comparação animada: https://claude.ai/artifact/8mDaYnhGo8hGKTrh5hvmm1
