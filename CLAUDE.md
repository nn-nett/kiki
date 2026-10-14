# Kiara Pixel Pal 🐕

Mascote virtual em pixel art da Kiara — Pinscher fêmea, 12 anos, pelagem preta
com marcações castanhas (tan), orelhas em pé, porte pequeno. **Detalhe essencial:
pelos grisalhos/brancos no focinho, ao redor dos olhos e espalhados pelo rosto**
(ela é idosa). Vive na taskbar do Windows 11 e num overlay no Android.

## Sprites prontos pra implementação (leia primeiro se for mexer no app)

O dono vai implementar o app (Fase 1) em outra sessão com o que já está aprovado; a Fase 0
(sprites) continua em paralelo e os novos aprovados entram no mesmo lugar, no mesmo formato.

- **Tudo pronto fica em `sprites/final/`** — guia completo em **`sprites/final/README.md`**
  (formato do JSON, `step_px`, variantes, regras de desenho na tela).
  - `kiara-sprites.png` (folha 32x32 por célula) + `kiara-sprites.json` (frames, durações, loop, passo).
  - `frames/<anim>/` com os PNGs soltos.
- **Aprovadas hoje:** `parada`, `andando` (trote, 1 px/frame) e `latindo` (com tranco). Cada uma em 4
  versões: normal, `_esquerda`, `_contorno` (taskbar escura) e `_contorno_esquerda`.
- **Ver tudo animado:** Galeria https://claude.ai/artifact/Cg5sdrUGvrXio7Wn9rx6oe
- **Comportamento de referência:** simulação https://claude.ai/artifact/GmRRzGRh512wQHAbToic6Y
  (`sprites/tools/sim_template.html`, objeto `BRAIN`).
- **Ainda não aprovados** (não usar como final): correndo, dormindo (+ travesseiro), piscar, ofegante, transições.
- Pra regenerar os finais: `python3 sprites/tools/export_final.py` (lê `sprites/final/aprovadas.json`).

## Estado do projeto

- **Fase atual: Fase 0 — Sprites** (em andamento, nova tentativa — ver `sprites/PLANO.md`)
- Fotos reais em `./reference/` (16 fotos, incluindo perfil com o potinho, incluindo câmera noturna, peitoral teal,
  suéter listrado, dormindo enrolada, deitada lambendo e de cima com bandana vermelha)
- Paleta v2 em `sprites/palette.json` — cores extraídas das fotos por amostragem.
- **Rabo confirmado: toquinho curto, preto, reto ou pra cima** (foto da bandana).
  Abanar = toquinho mexe 1px + bumbum balança.
- **Tamanho único: 32x32** (~11 cores da cachorra: X K k D T t G W E B N; objetos têm cores próprias).
  Poses com objeto (travesseiro) usam quadro mais largo (44x32). O dono descartou o 64
  e achou o 16 e o 8 fracos ("só 32"). Ampliado 2x quando precisar de mais tamanho.
- **Contorno grisalho (G)**: aprovado, mas o dono pediu pra trabalhar **sem contorno por
  enquanto** (previews e revisões sem borda). Continua disponível por filtro
  (`filters.py outline color=G`) pra saída final.
- **Pose base: em pé, de lado** (substitui a sentada).
- **Pose base APROVADA: `sprites/base/kiara_32.txt`** (e `_contorno.png`). Caminho:
  rascunho C2 (Canva) → retoque mínimo → olho castanho → testa preta → sobrancelha
  cinza na ponta (opção 3) → buracos fechados. Histórico em `sprites/candidates/base/`.
- No app, a janela deve andar ~1px do sprite por frame (as patas plantadas recuam
  1px/frame) pra não patinar; esquerda por espelho.
- Potinho (da foto `reference/kiki_perfil_potinho.jpg`): ração num pote baixo de cerâmica
  bege-claro (pedra) e água numa vasilha escura (berinjela) — a paleta ainda está
  terracota e precisa ser ajustada na etapa "comendo".
- **Proporção P1 aprovada** (pernas +1 px, corpo +2 px; `tools/proportion.py`): já
  aplicada em `sprites/base/kiara_32.txt` e nas peças `sprites/parts/32/`.
- Andar refeito com a perna inteira articulada (dianteira: ombro, cotovelo, pata;
  traseira: glúteo, joelho/jarrete, pata), sobre a P1: trote A (4 frames, `walk_a.json`)
  e trote B (6 frames de 100 ms, `walk_b.json`, preferido pelo juiz Haiku). **O dono
  gostou do trote B** ("o trote b tá ótimo"). O `walk.json` antigo (só patinhas) foi reprovado.
- Barriga (pedidos do dono): **2 px mais funda**, toda preta, reta, com borda X embaixo
  (como as pernas), nas faixas de pernas (`legs_base`, `legs_trotB0-5`) e na pose base.
  A pele mais clara no ventre (cor `p`) foi reprovada e saiu da paleta; a curva junto da
  coxa deixava um buraco e foi fechada. Histórico em `sprites/candidates/barriga/`.
- Ajustes finos (`sprites/candidates/ajustes/`): peito 1 px mais fundo e com a frente
  maior (a barriga tinha ficado maior que o peito); orelha direita sem o pixel solto na
  ponta e com borda dos dois lados (opção B; a A, mais fina, ficou no quadro); castanho
  do alto da pata de trás de longe virou preto (fica atrás da barriga).
- **Toquinho APROVADO: 1 px mais alto** (opção r1, 3 px de altura; "agora sim o rabinho
  tá perfeito"), já em `parts/32/upper.txt` e na pose base. Outras opções em
  `sprites/candidates/rabo/`.
- **Andando APROVADO** ("já temos frames pra Kiki andando"): trote B (`anims/walk_b.json`)
  com P1, barriga +2 px, peito mais fundo, rabinho +1 px. Previews em `sprites/previews/andando/`.
- **Arquivos finais aprovados em `sprites/final/`**: a lista `aprovadas.json` diz quais
  receitas estão aprovadas; `python3 sprites/tools/export_final.py` gera `final/frames/<anim>/`
  (normal, esquerda, contorno, contorno_esquerda) e `final/kiara-sprites.png/.json` (células
  32x32, durações, loop, `step_px` = px do sprite que a janela anda por frame, frames no ar).
  Hoje: parada + andando + latindo. Aprovou uma animação nova → adicionar em `aprovadas.json` e rodar.
- **Cabeça separada** (pro latido e futuras expressões): `head.txt` (linhas 0-14, cols 16-31,
  `@anchor 4,14`) + `torso.txt` (`@socket.pescoco 20,14`, com toco do pescoço escondido). `stand_head`
  = `stand` pixel a pixel. Pra migrar uma receita: `upper` → `torso` e `head` com
  `attach: "torso.pescoco"`. A cabeça tem `@role cabeca` (o suéter não pega nela).
- **Galeria da Kiara (tudo o que já foi aprovado): https://claude.ai/artifact/Cg5sdrUGvrXio7Wn9rx6oe**
  — pedido do dono: mostrar sempre, "pra garantirmos que não estamos perdendo as coisas". Lê só os
  arquivos finais (`final/kiara-sprites.png/.json` + `aprovadas.json`) e o checklist deste arquivo.
  `export_final.py` refaz `sprites/final/galeria.html` (`tools/gallery.py`); depois de cada aprovação,
  republicar o artifact com esse mesmo arquivo e mandar o link pro dono.
- Página animada de comparação: https://claude.ai/artifact/8mDaYnhGo8hGKTrh5hvmm1
- **Simulação "Kiara na taskbar"** (pedido do dono: andando e latindo ao acaso):
  https://claude.ai/artifact/GmRRzGRh512wQHAbToic6Y — `tools/sim_page.py` + `sim_template.html`
  (cópia em `sprites/previews/simulacao/`). Monta os frames por camadas (pernas, tronco,
  cabeça; conferido pixel a pixel contra o rig), então ela late andando sem frames novos.
  O "cérebro" (estados, chances e tempos) é um rascunho pra Fase 1. Usa as animações aprovadas e,
  marcadas como teste (cada uma com caixa pra desligar): a corrida (`sim_page.py --run run`), o
  ofegante (depois de correr: parada ofegante ou andando ofegante) e o piscar (sozinho a cada 2,5-7 s,
  por cima de qualquer estado; o remendo cai em `eyePos[cabeça][olho]`). Tudo conferido pixel a pixel.

### Observações de anatomia (das fotos)

- Orelhas MUITO grandes, pontudas e abertas (quase de morcego) — marca registrada.
- Focinho fino; grisalho denso no focinho, queixo, sobrancelhas e ao redor dos
  olhos; pelos brancos salpicados pela cabeça.
- Tan: bochechas, sobrancelhas (pontinhos), garganta, peito (com mancha clara
  cremosa no centro), pernas e patas.
- Olhos castanhos (o dono corrigiu: nada de catarata/névoa azulada; o azulado das
  fotos é reflexo). Cor E #4a2c1e com 1 pixel de brilho B.
- Corpo compacto e robusto, pernas finas.
- Usa às vezes bandana/coleira vermelha (fotos), peitoral teal no passeio.

## Próximos passos (to-dos do dono)

- **Frames de transição entre estados** (pedido pra "amanhã", 14/10): parado → andando,
  andando → correndo, correndo → andando, andando → parado, parado → latindo etc. Ideia: 1-3 frames
  curtos por transição (ex.: pata levantando antes do primeiro passo, corpo inclinando antes do
  galope, freada com o corpo pra trás), montados no rig com as peças que já existem quando der, e
  a simulação passa a tocar a transição entre um estado e outro.
- Galope: o dono está "entre a v3 e a v4" e pediu a **cabeça de corrida** (orelhas deitadas pra trás,
  cabeça mais alinhada com o corpo). Corrigida a pedido dele ("mudou o tamanho do focinho", "cadê o
  pescoço"): rosto idêntico à `head.txt` (só as orelhas mudam), pescoço visível, cabeça só 3 px abaixo
  da pose parada (`parts/32/head_run.txt`). Duas opções: v4 + cabeça (`anims/run.json`) e v3 + cabeça
  (`anims/run_v3c.json`, peças em `sprites/candidates/correndo_v3c/parts/`, ver README lá).
  O dono escolheu a **v4 com essa orelha** e pediu cabeça mais baixa e pescoço mais longo: opções
  "agora" (desce 3), **A** (desce 4, `anims/run_pescoco_A.json`) e **B** (desce 5, `run_pescoco_B.json`),
  com troncos `torso_run_*_A/_B.txt`; esperando a escolha (ver `run_log.md`).
- Kiki dormindo — **4 opções de frame pra validar**: A (de barriga) e B (enrolada), 32x32, e com o
  **travesseiro** que o dono sugeriu ("ela precisa de um travesseiro pra subir e dormir"): C (corpo no
  chão, peito/cabeça/pata apoiados no travesseiro) e D (inteira em cima, cabeça na beirada), quadro 44x32.
  Peças `parts/32/dormir_A-D.txt` + `travesseiro.txt` (24x8, `@role objeto`, cores novas Q/q/Z no grupo
  `travesseiro` da paleta, tiradas das fotos); receitas `anims/dormir_A-D.json`; log `dormir_log.md`;
  fotos novas `reference/kiki_dormindo_*.jpg`. Depois da escolha: respiração (2-3 frames) e a
  transição "subir no travesseiro" (plano no log).

- **Expressões desacopladas** (ideia do dono) — **piscar e ofegante prontos pra aprovação**:
  prévia https://claude.ai/artifact/NwRJaKgDuVaZGukfRDMjxw (cópia em `sprites/previews/expressoes/`).
  - Piscar: remendos `olho_meio`/`olho_fechado` (`@anchor 1,0`, vindos do olho fechado do dormir) que
    encaixam em `@socket.olho` de qualquer cabeça (7,9 em head/head_bark1/2/head_ofegante; 12,7 em
    head_run). Receita `anims/piscar.json` (aberto 1,5 s, meio 60, fechado 110, meio 60).
  - Ofegante: `head_ofegante1/2` (boca entreaberta como no latido, língua rosa P pendurada que desce 1 px
    na expiração; o peito desce 1 px). `anims/ofegante.json` (2×130 ms) e `anims/andar_ofegante.json`
    (trote B + cabeça ofegante). Log em `parts/32/expressoes_log.md`.
  - Perguntas abertas do desenhista: ritmo (130 ms ofegante de quem correu ou 180-200 ms mais calmo);
    "cara relaxada" = ofegante + olho meio fechado.
  - Depois: o export final passa a ter camadas (corpo sem cabeça + âncora da cabeça por frame +
    cabeças/olhos por expressão) pro app compor.

## Fases

1. **Fase 0 — Sprites**: spritesheet 32x32 gerado programaticamente (Python +
   Pillow), fluxo iterativo: cada sprite só avança com aprovação visual do dono.
2. **Fase 1 — Desktop**: Electron, janela transparente sobre a taskbar do
   Windows 11, 2 monitores, máquina de estados autônoma, potinho, modo passeio,
   tray.
3. **Fase 2 — Android**: Kotlin, foreground service + overlay no topo da tela.

**Regra de ouro: trabalhar uma fase por vez; nunca avançar sem aprovação
explícita do dono. Na Fase 0, NUNCA avançar um sprite sem aprovação visual.**

## Fase 0 — checklist de sprites

Cada item: gerar em 32x32, fundo transparente → folha de revisão → mostrar → iterar →
só marcar como ✅ com aprovação explícita.

- [x] ✅ Pose base (em pé, vista lateral, 32x32) — `sprites/base/kiara_32.txt`
- [x] ✅ Andando — trote B, 6 frames de 100 ms, esquerda por espelho (`anims/walk_b.json`)
- [ ] Correndo — v1 reprovada ("faltou o tronco inclinar"); v2 inclinou o tronco; v3 acertou pernas e
  toquinho na coluna (+ bumbum arredondado no último frame); **v4 pra aprovação**, guiada pela referência
  de pixel art do dono: corpo de 19 (bola, costas arqueadas) a 24 colunas (esticado), pernas curtas embaixo
  do corpo, cabeça baixa no compacto/alta no esticado, bumbum arredondado em todos os frames; tronco por pose
  `torso_run_*`, 6×70 ms, 2 px/frame (`anims/run.json`, `legs_run0-5`, `run_log.md`). Na simulação como teste.
- [x] ✅ Latindo — `anims/latir_tranco.json` (o dono escolheu "com tranco"; queixo do AU! afinado a pedido
  dele; confirmado: "o latido com tranco tá perfeito")
- [ ] Sentada/idle (2–3 frames, respiração + piscar)
- [ ] Dormindo (2–3 frames, "zZz" opcional)
- [ ] Comendo (3–4 frames, no potinho)
- [ ] Saltando (3–4 frames, esquerda/direita)
- [ ] Reação ao toque (3–4 frames, pulinho + rabo abanando)
- [ ] Modo câmera noturna 👁️👁️ (2–3 frames, silhueta + olhos brancos com glow)
- [ ] Passeando de coleira (4–6 frames, peitoral teal + guia preta/amarela diagonal)
- [ ] Fazendo cocô (3–4 frames)
- [ ] Objeto: potinho de ração (~24x16, cheio/vazio)
- [ ] Objeto: cocô (~8x8, com brilho de "fresquinho")
- [ ] Skin: suéter preto com listras brancas (variante/overlay de todos os corpos)
- [ ] Saída final: `kiara-sprites.png` + JSON de metadados (frames, durações, loops) —
  já sai parcial em `sprites/final/` a cada aprovação (`tools/export_final.py`)

## Decisões técnicas

- **Estratégia de produção (sessão 2, plano completo em `sprites/PLANO.md`)**:
  "boneco articulado" — peças desenhadas uma vez (cabeça, tronco, pernas, rabo) e
  montadas por receita (`tools/rig.py`), sem rotação; noturna, suéter, espelho e
  passeio saem por filtro (`tools/filters.py`). Ponto de partida escolhido num
  bake-off de rotas (A Claude desenha, B foto→pixels, C Canva, D Figma AI, E pixel a
  pixel com juiz). A estratégia antiga de adaptar o sheet de husky foi abandonada
  (opengameart segue bloqueado na rede do sandbox).
- **Papéis dos modelos**: Opus (sessão principal) = diretor de arte, código central,
  decisões e conversa com o dono; Sonnet (subagentes) = desenhista e scripts de rotina;
  Haiku (subagentes) = juiz rápido A/B e conferências frame a frame.
- Ferramentas em `sprites/tools/` (base comum em `common.py`): `rig.py`, `filters.py`,
  `lint.py` (paleta, pés no chão, contraste com a taskbar), `review.py` (folha com
  grade e foto), `compare.py` (A/B pro juiz), `similarity.py` (nota 0–100 vs. foto),
  `normalize.py` (imagem de IA → sprite, via `unfake`), `photo2sprite.py` (rota B em
  qualquer tamanho), `tiers_board.py` (quadro 8/16/32), `animate.py`, `pack.py`,
  `spritegen.py`, `recolor.py`, `sheet_extract.py`, `tweak.py` (ajuste fino de pixels com
  variantes, checagem de buracos/entalhes e aplicação), `preview_html.py` (HTML offline),
  `page.py` + `page_template.html` (página animada do artifact), `export_final.py`.
  Dependências: `sprites/requirements.txt`.
- **Skill do projeto `ajuste-sprite`** (`.claude/skills/ajuste-sprite/SKILL.md`): o ciclo
  localizar → variantes → mostrar → aplicar → salvar, com as lições do dono (bordas X,
  perna de longe atrás da barriga, sem pixel solto). Usar sempre que ele apontar um detalhe.
- Rede do sandbox: Figma e Canva geram, mas o download em resolução cheia e o upload
  de fotos são bloqueados; as miniaturas (200–256 px) bastam para 64x64.
- Pipeline validado de ponta a ponta com sprites do FF1 (Black Mage) enviados
  pelo dono — material Square Enix, só teste local, fora do git (.gitignore).
- Sprites sem anti-aliasing; matrizes de caracteres (`.txt`) continuam sendo o
  formato editável de tudo.
- Skin do suéter: overlay automático por filtro sobre a peça do tronco.
- Contorno pra taskbar escura: G (contraste 5,4) — aprovado pelo dono.

## Estrutura

```
reference/   # fotos reais da Kiara (o dono coloca)
sprites/     # paleta, matrizes dos sprites, scripts de geração, previews
desktop/     # Fase 1 (Electron) — ainda não iniciada
android/     # Fase 2 (Kotlin) — ainda não iniciada
```

## Regras de trabalho

- Commits pequenos e frequentes, mensagens claras.
- O dono é iniciante em desenvolvimento: explicar decisões técnicas de forma
  simples.
- Atualizar este arquivo a cada sessão (estado, fase, decisões).
