---
name: rodada-animacao
description: Método de trabalho dos sprites da Kiara pra uma rodada de animação nova ou refeita (desenhar, conferir, mostrar, aprovar), com multi-agentes (sessão principal = diretor de arte, subagentes desenhistas em paralelo, juiz Haiku). Use quando o dono pedir uma animação nova, uma rodada nova de uma pendente (virada, galope, dormindo, ofegante), mandar fotos de referência pra uma pose, ou aprovar algo pra virar final. Pra ajuste de poucos pixels use a skill ajuste-sprite.
---

# Rodada de animação da Kiara

Antes: leia `STATUS.md` (o que está validado e o que falta), `sprites/ANALISE.md` (o que o dono aprova e por
quê, e as cinco regras da reanálise de 11/11) e o log da animação em `sprites/parts/32/*_log.md`.

## Papéis

- **Sessão principal = diretor de arte.** Conversa com o dono em português simples, traduz o pedido em mudanças
  concretas, decide, revisa tudo antes de mostrar, publica e commita. As peças que definem a identidade dela (cabeça,
  rosto, uma vista nova como de frente ou 3/4) você desenha ou revisa pixel a pixel. Lição da virada: entregues de
  olho fechado ao desenhista, saíram quatro rodadas reprovadas; a rodada feita na sessão principal com a bancada
  resolveu.
- **Subagente desenhista** (Agent `general-purpose`, em background): volume e variações. Exemplos: N opções de
  uma peça, frames do meio depois das poses-chave aprovadas, espelhos, receitas, scripts. Tarefas independentes vão
  em agentes separados ao mesmo tempo (ex.: galope e dormindo), cada um com a sua pasta no scratchpad. Continue o
  mesmo agente com SendMessage enquanto a sessão durar. Numa sessão nova os agentes antigos não existem: crie
  outro com o briefing abaixo.
- **Juiz** (Agent com `model: "haiku"`): só perguntas fechadas, com duas imagens e um critério. Exemplos: "A ou B
  parece mais a foto, só na orelha?", "é a mesma cachorra nos frames 2 e 3?", "o pé escorregou?". Nunca "está
  bonito?".

## Briefing do desenhista (copie e preencha)

```
Rodada N de <animação> da Kiara (pinscher, sprites 32x32 em matriz de texto). Leia CLAUDE.md, STATUS.md,
sprites/ANALISE.md e sprites/parts/32/<x>_log.md antes.
Pedido do dono (palavras dele): "..."
O que mudar: <peças/frames/pixels, com coordenadas quando souber>
Não mexer: <o que já foi aprovado>
Regras: só cores de sprites/palette.json; bordas X embaixo de barriga/peito/pernas; perna de longe atrás da
barriga com a 1ª linha em K; sem buraco, pixel solto ou entalhe; patas na linha 31; todo movimento de 1 px;
mesma cabeça/rosto/âncora das peças aprovadas; peças NOVAS com sufixo da rodada (nunca sobrescrever).
Ferramentas: sprites/tools/bancada.py (folha ampliada + tamanho real) e rig.py com --parts sprites/parts/32.
Entregar em <scratchpad>/<anim>/vN/: quadro antes/depois, spritemap (spritemap.py) e as pastas do rig (com
_contorno e _esquerda). Anote no log da animação uma seção "Rodada N" curta. Não faça commit.
Responda curto: arquivos criados, o que mudou e por quê, dúvidas pro dono.
```

## Ciclo de uma rodada

1. **Entender.** Releia o pedido. Print do dono → ache o frame e o pixel na régua do spritemap. Fotos novas →
   salvar em `reference/` com nome descritivo e anotar em `reference/README.md`.
2. **Poses-chave primeiro.** Numa animação nova, desenhe e mostre só as 2-3 poses que definem o movimento. Os
   frames do meio vêm depois da aprovação.
3. **Desenhar** (você ou o desenhista). Vista intermediária = híbrido das duas pontas aprovadas (ex.: a cabeça
   3/4 é metade a de frente e metade o perfil). Posição por medida: escolha o eixo do giro e calcule onde caem olho
   e nariz. A mesma marca aparece em todas as vistas.
4. **Conferir na bancada** antes de mostrar:
   ```python
   import sys; sys.path.insert(0, "sprites/tools")
   from bancada import *
   f = frames_of("virar_B5")
   show("<scratchpad>/x.png", [("B5", f)])           # ampliado + 2x/3x em fundo claro e escuro
   print([diff(f[i][1], f[i+1][1]) for i in range(len(f)-1)])   # px que mudam por troca
   ```
   Confira também:
   - Primeiro e último frame iguais à `parada` pixel a pixel, quando começa ou termina parada.
   - Só cores da paleta e patas na linha 31.
   - `python3 sprites/tools/lint.py --size 32 32 <pasta>_contorno` sem erros.
   - **Decida olhando o tamanho real**, não o ampliado.
5. **Mostrar** (regra do dono: tudo vai com o spritemap):
   ```
   python3 sprites/tools/rig.py sprites/anims/X.json --out <scratch>/rig --parts sprites/parts/32
   python3 sprites/tools/page.py --out <scratch>/pagina.html --title "..." --intro "..." \
       --mapa sprites/previews/<anim>/spritemap_<anim>.png "Nome|nota|<scratch>/rig/X" ["Antes|...|pasta"]
   ```
   - Copie a página e o quadro pra `sprites/previews/<anim>/`.
   - Republique no artifact da animação com o parâmetro `url` (lista em `CONTINUAR.md`).
   - Mande o quadro antes/depois e o spritemap com SendUserFile.
   - Explique em português simples: o que mudou e por quê. Feche com as perguntas numeradas.
6. **Salvar.** Commit pequeno e push em `claude/charming-gates-tf2lki`. Atualize o log da animação, o `STATUS.md`
   e o `CLAUDE.md`. Commite trabalho em andamento também: o worker pode reiniciar e o scratchpad some.
7. **Aprovou?** Só com aprovação explícita do dono, vendo:
   - Entrada em `sprites/final/aprovadas.json` com `"status": "VALIDADO"` e a frase dele.
   - `python3 sprites/tools/export_final.py`: confere camadas e remendos e refaz a galeria.
   - Republique a galeria (https://claude.ai/artifact/Cg5sdrUGvrXio7Wn9rx6oe) com `sprites/final/galeria.html`.
   - Mova o item pra ✅ no `STATUS.md` e no checklist do `CLAUDE.md`.
   - Se o app precisa saber de algo novo (ex.: a meia-volta termina virada), anote em `sprites/final/README.md`.
