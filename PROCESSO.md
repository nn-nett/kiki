# Como trabalhamos neste projeto (guia pra qualquer sessão/agente)

Este arquivo é o "manual de operação". Qualquer sessão do Claude Code (ou outro agente) que
abrir o projeto deve ler, nesta ordem: `CLAUDE.md` (estado atual) → este arquivo (como trabalhar)
→ o guia da frente em que vai mexer (`sprites/PLANO.md` pros sprites, `desktop/README.md` pro app).

## 1. Regras que nunca mudam

- **O dono aprova tudo que é visual.** Nenhum sprite ou animação vira "final" sem ele ver e dizer
  que aprovou (de preferência com a frase dele anotada no `CLAUDE.md`).
- **Uma fase só avança com liberação explícita do dono.** Hoje: Fase 0 (sprites) e Fase 1 (app
  do Windows) andam em paralelo, liberadas por ele em 14/10/2026. Fase 2 (Android) ainda não.
- **O dono é iniciante em programação.** Explique em português simples, sem jargão, e diga
  sempre o que ele precisa fazer (testar, escolher, aprovar).
- **Mostre sempre**: toda proposta vai com imagem (folha de revisão, GIF ou página animada).
  Depois de cada aprovação, republique a Galeria (link no `CLAUDE.md`).
- **Nada se perde**: commits pequenos, push no fim de cada passo, `CLAUDE.md` atualizado a cada
  sessão (o que mudou, o que foi aprovado, o que está pendente).

## 2. As duas frentes e como elas se conversam

```
 SESSÃO DE SPRITES (Fase 0)                         SESSÃO DO APP (Fase 1)
 desenha → mostra → dono aprova                      desktop/ (Electron)
        │                                                   ▲
        ▼                                                   │ lê direto, sem copiar
 sprites/final/aprovadas.json  ── export_final.py ──►  sprites/final/
                                                       kiara-sprites.png/.json
                                                       expressoes/*.png
```

- **A "fronteira" entre as duas é a pasta `sprites/final/`** e o formato descrito em
  `sprites/final/README.md`. A sessão de sprites só escreve lá depois de aprovação; o app só lê
  de lá.
- Animação nova aprovada → `aprovadas.json` + `python3 sprites/tools/export_final.py` → commit.
  O app pega sozinho: o "cérebro" (`desktop/renderer/kiara.js`, objeto `BRAIN`) ignora estados
  cuja animação ainda não existe na folha e passa a usá-los assim que aparecem (ex.: `correndo`).
- Se o app precisar de algo que a folha ainda não tem (ex.: `latindo_andando`), **peça pra
  sessão de sprites exportar**; não desenhe sprite dentro do app.
- O comportamento é testado primeiro na **Simulação** (artifact, `sprites/tools/sim_template.html`)
  e só depois copiado pro `BRAIN` do app. Mantenha os dois iguais.

## 3. Quem faz o quê: Opus, Sonnet e Haiku

A sessão principal (a que conversa com o dono) é o **Opus**. Ele chama **Sonnet** e **Haiku**
como subagentes pela ferramenta `Agent`, escolhendo o modelo no parâmetro `model`
(`"sonnet"` ou `"haiku"`). A tabela completa, com exemplos, está em `sprites/PLANO.md`
("Quem faz o quê"). Resumo:

| Modelo | Papel | Faz | Não faz |
|---|---|---|---|
| **Opus** (sessão principal) | Diretor de arte e arquiteto | Conversa com o dono, decide, escreve o código central (rig, app), desenha/ajusta a **cabeça** (identidade dela), revisão final, commits | Loops repetitivos de muitas rodadas |
| **Sonnet** (subagente) | Desenhista e programador de rotina | Peças e receitas de animação, variantes de pixel, scripts a partir de uma especificação do Opus | Decidir sozinho o que vai pro dono |
| **Haiku** (subagente) | Juiz rápido e conferente | Perguntas **fechadas** A/B ("qual parece mais a foto, só na orelha?"), conferência frame a frame ("pé escorregou?"), validar JSON | Gosto aberto ("está bonito?") |

Por quê: o mais forte fica com as decisões e a conversa; o trabalho braçal vai pro Sonnet;
e o Haiku é barato e consistente em pergunta de sim/não comparando duas imagens.

### Como o Opus delega (modelos de prompt)

Sempre: dizer **qual pasta usar** (`sprites/candidates/<tarefa>/`), **o que entregar** e **o
critério de pronto**. O subagente não vê a conversa, então o prompt tem que ser completo.

**Sonnet desenhista**
```
Agent(model: "sonnet", description: "Desenhar <peça>", prompt: """
Projeto Kiara Pixel Pal (leia CLAUDE.md e sprites/PLANO.md).
Tarefa: desenhar <peça/animação> em 32x32 a partir de <peças existentes em sprites/parts/32/>.
Regras: só cores de sprites/palette.json; bordas X; patas na linha 31; sem pixel solto.
Use tools/rig.py pra montar e tools/review.py pra gerar a folha de revisão.
Entregue em sprites/candidates/<tarefa>/: .txt + PNG + folha de revisão + log curto.
Não mexa em sprites/final/ nem em sprites/parts/32/. Não faça commit.
""")
```

**Haiku juiz A/B** (o Opus gera a imagem com `tools/compare.py` antes)
```
Agent(model: "haiku", description: "Juiz A/B orelha", prompt: """
Olhe a imagem <caminho>. À esquerda A, ao meio B, à direita a foto real.
Pergunta única: qual (A ou B) tem a ORELHA mais parecida com a da foto?
Responda só "A" ou "B" e uma frase de motivo.
""")
```
Use 3 juízes Haiku em paralelo quando a decisão importa e fique com a maioria.

**Haiku conferente** (depois de qualquer animação nova)
```
Agent(model: "haiku", description: "Conferir frames", prompt: """
Olhe os frames em <pasta>. Para cada par consecutivo responda sim/não:
é a mesma cachorra? as patas no chão ficaram no mesmo lugar? a orelha mudou de tamanho?
Liste só os pares com algum "não".
""")
```

### O ciclo de um sprite (do pedido à barra do Windows)

1. Dono pede ou aponta um detalhe → Opus entende e, se for ajuste fino, segue a skill
   `ajuste-sprite` (`.claude/skills/ajuste-sprite/SKILL.md`).
2. **Sonnet** desenha as variantes (em paralelo quando houver mais de uma ideia).
3. **Haiku** filtra: A/B contra a foto e conferência frame a frame. O que reprovar volta pro Sonnet.
4. **Opus** revisa o que sobrou e mostra pro dono (folha + página animada).
5. Dono escolhe/aprova → Opus aplica nas peças, `aprovadas.json`, `export_final.py`, Galeria, commit.
6. O app já usa na próxima vez que o dono rodar `npm start`.

**Limites de gasto** (do `PLANO.md`): no máximo 4 tentativas por região e ~40 chamadas de juiz
por pose. Se for estourar, pare e pergunte ao dono.

## 4. GitHub (branches)

- Cada sessão trabalha na sua branch `claude/...`. Antes de começar, traga o que as outras
  sessões já subiram: `git fetch origin` e `git merge origin/<branch da outra sessão>`.
- A branch que junta tudo (app + sprites aprovados) é a mais recente com `desktop/`; o `CLAUDE.md`
  diz qual é. Ao terminar, faça push e diga ao dono em qual branch está.

## 5. Checklist de fim de sessão

- [ ] `CLAUDE.md` atualizado (estado, aprovações com a frase do dono, pendências).
- [ ] Aprovou algo? `export_final.py` rodado e Galeria republicada.
- [ ] Mexeu no comportamento? Simulação e `desktop/renderer/kiara.js` iguais.
- [ ] Commit + push; branch informada ao dono.
