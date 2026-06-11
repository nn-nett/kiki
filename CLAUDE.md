# Kiara Pixel Pal 🐕

Mascote virtual em pixel art da Kiara — Pinscher fêmea, 12 anos, pelagem preta
com marcações castanhas (tan), orelhas em pé, porte pequeno. **Detalhe essencial:
pelos grisalhos/brancos no focinho, ao redor dos olhos e espalhados pelo rosto**
(ela é idosa). Vive na taskbar do Windows 11 e num overlay no Android.

## Estado do projeto

- **Fase atual: Fase 0 — Sprites** (em andamento)
- Aguardando: fotos reais da Kiara em `./reference/` para extrair paleta exata
- Paleta inicial proposta em `sprites/palette.json` (baseada na descrição da raça;
  será refinada com as fotos)

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

- Sprites gerados pixel a pixel via matrizes de caracteres → cores da paleta
  (cada letra na matriz mapeia para uma cor em `palette.json`). Fácil de editar
  e versionar em git.
- Resolução 48x48, fundo transparente, sem anti-aliasing; previews ampliados
  com nearest-neighbor.
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
