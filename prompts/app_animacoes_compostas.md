# Prompt pra sessão do app (Fase 1): animações compostas e taskbar em cima

Cole o texto abaixo numa sessão nova do Claude Code no repo `nn-nett/kiki`.

---

Você vai continuar o app do Windows da Kiara (Fase 1, Electron, pasta `desktop/`) no repo `nn-nett/kiki`,
branch `claude/pixel-pai-windows-bar-qx0qjl`. O dono é iniciante: explique tudo em português simples e diga
exatamente o que ele precisa fazer pra testar. Commits pequenos e push nessa mesma branch; não abra PR sem ele pedir.

## 1. Antes de tudo
1. Traga os sprites novos: `git fetch origin && git merge origin/claude/charming-gates-tf2lki` (é a branch dos
   sprites; ela mudou o formato de algumas coisas, veja abaixo). Resolva conflitos mantendo o app.
2. Leia, nesta ordem: `CLAUDE.md`, `PROCESSO.md`, `sprites/final/README.md` (formato completo, principalmente as
   seções "Camadas", "Expressões por cima" e "Regras de desenho na tela"), `sprites/ANALISE.md` (o que o dono
   aprovou e por quê: ritmos e regras), `desktop/README.md` e o código atual em `desktop/`.
3. O comportamento de referência é a simulação `sprites/tools/sim_template.html` (objeto `BRAIN`); o app hoje copia
   esse cérebro em `desktop/renderer/kiara.js`.

## 2. O que mudou nos sprites (o app precisa acompanhar)
- **`andando_ofegante` não tem mais frames próprios.** Agora é uma *composição* (`composicoes` no JSON): o corpo
  `andando` + a boca ofegante (`expressoes.ofegante`, remendo na âncora `boca` de cada frame), cada um no seu
  relógio (passo a cada 100 ms, respiração a cada 130 ms, sem sincronizar). O dono aprovou assim ("andando tá ok,
  perfeito"). Os PNGs `andando_ofegante_*` foram removidos.
- **Tudo agora também existe em camadas** (`final/camadas/` + `camadas` no JSON): corpo sem cabeça por frame (com
  `pescoco`), cabeças soltas (`head`, `head_bark1/2`, `head_ofegante1/2`, com `ancora` e `olho`) e expressões de
  cabeça (`latir`, `ofegante`) que valem pra qualquer corpo. O olho do piscar cai em qualquer cabeça. O export
  confere que montar as camadas dá exatamente os frames aprovados.
- Pedido do dono: **"componentizar: cabeça separada do corpo, olho também, pra ela poder piscar em qualquer estado,
  tipo piscar enquanto late"**.

## 3. Tarefas

### 3.1 Desenhar por camadas, com três relógios
Troque o desenho por frame inteiro pela montagem por camadas (o README explica):
corpo do frame em (0, 0) → cabeça (a do frame, ou a da expressão de cabeça que estiver tocando) em
`pescoco - ancora + off` → olho do piscar em `posição da cabeça + olho` → contorno G (#a09287, pixel transparente
com vizinho opaco em cima/baixo/lados) se a barra for escura → espelhar se estiver indo pra esquerda → ampliar
por inteiro sem suavizar. Três relógios independentes: corpo, expressão de cabeça e piscar. Escreva um teste
(Node, sem Windows) que monta todas as animações aprovadas por camadas e compara pixel a pixel com
`kiara-sprites.png`, nas 4 versões; tem que bater 100%.

### 3.2 Comportamento aleatório composto, num ritmo que faz sentido
Hoje o cérebro só troca de animação inteira. Faça dois níveis:
- **Corpo** (estado): `parada`, `andando`, meia-volta, e `latindo` parada (use o corpo `latindo` aprovado, que tem o
  tranco no tronco). Corrida e dormir ainda NÃO foram aprovados: não use.
- **Cabeça por cima do corpo**, sorteada à parte: normal, `latir` (1 ou 2 latidos, depois volta pro normal) e
  `ofegante` (loop enquanto ela estiver cansada).
- **Piscar** sempre ligado, por cima de tudo (inclusive latindo e ofegante), a cada 2,5-7 s sorteados.

Combinações que devem acontecer: parada, andando, latir parada, latir andando, ofegante parada, ofegante andando,
e piscar em qualquer uma delas.

Ritmo (tirado do que o dono aprovou, ver `sprites/ANALISE.md`):
- Nada de troca o tempo todo: parada 2-5 s, andando 3-8 s, e uma pausa curta parada antes de latir.
- Latir: preparação → AU! → volta (as durações já vêm no JSON); intervalo mínimo de ~6 s entre latidos. Andando, a
  chance de latir é baixa (algo como 1 a cada 15-20 s em média).
- Cansaço no lugar da corrida (que ainda não existe): um medidor que sobe enquanto ela anda e desce parada; passou
  do limite (uns 20 s de caminhada somados), ela fica ofegante por 3-6 s (parada ou andando), depois o medidor
  zera. Respiração sempre no ritmo dela (130 ms), nunca sincronizada com o passo.
- Clique nela = ela late (no corpo em que estiver).
Deixe os números num lugar só (um objeto `BRAIN` fácil de ajustar) e documente no `desktop/README.md`. Quando o
dono aprovar o ritmo, avise que a simulação (`sprites/tools/sim_template.html`) precisa ganhar o mesmo cérebro, pra
continuarem iguais.

### 3.3 Taskbar em cima da tela (é como o dono usa)
O dono usa a barra de tarefas **no topo** da tela e quer a Kiara **pisando na fronteira entre a taskbar e as
janelas**: as patas (última linha do sprite) na borda de baixo da taskbar, o corpo dentro da taskbar. Hoje o app
assume a barra embaixo (`main.js`: `y = workArea.y + workArea.height - altura`).
- Descubra de que lado está a barra em cada monitor comparando `display.bounds` com `display.workArea`
  (em cima: `workArea.y > bounds.y`; embaixo: `workArea.y + workArea.height < bounds.y + bounds.height`).
- Em cima: a faixa transparente fica com a borda de baixo em `workArea.y` (patas na fronteira). Embaixo: como hoje
  (patas na borda de cima da barra). Barra do lado: mantenha embaixo da tela como fallback e avise no README.
- Tamanho: a Kiara tem 32 px; a 2x são 64 px e a barra do Windows 11 tem 48 px a 100% de escala (72 px a 150%).
  Com a barra em cima ela não pode passar do topo da tela: no modo "Automático" use a maior escala inteira que caiba
  na altura da barra; o menu da bandeja continua podendo forçar 1x/2x/3x.
- Ela continua passando de um monitor pro outro quando os dois têm a barra no mesmo lado.

## 4. Como testar e entregar
- Teste o que der sem Windows: o teste de camadas (3.1), uma página de demonstração do renderer no navegador com uma
  taskbar falsa em cima (abra com o Playwright/Chromium que já vem no ambiente e confira que não há erros no
  console), e a lógica de posição da janela com valores de `bounds`/`workArea` de exemplo (barra em cima, embaixo,
  dois monitores, escala 100% e 150%).
- Atualize `desktop/README.md` e o `CLAUDE.md` (o que mudou, o que falta o dono testar).
- No fim, diga ao dono em passos curtos: `git pull` na pasta do projeto, `cd desktop`, `npm install` (só se mudou
  dependência), `npm start`, e o que ele deve observar (ela pisando na borda de baixo da barra lá em cima; latindo
  andando; piscando latindo; ofegante andando depois de andar bastante).
- Regra de ouro do projeto: nada de desenhar ou mudar sprite dentro do app. Se faltar algo (ex.: rabo abanando,
  sentada), anote e peça pra sessão de sprites.
