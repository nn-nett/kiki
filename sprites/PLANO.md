# Plano — Sprites da Kiara, nova tentativa (Fase 0)

## Contexto

Na tentativa anterior chegamos a uma pose sentada 24x24 (`sprites/frames/sit_base.txt`)
e montamos um pipeline em `sprites/tools/`, mas nenhum sprite foi aprovado. O que travou:

1. **Desenho às cegas, frame a frame.** Cada frame era redesenhado do zero numa matriz
   de texto, então a anatomia mudava de um frame pro outro. Animação exige o contrário:
   a mesma Kiara em todos os frames.
2. **Dependência de download manual.** A estratégia "adaptar o sheet de husky" esbarrou
   na rede: o opengameart continua bloqueado (testei hoje: 403).
3. **Você virou o detector de erros.** Os sprites chegavam até você sem uma checagem
   visual rigorosa antes.

**Objetivo:** usar os modelos de um jeito mais esperto. Eles enxergam imagens (comparam o
sprite com as fotos), escrevem código bom (montam animação por regra, sem redesenhar) e
seguram um ciclo de autocrítica antes de te mostrar qualquer coisa. Resultado final:
`kiara-sprites.png` + JSON de animações, com cada sprite aprovado por você.

**Decisões já tomadas com você nesta sessão:**
- Rabo: **toquinho curto, reto ou pra cima** (confirmado também na foto `78cd3897`).
  Abanar = toquinho mexe 1px + bumbum balança.
- Pose base: **em pé, de lado** (substitui a sentada como base).
- Ponto de partida: **testar todas as rotas** (Claude desenhando, foto→pixels, Canva,
  Figma, pixel a pixel com feedback), juntar, avaliar e escolher a melhor (ou combinar as
  melhores partes).
- Modelos: **Opus, Sonnet e Haiku 5.5 com papéis fixos** (tabela abaixo), usados como
  subagentes.

## A ideia central: "boneco articulado" em vez de desenhar cada frame

Em vez de desenhar ~45 frames, desenho **~12–15 peças uma única vez** (cabeça, tronco,
pernas, rabo) e um script monta os frames encaixando as peças e deslocando 1px aqui e ali.
A cabeça é literalmente a mesma em todos os frames, então a consistência vem de graça.

Várias animações do checklist viram **filtros automáticos**, sem desenho novo:

| Item do checklist | Como sai |
|---|---|
| Esquerda/direita | espelhamento automático |
| Piscar / respirar | troca só a peça do olho / tronco sobe 1px |
| Câmera noturna 👁️👁️ | filtro: corpo vira silhueta `S/s`, olhos viram `O` + glow `o` |
| Suéter listrado | filtro: listras `U/u` aplicadas nos pixels do tronco (resolve "overlay vs variante": vira overlay automático) |
| Passeio de coleira | camada do peitoral `H` + guia `L/Y` por cima do "andando" |

Canvas nativo de **24x24**, exibido a **2x (48px)** na taskbar, sem suavização (igual hoje).

## Regras de pixel art (da pesquisa na web, out/2026)

Viram regra no código (`rig.py`/`lint.py`) e no checklist de revisão:

- **Silhueta primeiro**: reconhecível só pelo contorno; na Kiara, as orelhas enormes são a silhueta.
- **Testar no tamanho real** (48px na taskbar), não só ampliado.
- **Contorno opcional** pra destacar em qualquer fundo (`filters.py outline`/`rim`), decidido
  pelo teste de contraste com a taskbar escura.
- **Nunca girar peça**: abaixo de 24x24 rotação destrói a grade. O rig só desloca (1px) ou
  troca a peça. `rig.py` nem tem opção de rotação.
- **Animação mínima**: pernas mexem 1–2px; 2–4 frames por ciclo; ordem ping-pong
  1-2-3-4-3-2 pra parecer mais frames.
- **Cachorro não anda como gente**: pata traseira ~meio passo defasada da dianteira.
- **Caricatura de mascote**: cabeça levemente maior que o real.
- **Paleta única** pra tudo (`palette.json`).

## Quem faz o quê: Opus, Sonnet e Haiku (todos 5.5)

A regra: **trabalho repetitivo vai pro modelo mais barato que dá conta, decisão de gosto
fica com o mais forte.** A sessão principal (esta, com você) é o Opus; Sonnet e Haiku
entram como subagentes, cada um numa pasta própria (`sprites/candidates/<rota>/`) pra
ninguém pisar no trabalho do outro. Só a sessão principal faz commit.

| Modelo | Papel | Quando entra | Quando NÃO usar |
|---|---|---|---|
| **Opus 5.5** (sessão principal) | Diretor de arte e orquestrador | Conversar com você; escrever o código central (`common.py`, `rig.py`); dar os prompts das IAs de imagem (rotas C/D); decidir o vencedor do bake-off; desenhar/ajustar a **cabeça** (é a identidade dela: orelhas, grisalho, olho); revisão final antes de qualquer coisa chegar no painel; commits | Loops repetitivos de muitas rodadas (caro e lento) |
| **Sonnet 5.5** (subagentes) | Desenhista | Rota A (2 variantes em paralelo: "chunky" e "esguia"); rota E, o loop pixel a pixel; peças novas das etapas 2–8 (tronco sentado, deitada, agachada…); receitas de animação; scripts de rotina (`lint.py`, `review.py`, `normalize.py`, `filters.py`) a partir de uma especificação minha; crítico independente do bake-off (um agente que só recebe as fotos e os candidatos, sem saber quem desenhou) | Decidir sozinho o que vai pro painel |
| **Haiku 5.5** (subagentes) | Juiz rápido e conferente | Pergunta A/B no loop pixel a pixel ("qual das duas parece mais com a foto, neste ponto: orelha?"); 3 juízes votando nos pares do bake-off; conferir consistência frame a frame ("é a mesma cachorra? o pé escorregou?"); checar cada frame derivado (noturna, suéter, passeio); validar o JSON final | Julgamento estético aberto ("está bonito?") — só perguntas fechadas, comparando duas imagens |

Pergunta fechada A/B é onde um modelo rápido acerta com consistência, por isso o Haiku
sempre recebe duas imagens e um critério só. Gosto e anatomia geral ficam com Sonnet/Opus.

## Etapas

Cada etapa termina com: commit pequeno + `CLAUDE.md` atualizado + push em
`claude/charming-gates-tf2lki`. **Nenhum sprite avança sem sua aprovação visual.**

### Etapa 0 — Ferramentas (não precisa de aprovação de sprite)

Novos scripts em `sprites/tools/`, reaproveitando o que já existe:

- `rig.py`: lê peças (`sprites/parts/*.txt`) e receitas de animação (`sprites/anims/*.json`)
  e gera os frames PNG. Cada peça é uma matriz no formato atual do `spritegen.py`, com
  cabeçalho de encaixe (`# @anchor x,y`, `# @socket pescoco x,y`). Reusa `load_palette`/
  `parse_matrix` de `spritegen.py` (vou extrair essas duas funções pra um `common.py`,
  já que hoje estão copiadas em 4 scripts).
- `filters.py`: espelhar, noturna, suéter, peitoral+guia.
- `lint.py`: checagens objetivas que rodam em todo frame:
  só cores da paleta; fundo transparente; pés na mesma linha em todos os frames de uma
  animação (sem "escorregar"); tamanho certo; nenhum frame muito diferente do vizinho
  (pega "pulos" de desenho); **contraste contra a taskbar escura e clara do Windows 11**.
  Esse último importa: cachorra preta em taskbar escura some. Se falhar, a solução é um
  contorno/brilho de borda com `k` (preto azulado).
- `review.py`: monta a "folha de revisão", que é o que eu olho antes de te mostrar:
  sprite a 1x, 2x e 8x com grade e coordenadas; ao lado, o recorte da foto real na mesma
  escala; frames lado a lado; e sobre fundos de taskbar escura/clara.
- `similarity.py`: o "olho automático" do loop pixel a pixel. Recorta a Kiara da foto
  lateral (`78cd3897`, espelhada pra olhar à direita), troca peitoral/saia por preto, gera
  a silhueta-alvo e o mapa de cores por região em 24px. Dá uma nota de 0 a 100 pra
  qualquer sprite: quanto a silhueta bate (sobreposição) + quanto as cores de cada região
  batem (tan onde é tan, grisalho onde é grisalho). Roda em milissegundos, então pode
  rodar a cada pixel.
- `compare.py`: gera a imagem A/B (antes | depois | foto) que vai pro juiz Haiku.
- `normalize.py`: **wrapper fino do `unfake`** (biblioteca pronta, instalada via pip) em vez
  de escrever do zero. O `unfake` detecta o tamanho do "pixelão" da imagem de IA, alinha
  na grade e reduz; o wrapper passa a **paleta fixa da Kiara**, tira o fundo, encaixa em
  24x24 com pés na última linha e grava matriz `.txt` + PNG. Dependências em
  `sprites/requirements.txt` (Pillow, unfake).
- Reusar sem mudar: `animate.py` (GIF), `pack.py` (sheet final + JSON), `photo2matrix.py`
  (rota B), `sheet_extract.py`/`recolor.py`.
- **Painel de aprovação** (página privada no claude.ai, abre no celular): cada animação
  tocando em tamanho real numa taskbar falsa (escura e clara), botões
  "aprovar" / "pedir ajuste" + campo de comentário que eu leio direto daqui. O player da
  página lê o mesmo sheet + JSON que o app desktop vai ler, então de quebra testa o formato.

### Etapa 1 — Pose base em pé: "bake-off" de rotas

Gerar candidatos por todas as rotas, normalizar todos pro mesmo formato e comparar:

| Rota | Como | Observação |
|---|---|---|
| A — Claude desenhista | desenho as peças direto, olhando as fotos `78cd3897` (lateral), `d380ab7d` e `3e38dc34` (orelhas/rosto); 3–4 rodadas de autocrítica | sem custo extra |
| B — Foto → pixels | `photo2matrix.py` no recorte da foto lateral, sem fundo, reduzido a 24px e quantizado na paleta | proporções fiéis, precisa de limpeza |
| C — Canva (imagem→imagem) | sobe a foto lateral e pede "sprite pixel art 16-bit, vista lateral, cores chapadas"; 2–3 variações | manda a foto pro Canva (você autorizou) |
| D — Figma (texto→imagem) | descrição detalhada da anatomia; 1 imagem em `gpt-image-2.5` e 1 em `gemini-3.1-flash-image` | gasta créditos de IA do Figma (plano "Nilson de Moura Netto's team", o único da conta) |
| E — Pixel a pixel com feedback | thread própria, descrita abaixo | Sonnet desenha, Haiku julga |
| F — PixelLab (opcional) | gerador feito pra pixel art, com MCP oficial pro Claude Code; cria personagem e anima andar/parado | só se você criar conta e me passar a chave; testo antes se a rede deixa passar |
| G — Retro Diffusion (opcional) | gerador com grade de pixel de verdade, anima | idem: conta paga + chave + teste de rede |

F e G não bloqueiam nada: o bake-off roda com A–E, e F/G entram se a conta aparecer.

**Rota E — desenho pixel a pixel (a "outra thread").** Um subagente Sonnet desenha a
Kiara do zero, um pixel por vez, e depois de cada passo "tira foto" e confere com a
referência. Ordem de desenho: contorno da silhueta → preenchimento do corpo → orelhas →
focinho e grisalho → olho → marcações tan → toquinho do rabo. Três níveis de conferência,
do mais barato ao mais caro:

1. **A cada pixel — `similarity.py`** (código, grátis): se a nota caiu, o pixel volta e
   tenta outra cor/posição. Se subiu ou manteve, fica.
2. **A cada 5–10 pixels — o próprio Sonnet olha** a folha de revisão ao lado da foto
   (é ele "tirando foto e vendo se tá parecido").
3. **Ao fechar cada região (ex.: orelhas) — juiz Haiku**: recebe `compare.py` (antes |
   depois | foto) e responde "melhorou / piorou / igual" pra aquela região. Piorou → a
   região volta pro estado anterior e o Sonnet tenta de novo (máx. 4 tentativas por região).
   Quem faz a ponte sou eu (Opus): o Sonnet pausa ao fechar a região, eu chamo o Haiku e
   devolvo o veredito pro mesmo Sonnet, que continua com o contexto que já tinha.

Por que não olhar a imagem a cada pixel: num sprite de 24x24, um pixel sozinho quase não
muda a figura, então o julgamento visual vira ruído, e seriam ~500 rodadas de visão por
pose. A nota automática cobre o pixel a pixel; a visão entra quando já dá pra ver diferença.
A nota não manda sozinha: pixel art exagera de propósito (orelhas maiores que na foto),
então nas regiões marcadas como "exagero permitido" quem decide é a visão, não a nota.

- **Normalização** (`normalize.py`, via `unfake`): imagem de IA não tem grade de pixel de
  verdade; vira matriz `.txt` 24x24 na paleta da Kiara, como todas as outras.
- **Prompts das rotas C/D** (dicas da pesquisa): "side view", "2d game sprite", "limited
  color palette", fundo liso; o primeiro resultado bom vira referência de estilo dos próximos.
- **Avaliação:** folha com todos os candidatos lado a lado + foto, e nota de 1 a 5 por
  critério: orelhas enormes/pontudas/abertas; focinho fino com grisalho; olho azulado
  `E`; tan nos lugares certos (bochecha, sobrancelha, peito com mancha creme, pernas);
  corpo compacto e pernas finas; toquinho de rabo; legível a 2x nas duas taskbars;
  "parece a Kiara?".
- **Quem avalia:** (1) `similarity.py` dá a nota objetiva de cada candidato; (2) um
  Sonnet crítico, sem saber de que rota veio cada um, preenche a rubrica; (3) três juízes
  Haiku votam em pares ("A ou B parece mais a Kiara?"); (4) Opus junta as três leituras e
  decide.
- **Decisão:** vencedor ou híbrido (ex.: silhueta da rota B + rosto da rota C), redesenhado
  como peças no formato do rig. Te mostro **2–3 finalistas + minha recomendação** no painel.
- Imagens de IA vão para `sprites/concepts/` (as URLs do Figma expiram em 7 dias).
- **Risco:** se a rede bloquear o upload/download do Canva ou do Figma, peço pra você salvar
  e anexar a imagem (como fizemos com o FF1). As rotas A e B não dependem de rede.

### Etapa 2 — Andando (primeira animação do rig, valida a abordagem)
4 poses de passo (contato/passagem), tocadas em ping-pong 1-2-3-4-3-2, pata traseira
meio passo defasada da dianteira, corpo balança 1px, ~130 ms/frame, esquerda/direita
por espelho. → aprovação.

### Etapa 3 — Sentada/idle
Peça nova: tronco sentado. Respiração + piscar. → aprovação.

### Etapa 4 — Dormindo
Peça nova: deitada enrolada. Respiração lenta + "zZz" opcional. → aprovação.

### Etapa 5 — Comendo + potinho
Peças novas: cabeça abaixada + objeto potinho (~24x16, cheio/vazio). → aprovação.

### Etapa 6 — Saltando + reação ao toque
Só recombinação de peças (agacha, estica, aterrissa; pulinho + toquinho abanando). → aprovação.

### Etapa 7 — Derivados automáticos
Câmera noturna, passeio (peitoral teal + guia preta/amarela), suéter em todos os corpos.
Aprovação em lote no painel, mas cada um com botão próprio.

### Etapa 8 — Cocô
Peça nova: agachada + objeto cocô (~8x8, com brilho). → aprovação.

### Etapa 9 — Saída final
`pack.py` gera `kiara-sprites.png` + `kiara-sprites.json`; `lint.py` passando em tudo;
checklist do `CLAUDE.md` todo ✅.

## O ciclo de cada animação (etapas 2–8)

1. **Sonnet** desenha a peça nova (se houver) e escreve a receita da animação.
2. `rig.py` monta os frames → `lint.py` checa as regras objetivas.
3. **Haiku** confere frame a frame em pares ("mesma cachorra?", "pé escorregou?",
   "orelha mudou de tamanho?"). Qualquer "não" volta pro Sonnet com o par problemático.
4. **Opus** olha o GIF + folha de revisão junto com a foto real e corrige o que não bate
   (no máximo ~4 rodadas antes de te mostrar).
5. Só então publico no painel pra você aprovar.

Na Etapa 0, os scripts de rotina (`lint`, `review`, `normalize`, `filters`, `similarity`,
`compare`) saem de subagentes Sonnet em paralelo a partir de uma especificação minha,
enquanto eu escrevo `common.py` e `rig.py`; depois eu reviso o código deles antes do commit.

**Limites de gasto:** rota E com no máximo 4 tentativas por região e ~40 chamadas de juiz
Haiku por pose; rotas C/D com 2 imagens cada. Se algo estourar isso, paro e te pergunto.

## Arquivos

- Já feito (commit `common.py`): funções compartilhadas; `spritegen`, `photo2matrix`,
  `recolor` já importam de lá.
- Novos: `sprites/tools/{rig,filters,lint,review,normalize,similarity,compare}.py`,
  `sprites/requirements.txt`, `sprites/PLANO.md` (cópia deste plano no repo),
  `sprites/parts/*.txt`, `sprites/anims/*.json`, `sprites/concepts/` (imagens de IA),
  `sprites/candidates/<rota>/` (trabalho de cada subagente), `sprites/out/`
- Alterados: `spritegen.py`, `photo2matrix.py`, `recolor.py` (passam a importar de
  `common.py`); `CLAUDE.md` (nova estratégia, rabo confirmado, base em pé, checklist)
- `sprites/frames/sit_base.txt` fica como referência da tentativa anterior.

## Pendências pra você (perguntar na hora certa)
- Cor real do potinho: o `CLAUDE.md` diz "chutei vermelho", mas a paleta está terracota.
  Pergunto na Etapa 5.

## Verificação
- `python3 sprites/tools/lint.py sprites/out/` sem erros em toda etapa.
- `similarity.py` testado antes da rota E: a foto→pixels da rota B tem que tirar nota alta
  e um sprite aleatório, nota baixa (prova que o "olho automático" mede o que deve).
- Cada subagente devolve seu candidato em `sprites/candidates/<rota>/` com PNG + matriz
  `.txt` + log das rodadas (nota antes/depois, veredito do juiz), que eu confiro.
- GIFs de cada animação (`animate.py`) e folha de revisão abertos e conferidos por mim.
- Painel de aprovação: cada animação toca lendo o sheet + JSON reais; seus cliques de
  aprovação/comentário chegam aqui.
- Etapa 9: script de checagem confere que todo frame do JSON cai dentro do PNG e que
  todas as animações do checklist existem.
