# Kiara Pixel Pal 🐕

Mascote virtual em pixel art da Kiara — Pinscher fêmea, 12 anos, pelagem preta
com marcações castanhas (tan), orelhas em pé, porte pequeno. **Detalhe essencial:
pelos grisalhos/brancos no focinho, ao redor dos olhos e espalhados pelo rosto**
(ela é idosa). Vive na taskbar do Windows 11 e num overlay no Android.

## Estado do projeto

- **Fase atual: Fase 0 — Sprites** (em andamento, nova tentativa — ver `sprites/PLANO.md`)
- Fotos reais em `./reference/` (15 fotos, incluindo câmera noturna, peitoral teal,
  suéter listrado, dormindo enrolada, deitada lambendo e de cima com bandana vermelha)
- Paleta v2 em `sprites/palette.json` — cores extraídas das fotos por amostragem.
- **Rabo confirmado: toquinho curto, preto, reto ou pra cima** (foto da bandana).
  Abanar = toquinho mexe 1px + bumbum balança.
- **3 tamanhos, cores sobem junto:** 8x8 (3 cores, ícone), 16x16 (~8) e 32x32 (~11,
  sprite principal). O dono descartou o 64: o 32 é o máximo (ampliado 2x quando
  precisar de mais tamanho).
- **Pose base: em pé, de lado** (substitui a sentada).
- Pose base: o **C2 32x32 com retoque mínimo** é o mais fiel (palavra do dono).
  Olho castanho. Em ajuste: testa (os 2 pontos bege viram cabeça preta, cristinha
  grisalha ou sobrancelha — 5 variações em `candidates/base/C2_32_testa/`).
  16x16 e 8x8 sendo redesenhados à mão a partir do 32.
- Pendência: cor real do potinho (paleta está terracota; perguntar na etapa "comendo").

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

1. **Fase 0 — Sprites**: spritesheets 8/16/32 gerados programaticamente (Python +
   Pillow), fluxo iterativo: cada sprite só avança com aprovação visual do dono.
2. **Fase 1 — Desktop**: Electron, janela transparente sobre a taskbar do
   Windows 11, 2 monitores, máquina de estados autônoma, potinho, modo passeio,
   tray.
3. **Fase 2 — Android**: Kotlin, foreground service + overlay no topo da tela.

**Regra de ouro: trabalhar uma fase por vez; nunca avançar sem aprovação
explícita do dono. Na Fase 0, NUNCA avançar um sprite sem aprovação visual.**

## Fase 0 — checklist de sprites

Cada item: gerar nos 3 tamanhos (32, 16, 8), fundo transparente → folha de revisão → mostrar → iterar →
só marcar como ✅ com aprovação explícita.

- [ ] Pose base (em pé, vista lateral) — define a anatomia para todo o resto (32 → 16 → 8)
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
- Contorno pra taskbar escura: candidato G (contraste 5,4); decidir com o dono.

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
