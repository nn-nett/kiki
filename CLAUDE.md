# Kiara Pixel Pal 🐕

Mascote virtual em pixel art da Kiara — Pinscher fêmea, 12 anos, pelagem preta
com marcações castanhas (tan), orelhas em pé, porte pequeno. **Detalhe essencial:
pelos grisalhos/brancos no focinho, ao redor dos olhos e espalhados pelo rosto**
(ela é idosa). Vive na taskbar do Windows 11 e num overlay no Android.

## Estado do projeto

- **Fase atual: Fase 0 — Sprites** (em andamento)
- Fotos reais recebidas em `./reference/` (12 fotos, incluindo câmera noturna,
  peitoral teal e suéter listrado)
- Paleta v2 em `sprites/palette.json` — cores extraídas das fotos por amostragem
  de pixels. **Aguardando aprovação da paleta** antes do primeiro sprite.
- Pendências de confirmação com o dono: cor real do potinho (chutei vermelho) e
  formato do rabo (curto/amputado vs. comprido — afeta animação de abanar).

### Observações de anatomia (das fotos)

- Orelhas MUITO grandes, pontudas e abertas (quase de morcego) — marca registrada.
- Focinho fino; grisalho denso no focinho, queixo, sobrancelhas e ao redor dos
  olhos; pelos brancos salpicados pela cabeça.
- Tan: bochechas, sobrancelhas (pontinhos), garganta, peito (com mancha clara
  cremosa no centro), pernas e patas.
- Olhos grandes com leve névoa azulada de idade (catarata senil) — usar a cor
  E #4a4854 em vez de castanho-escuro: detalhe autêntico dela.
- Corpo compacto e robusto, pernas finas.
- Usa às vezes bandana/coleira vermelha (fotos), peitoral teal no passeio.

## Fases

1. **Fase 0 — Sprites**: spritesheet 48x48 gerado programaticamente (Python +
   Pillow), fluxo iterativo: cada sprite só avança com aprovação visual do dono.
2. **Fase 1 — Desktop**: Electron, janela transparente sobre a taskbar do
   Windows 11, 2 monitores, máquina de estados autônoma, potinho, modo passeio,
   tray.
3. **Fase 2 — Android**: Kotlin, foreground service + overlay no topo da tela.

**Regra de ouro: trabalhar uma fase por vez; nunca avançar sem aprovação
explícita do dono. Na Fase 0, NUNCA avançar um sprite sem aprovação visual.**

## Fase 0 — checklist de sprites

Cada item: gerar 48x48 transparente → preview ampliado 8x → mostrar → iterar →
só marcar como ✅ com aprovação explícita.

- [ ] Pose base (sentada, vista lateral) — define a anatomia para todo o resto
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

- **Estratégia de produção (decidida com o dono após iterações)**: adaptar um
  spritesheet de cachorro pronto (CC0, ex. Husky Sprites do OpenGameArt) em vez
  de desenhar do zero — extrair frames, recolorir para a paleta da Kiara e
  ajustar detalhes dela (orelhas grandes, focinho grisalho, rabo curvado).
  O dono baixa e anexa o sheet (rede do sandbox bloqueia sites de assets;
  só GitHub passa).
- Pipeline pronto em `sprites/tools/`: `sheet_extract.py` (recorte + fundo
  transparente + truque NES de cor emparedada), `recolor.py` (mapa de cores →
  paleta), `animate.py` (GIF de preview nearest-neighbor alinhado pela base),
  `pack.py` (spritesheet final + JSON de animações compartilhado desktop/
  Android), `spritegen.py` (matriz de caracteres → PNG, p/ retoques manuais),
  `photo2matrix.py` (foto → matriz, experimental).
- Pipeline validado de ponta a ponta com sprites do FF1 (Black Mage) enviados
  pelo dono — material Square Enix, só teste local, fora do git (.gitignore).
- Resolução nativa pequena (16–24 px) ampliada 2x sem anti-aliasing; matrizes
  de caracteres (`sprites/frames/*.txt`) seguem disponíveis para edição fina.
- Skin do suéter: decisão pendente (overlay vs. variante completa) — escolher a
  mais simples quando a pose base estiver aprovada.

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
