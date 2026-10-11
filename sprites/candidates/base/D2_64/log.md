# Log da limpeza do D2 em 64x64

Partida: `base_r0.txt` (copia de `sprites/candidates/tiers/D2_64.txt`, conversao automatica do rascunho
D2 do Figma/gemini). Guia usado: o rascunho `sprites/concepts/D2_figma_gemini_thumb.jpg` alinhado a grade
64x64 (celula ~4,9 x 5,06 px da imagem; canto da celula (11,17) = pixel (28,10) do rascunho).

## r0 (original, so diagnostico)
- Cabeca ilegivel: olhos viraram um monte de E/K, focinho = blocos G/W soltos, orelhas sujas.
- Ruido por todo o corpo: pixels E (azulado) e G no meio do preto, borda serrilhada, patas de longe terminando
  em y=60/61 (nao tocam o chao), rabo com pixel solto.
- Tan so em manchas aleatorias; mancha do peito deformada.

## r1 (reconstrucao limpa, mesma pose/silhueta)
- Silhueta refeita por spans linha a linha seguindo o rascunho D2; contorno X automatico (1 px).
- Orelhas: interior t/T/D, pontudas, grandes (35-41 e 46-51, y 17-27).
- Corpo K com brilho k no dorso/ombro/pescoco e sombra X na barriga; mancha do peito tan + creme W.
- 4 pernas: traseira de perto (diagonal), traseira de longe, dianteira de perto (A), dianteira de longe (B);
  as 4 patas terminam em y=63 (pernas de longe esticadas 2-3 px); longe = D/T (mais escura).
- Rabo: toquinho preto de 2-3 px apontando pra cima/tras.
- Visto na folha: olhos viraram so um quadrado branco (B) com E quase invisivel; focinho em xadrez G/W
  barulhento; faltava a faixa tan que liga a coxa traseira ao resto; corpo "caixa".

## r2
- Cabeca reescrita como bloco unico: sobrancelhas tan (pontinhos), olhos E com contorno e e brilho B, anel G,
  bochecha tan maior, focinho G/W em aglomerados (nao xadrez), linha da boca e, queixo W/G, nariz N com brilho k.
- Faixa tan diagonal da perna traseira de perto subindo ate o joelho (sobre o preto) -> coxa e pata ficam legiveis.
- Mancha do peito: W mais estreito, tan nos flancos.
- Visto: olhos ainda cercados de G demais (faixa cinza entre os olhos), pelos G/W soltos no pescoco parecendo
  poeira, brilho k do traseiro virou zigue-zague.

## r3
- Orelha de longe termina 1 linha antes pra nao grudar no tan da sobrancelha (separa orelha de sobrancelha).
- Sobrancelhas movidas pra y=27, palpebras e em y=28, olhos y=29-30, palpebra de baixo G em y=31.
- Corrigido recorte de 1 px na garupa (linha 38). Mais brilho k no ombro.
- Visto: ainda mosaico G em volta dos olhos; zigue-zague de k no quadril.

## r4 (final)
- Faixa G entre os olhos removida; G agora em aglomerado: palpebra de baixo, cantos externos, ao redor das
  sobrancelhas, testa (G/W salpicados), focinho e queixo.
- Quadril: k so no arco da garupa (16,39)-(18,43). Pelos soltos do pescoco removidos (resta 1 G na bochecha).
- Conferencias: 64x64, so letras X K k D T t G W E B N e, 4 patas em y=63, sem pixel solto na borda.
  Lint: so o erro esperado "silhueta some na taskbar escura".
- Scripts de autoria: `build_rN.py` + `paint_rN.py` (silhueta por spans + pintura por texto).
