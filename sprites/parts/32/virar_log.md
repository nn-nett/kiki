# Virar pro outro lado: log (rascunho, 15/10)

Pedido do dono: "Um desafio: fazer ela olhar pro outro lado... ela vai girar a cabeça, o pescoço faz o movimento
com um pouco do peito (a pata do lado oposto que ela tá levantando sobe, né?) pensa nisso."

Hoje, na meia-volta, o app troca `parada` por `parada_esquerda` de uma vez. Aqui estão duas propostas de movimento,
montadas no rig com peças novas (nada das peças aprovadas foi alterado). Sem contorno nos previews.

## 1. Como um cachorro pequeno, parado, vira pro outro lado

**De que lado a vemos.** Ela está de perfil olhando pra DIREITA da tela. Para quem olha a tela, quem encara a
direita mostra o **lado direito** do corpo (fique de pé, vire pra sua direita: quem estava na sua frente agora vê o
seu lado direito). Então nos sprites de perfil vemos o lado DIREITO dela: as pernas "de perto" (a da frente nas
colunas 21-23 e a de trás nas colunas 2-4) são as direitas, e as "de longe" (frente 17-19, atrás 7-10, as que ficam
atrás da barriga) são as esquerdas.

**Pra que lado ela gira.** Pra passar de frente pra gente (proposta B) ou olhar por cima do ombro do nosso lado
(proposta A), ela gira **pra direita dela** (sentido horário visto de cima): o focinho vai da direita da tela,
passa por nós e termina na esquerda.

**Ordem (a cabeça vai na frente, o resto vem atrasado):**
1. olhos/cabeça: a cabeça começa a virar (3/4) com o corpo ainda parado;
2. pescoço: torce e leva a cabeça até ficar de frente (ou por cima do ombro, na A);
3. ombros/peito: o peito vira um pouco, ou inteiro na B, sempre um passo atrás da cabeça;
4. patas: a pata da frente que ficou leve sobe, e desce quando o corpo chega.

**Qual pata levanta (resposta pro dono: sim, a do lado oposto).** Quando a cabeça e o pescoço vão pra direita dela,
o peso da frente do corpo vai junto pra direita. A **pata da frente direita** (a de dentro da curva) fica carregada
e vira o pivô, e a **pata da frente esquerda** (a de fora da curva, do lado oposto ao giro) fica leve. É ela que
levanta. Numa volta completa, essa é a pata que dá a volta por fora, pro lado novo (como o "cruzar por fora" de
cavalo e cachorro girando no lugar). Quando ela só olha pra trás, o peso muda pouco, então a pata esquerda sobe só
um pouquinho (1-2 px) e volta pro chão.
No sprite isso é a **pata da frente de longe** (colunas 17-19 no perfil). Na vista de frente ela aparece no lado
direito da tela, porque, de frente pra gente, a esquerda dela fica à nossa direita.
Obs.: o pedido original dizia que vemos o lado esquerdo dela. Pela conta acima vemos o direito, mas a resposta em
pixels é a mesma nas duas leituras: sobe a pata da frente de longe (a do lado de fora da curva).

**Ritmo (o mesmo das aprovadas):** pausa curta parada → preparação curta (cabeça 3/4) → pico mais longo (olhando pra
trás / olhando pra gente) → volta curta.

## 2. Proposta A: olhar pra trás (`anims/virar_A.json`, loop pra preview)

O corpo continua virado pra direita. A cabeça gira por cima do ombro direito dela (o do nosso lado), passando de
frente; o pescoço torce, o peito vira um pouco, a pata esquerda da frente sobe e volta.

| frame | ms | cabeça | tronco | pernas |
|---|---|---|---|---|
| f0 | 300 | `head` (parada) | `torso` | `legs_base` |
| f1 | 100 | `head_virar34` (1 px pra trás) | `torso` | `legs_base` |
| f2 | 110 | `head_virar_frente` | `torso_virarA1` (garganta aparece, mancha creme 1 px mais pra frente) | `legs_virarA_p1` (pata 1 px) |
| f3 | 700 | `head_virar_tras` (olhando pra trás, 1 px mais baixa) | `torso_virarA2` (pescoço torcido, peito mais virado) | `legs_virarA_p2` (pata 2 px, punho dobrado) |
| f4 | 100 | = f2 | | |
| f5 | 100 | = f1 | | |

Total 1,41 s. Pixels que mudam entre frames: 124, 121, 180, 180, 121, ou seja só na cabeça, no pescoço/peito e na pata,
o resto do corpo não mexe. `head_virar_tras` é a `head.txt` espelhada pixel a pixel (mesmo rosto), só a nuca ganhou
borda X porque quem continua o pescoço é o tronco.

## 3. Proposta B: meia-volta passando de frente (`anims/virar_B.json`, sem loop)

Direita → cabeça 3/4 → cabeça de frente com o corpo em 3/4 → tudo de frente (pata no alto, ela olha pra gente) →
cabeça 3/4 pro outro lado com o corpo de frente → perfil esquerdo com o corpo em 3/4 → parada esquerda. A cabeça vai
sempre um passo na frente do corpo (o "atraso" que deixa o giro natural).

| frame | ms | cabeça | corpo | pata esquerda da frente |
|---|---|---|---|---|
| f0 | 300 | perfil dir. (`head`) | perfil (`torso` + `legs_base`) | chão |
| f1 | 100 | 3/4 (`head_virar34`) | perfil | chão |
| f2 | 110 | de frente (`head_virar_frente`) | 3/4 (`torso_virar34` + `legs_virar34_p1`) | 1 px |
| f3 | 260 | de frente | de frente (`torso_virar_frente` + `legs_virar_frente_p2`) | 2 px, dedos pra dentro |
| f4 | 110 | 3/4 esq. (`head_virar34_esq`) | de frente (`legs_virar_frente_p1`) | 1 px |
| f5 | 100 | perfil esq. (`head_virar_esq`) | 3/4 esq. (`torso_virar34_esq` + `legs_virar34_esq`) | chão |
| f6 | 300 | perfil esq. | perfil esq. (`torso_virar_esq` + `legs_virar_esq`) | chão |

Total 1,28 s. f0 = `parada` e f6 = `parada_esquerda` pixel a pixel (conferido), e a variante `_esquerda` faz a volta
da esquerda pra direita. O centro da cabeça anda 23 → 22 → 18 → 15 → 12 → 10 → 8 (devagar no começo e no fim). A
silhueta inteira fica no lugar (centro entre as colunas 13 e 16.5), então a janela não precisa andar (`step_px` 0).

**Cabeça de frente (`head_virar_frente`, 15 linhas como a de perfil, olhos na mesma linha 9-10):** orelhas enormes
em pé, abertas pra fora, com castanho dentro e borda X dos dois lados; testa preta; sobrancelha castanha (t) com
grisalho G; olhos castanhos E 2x2 com 1 px de brilho B (no mesmo lado nos dois); grisalho em volta dos olhos, no
focinho e no queixo (G/W); bochechas castanhas; nariz N de 3 px em cima e 1 embaixo; focinho fino (5 px num rosto de
11). Referências: `reference/3e38dc34-…jpg` (de frente), `d1a33dab-…jpg` (3/4, rosto), `f339af0b-…jpg` (corpo 3/4 com
a cabeça virada pra câmera).

**Corpo de frente:** mesma altura de peito (linhas 15-24) e de perna (25-31) do perfil; peito com a garganta
castanha e a mancha creme W no meio, ombros pretos, pernas castanhas finas com borda X e patas com X embaixo. As
patas de trás ficam escondidas atrás das da frente (testei com elas aparecendo; ficou poluído).
**Corpo 3/4:** o perfil encurtado 4 colunas (2 de cada lado, gira em volta do meio), peito virado mostrando a
mancha, pata da frente direita (de perto) à esquerda e a esquerda (de longe) à direita, que é a que sobe.

## 4. Conferências

- `problems()` (tweak.py): sem buraco e sem pixel solto em todos os frames das versões normal e esquerda. Na
  `_contorno` aparecem "buracos" de 1 px entre as pernas, que o filtro de contorno fecha. A `parada_contorno`
  aprovada tem o mesmo, em (5,27-29).
- `lint.py --size 32 32`: só cores da paleta, patas na linha 31 em todos os frames. Sem contorno, o único erro é o
  já aceito ("silhueta some na taskbar escura"); `virar_A_contorno` passa limpo. Na B o lint avisa "pulo de desenho"
  (37-51% muda) e "área varia" (25-30%) nas trocas perfil ↔ 3/4 ↔ frente: é o corpo girando (de frente ela é
  estreita), e não dá pra fazer em 1 px sem dobrar o número de frames.
- Olhado ampliado e em tamanho real 2x, na taskbar clara e na escura com contorno; comparado com a pose parada e
  com as fotos. 3 rodadas de autocrítica: (1) buracos entre as pernas no 3/4 e na pata levantada → pata de longe
  1 px mais pra direita e pata da frente dobrando pra trás; (2) toco do pescoço sobrando atrás da cabeça no
  3/4 esquerdo → pescoço do 3/4 mais estreito; tronco 3/4 recentrado (girava em volta da frente, o bumbum pulava 4 px);
  (3) pata no alto de frente parecia só "perna curta" → dedos virados pra dentro (punho dobrado).

## 5. Pro app (quando aprovar)

- O piscar não tem remendo pras cabeças novas (de frente tem 2 olhos; olhando pra trás o olho é espelhado): durante
  o virar, `olho = null` (sem piscar). Na A dá pra piscar no pico com o remendo espelhado se ele quiser.
- B termina na `parada_esquerda`; depois dela o estado segue com as animações `_esquerda`.

## 6. Perguntas pro dono

1. A, B, ou as duas (A como "olhadinha" quando algo acontece atrás, B pra dar meia-volta na ponta da barra)?
2. A cara de frente parece a Kiki? (orelhas, grisalho, olhos, nariz). É a peça mais nova de identidade.
3. Tempo: o pico da A (700 ms olhando pra trás) e o "olhou pra gente" da B (260 ms) estão bons, mais curtos ou mais longos?
4. De frente: corpo mais estreito assim ou um pouco mais largo/robusto? Patas de trás escondidas ou aparecendo?
5. Ele prefere que a meia-volta passe de frente pra gente (B) ou de costas (ver o bumbum, girando pro outro lado)?

## 7. Rodada 2 (feedback do dono, 15/10)

Feedback: (1) "a pata que levanta é a outra da frente, na parada" e (2) "quando ela girar o corpo todo, as patas meio
que todas colaboram, né? não só uma". Arquivos novos (as v1 continuam como estavam): receitas `anims/virar_A2.json`
e `anims/virar_B2.json`; peças `legs_virar2A_p1/_p2`, `legs_virar2_34_passo`, `legs_virar2_34esq_passo`,
`legs_virar2_esq_passo`. Cabeças e troncos são os mesmos da v1, inclusive a cabeça de frente.

**Por que a pata de perto (o dono tem razão).** O raciocínio da v1 olhava só pra onde o peso vai depois que a cabeça
virou. Parada, o cachorro faz o contrário primeiro: joga o peso na pata de fora (a esquerda dela, a de longe) pra
DESCARREGAR a pata do lado pra onde vai olhar ou andar, e essa pata de dentro (a direita dela, a de perto, a do lado
da tela) levanta, como quem prepara o primeiro passo naquela direção. É o mesmo que a gente faz pra dar um passo
de lado: o peso vai pro outro pé e o pé do lado do passo sobe.

**A2: olhar pra trás, 6 frames, 300 / 100 / 110 / 700 / 100 / 100 ms (1,41 s).** Igual à A, só muda a pata:
f0 todas no chão; f1 só a cabeça (3/4); f2 pata da frente de perto (direita) 1 px; f3 a mesma pata 2 px, punho
dobrado, olhando pra trás; f4 1 px; f5 no chão.

**B2: meia-volta com passinhos das 4 patas, 8 frames, 300 / 100 / 110 / 260 / 100 / 110 / 100 / 300 ms (1,38 s).**
Cada pata sobe 1-2 px e pousa no lugar novo, uma depois da outra, na ordem de um passo lento (frente direita →
lado esquerdo → traseira direita → traseira esquerda), sempre 1 px por frame em cada pata:

| frame | ms | cabeça / corpo | pata no ar (px) |
|---|---|---|---|
| f0 | 300 | perfil / perfil | nenhuma |
| f1 | 100 | 3/4 / perfil | frente DIREITA (de perto) 1: o primeiro passo, pro lado do giro |
| f2 | 110 | frente / 3/4 | frente direita pousa; frente ESQUERDA 1 + traseira ESQUERDA 1 (as duas de longe, o lado de fora da curva dá o passo junto, como no andar) |
| f3 | 260 | frente / frente | frente esquerda 2 (lado direito da tela); traseiras escondidas atrás |
| f4 | 100 | 3/4 esq. / frente | frente esquerda 1 (descendo) |
| f5 | 110 | perfil esq. / 3/4 esq. | frente esquerda pousa; traseira DIREITA 1 (a de longe no 3/4 esquerdo) |
| f6 | 100 | perfil esq. / perfil esq. | traseira direita pousa; traseira ESQUERDA 1 (a de perto): o último passinho, o bumbum assenta |
| f7 | 300 | perfil esq. / perfil esq. | nenhuma |

A traseira esquerda dá dois passos (f2 e f6) porque é a que mais anda: o bumbum vai da esquerda da tela pra direita.
Na vista de frente as traseiras ficam escondidas atrás das dianteiras (o passo delas aparece no 3/4 e no perfil).

**Conferências:** `problems()` sem buraco nem pixel solto (normal e esquerda); lint: paleta ok, patas na linha 31,
A2 contorno limpo; B2 com os mesmos avisos de "pulo de desenho" da v1 (troca de vista do corpo). f0 = `parada` e
f7 = `parada_esquerda` pixel a pixel. Prévia: `quadro.png` (A antes/depois, B antes/depois) e `spritemap.png` da v2.

**Perguntas:** os passinhos de 1 px ficaram visíveis o bastante no tamanho real, ou subir 2 px nas traseiras? Na
vista de frente, mostrar as traseiras dando o passo atrás das dianteiras?
