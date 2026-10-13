# Kiara Pixel Pal 🐕

Mascote virtual em pixel art da Kiara — Pinscher fêmea, 12 anos, pelagem preta
com marcações castanhas (tan), orelhas em pé, porte pequeno. **Detalhe essencial:
pelos grisalhos/brancos no focinho, ao redor dos olhos e espalhados pelo rosto**
(ela é idosa). Vive na taskbar do Windows 11 e num overlay no Android.

## Estado do projeto

- **Fase atual: Fase 0 — Sprites** (em andamento, nova tentativa — ver `sprites/PLANO.md`)
- Fotos reais em `./reference/` (16 fotos, incluindo perfil com o potinho, incluindo câmera noturna, peitoral teal,
  suéter listrado, dormindo enrolada, deitada lambendo e de cima com bandana vermelha)
- Paleta v2 em `sprites/palette.json` — cores extraídas das fotos por amostragem.
- **Rabo confirmado: toquinho curto, preto, reto ou pra cima** (foto da bandana).
  Abanar = toquinho mexe 1px + bumbum balança.
- **Tamanho único: 32x32** (~11 cores: X K k D T t G W E B N). O dono descartou o 64
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
- Barriga (pedido do dono): 1 px mais funda, toda preta, em curva (encolhe junto da
  coxa), nas faixas de pernas (`legs_base`, `legs_trotB0-5`) e na pose base. A pele
  mais clara no ventre (cor `p`) foi testada e **reprovada** ("cancela"); saiu da paleta.
  Histórico em `sprites/candidates/barriga/`.
- **Toquinho APROVADO: 1 px mais alto** (opção r1, 3 px de altura; "agora sim o rabinho
  tá perfeito"), já em `parts/32/upper.txt` e na pose base. Outras opções em
  `sprites/candidates/rabo/`.
- **Andando, versão final pra aprovação:** trote B (`anims/walk_b.json`) com P1, barriga
  gordinha e rabinho novo. Previews em `sprites/previews/andando/`
  (`kiara_andando_offline.html` abre offline). Falta só o OK explícito do dono pra marcar ✅.
- Página animada de comparação: https://claude.ai/artifact/8mDaYnhGo8hGKTrh5hvmm1

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
- [ ] Andando (4–6 frames, esquerda/direita)
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
- [ ] Saída final: `kiara-sprites.png` + JSON de metadados (frames, durações, loops)

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
  `spritegen.py`, `recolor.py`, `sheet_extract.py`. Dependências: `sprites/requirements.txt`.
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
