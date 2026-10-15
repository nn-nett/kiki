# Sprites prontos da Kiara (pra implementação)

Tudo nesta pasta foi **aprovado pelo dono** e é gerado por `python3 sprites/tools/export_final.py`
a partir de `aprovadas.json`. Não edite os PNGs à mão: eles saem das peças em `sprites/parts/32/`.
Pra ver tudo animado: Galeria da Kiara, https://claude.ai/artifact/Cg5sdrUGvrXio7Wn9rx6oe
(também em `galeria.html` nesta pasta, abre offline).

## Arquivos

| Arquivo | O que é |
|---|---|
| `kiara-sprites.png` | Folha única (RGBA, fundo transparente), células de 32x32 lado a lado numa linha. |
| `kiara-sprites.json` | Metadados: posição de cada frame na folha, duração, loop, passo e frames no ar. |
| `frames/<anim>/<anim>[_variante]_<i>.png` | Os mesmos frames soltos, 32x32 cada (pra quem preferir um PNG por frame). |
| `aprovadas.json` | Lista das animações aprovadas e de qual receita (`sprites/anims/*.json`) cada uma sai. |
| `expressoes/` | Remendos das expressões: piscar (`olho_meio`, `olho_fechado`, 4x3) e ofegante (`boca_ofegante1/2`, 5x5, e `_contorno` 7x7), cada um também em `_esquerda`. |
| `spritemap.png` | Folha de revisão: todos os frames das versões normais, numerados, com grade e régua. |
| `camadas/` | As mesmas animações em peças: `corpo/<anim>_<i>.png` (sem cabeça) e `cabeca/<nome>.png`. Ver "Camadas". |
| `galeria.html` | Página com tudo animado, lida só destes arquivos (prova de que estão íntegros). |

## Animações aprovadas

Cada uma existe em 4 versões: `<nome>`, `<nome>_esquerda`, `<nome>_contorno`,
`<nome>_contorno_esquerda`.

| Nome | Frames | Durações (ms) | Ciclo | `step_px` | Uso |
|---|---|---|---|---|---|
| `parada` | 1 | 500 | 0,5 s | 0 | em pé, parada |
| `andando` | 6 | 100 cada | 0,6 s | 1 | trote, andando pela barra |
| `latindo` | 7 | 300, 90, 170, 100, 90, 170, 100 | 1,02 s | 0 | late parada (2 latidos por ciclo, com tranco) |
| `piscando` | 4 | 1500, 60, 110, 60 | 1,73 s | 0 | parada piscando (o piscar também existe solto, ver abaixo) |
| `ofegante` | 2 | 130, 130 | 0,26 s | 0 | parada com a língua pra fora (em revisão: o dono está escolhendo como o peito mexe) |

Composições (não têm frames próprios: são um corpo aprovado + uma expressão tocando juntos, cada um no
seu relógio; ficam em `composicoes` no JSON):

| Nome | Corpo | Expressão | `step_px` | Uso |
|---|---|---|---|---|
| `andando_ofegante` | `andando` (100 ms por frame) | `ofegante` (boca, 130 ms por frame) | 1 | andando com a língua pra fora (ex.: depois de correr) |

**Mudou em 15/10:** `andando_ofegante` deixou de ser frames prontos (a boca ia sincronizada com o passo e o
dono achou estranho). Agora é `andando` + o remendo da boca no ritmo dele. Se o app usava os frames
`andando_ofegante_*`, troque por isso (ver "Expressões por cima" abaixo).

## Formato do JSON

```json
{
  "sheet": "kiara-sprites.png",
  "cell": { "w": 32, "h": 32 },
  "animations": {
    "andando": {
      "loop": true,
      "step_px": 1,
      "airborne_frames": [],
      "frames": [ { "x": 128, "y": 0, "w": 32, "h": 32, "duration_ms": 100 }, ... ]
    },
    "andando_esquerda": { "step_px": -1, ... }
  }
}
```

- `frames[i]`: recorte da folha (`x, y, w, h`) e quanto tempo o frame fica na tela.
- `step_px`: quantos **pixels do sprite** a janela anda a cada troca de frame. Negativo = pra
  esquerda. Com o sprite ampliado 2x, a janela anda `step_px * 2` px de tela por frame. Isso
  casa com as patas no chão (elas recuam exatamente isso por frame), então ela não "patina".
  Se a velocidade da animação mudar, mude o passo junto (é por frame, não por segundo).
- `airborne_frames`: índices dos frames com as patas fora do chão (o galope vai usar).
- `frames[i].olho`: canto `[x, y]` onde o remendo do piscar cai nessa célula (`null` = a animação já
  mexe no olho, como `piscando`).

## Expressões por cima (piscar e ofegante, desacopladas do corpo)

Cada expressão tem um relógio próprio, separado da animação do corpo, e um remendo pequeno desenhado por
cima da célula. A âncora (`expressoes.<nome>.ancora`) diz qual campo do frame dá a posição: `olho` (piscar)
ou `boca` (ofegante). Valor `null` = aquela animação já mexe nisso (não desenhe).

### Ofegante (boca)

```json
"ofegante": {
  "ancora": "boca",
  "frames": [
    { "img": "expressoes/boca_ofegante1.png", "img_esquerda": "...", "img_contorno": "...", "img_contorno_esquerda": "...", "duration_ms": 130 },
    { "img": "expressoes/boca_ofegante2.png", "...": "...", "duration_ms": 130 }
  ],
  "loop": true,
  "contorno_folga_px": 1
}
```

- Toque em loop (130 ms por frame) enquanto ela estiver ofegante, num relógio que não depende do passo.
- Em cada desenho: pinte a célula do corpo (ex.: `andando`) e o remendo em `(célula.x + boca[0], célula.y + boca[1])`.
  Nas `_esquerda` use `img_esquerda`; nas `_contorno` use `img_contorno` (ou `img_contorno_esquerda`) em
  `boca - 1` nos dois eixos (ele tem 1 px de folga em volta, pro contorno da língua).
- Conferido: `andando` + remendo = trote com a cabeça ofegante montado pelo rig, nas 4 versões e nas duas bocas.
  A galeria mostra o `andando_ofegante` assim.

### Piscar (olho)

O piscar não precisa de frames novos por animação: é um remendo pequeno do olho desenhado por cima.

```json
"expressoes": {
  "piscar": {
    "frames": [
      { "img": "expressoes/olho_meio.png",    "img_esquerda": "expressoes/olho_meio_esquerda.png",    "duration_ms": 60 },
      { "img": "expressoes/olho_fechado.png", "img_esquerda": "expressoes/olho_fechado_esquerda.png", "duration_ms": 110 },
      { "img": "expressoes/olho_meio.png",    "img_esquerda": "expressoes/olho_meio_esquerda.png",    "duration_ms": 60 }
    ],
    "intervalo_ms": [2500, 7000]
  }
}
```

- Um relógio próprio, independente da animação do corpo: a cada `intervalo_ms` (sorteie um valor entre os
  dois) toque os 3 frames do piscar.
- Em cada desenho: pinte a célula do corpo e, se o piscar estiver tocando e `frame.olho` não for `null`,
  pinte o remendo em `(célula.x + olho[0], célula.y + olho[1])`, na mesma escala. Nas animações
  `_esquerda`, use `img_esquerda` (a posição já vem espelhada no JSON). O mesmo remendo serve pras
  versões `_contorno`.
- Conferido: parada + remendo = `piscando` pixel a pixel, e o remendo cai no olho certo em todos os
  frames de andando, latindo e ofegante (comparado com o rig). A galeria tem a caixa "Piscar por cima".

## Camadas (corpo, cabeça e olho separados)

Pedido do dono: "componentizar: a cabeça separada do corpo, o olho também, pra ela poder piscar em qualquer
estado, tipo piscar enquanto late". Os frames inteiros continuam valendo; as camadas são pra combinar à vontade
(latir andando, piscar latindo, ofegante andando...). Tudo em `camadas` no JSON:

```json
"camadas": {
  "corpos": {
    "andando": { "loop": true, "step_px": 1, "frames": [
      { "img": "camadas/corpo/andando_0.png", "duration_ms": 100, "pescoco": [20, 14], "cabeca": "head", "cabeca_off": [0, 0] }, "..."
    ] },
    "parada": { "...": "..." }, "latindo": { "...": "..." }, "ofegante": { "...": "..." }
  },
  "cabecas": {
    "head": { "img": "camadas/cabeca/head.png", "ancora": [4, 14], "olho": [6, 9] },
    "head_bark1": { "...": "..." }, "head_bark2": { "...": "..." }, "head_ofegante1": { "...": "..." }, "head_ofegante2": { "...": "..." }
  },
  "expressoes_cabeca": {
    "latir":    { "loop": false, "frames": [ { "cabeca": "head_bark1", "off": [0, 1], "duration_ms": 90 }, "..." ] },
    "ofegante": { "loop": true,  "frames": [ { "cabeca": "head_ofegante1", "off": [0, 0], "duration_ms": 130 }, "..." ] }
  }
}
```

Montar um quadro (32x32, olhando pra direita), com 3 relógios independentes (corpo, expressão de cabeça, piscar):
1. Desenhe o corpo do frame atual em (0, 0).
2. Cabeça: a do frame (`cabeca` + `cabeca_off`) ou, se uma expressão de cabeça estiver tocando, a dela (`cabeca` +
   `off`). Posição: `pescoco - ancora + off`.
3. Piscar: se estiver piscando e a cabeça tiver `olho`, desenhe o remendo do olho (`expressoes.piscar`) em
   `posição da cabeça + olho`.
4. Taskbar escura: contorno G (#a09287) em todo pixel transparente que tem vizinho opaco em cima, embaixo ou dos
   lados. Depois, se ela estiver indo pra esquerda, espelhe o quadro. Por fim amplie por inteiro sem suavizar.

Conferido no export (`tools/export_camadas.py`): montar as camadas dá exatamente os frames aprovados, nas 4 versões
(80 frames). A galeria tem um "Montador por camadas" que faz isso ao vivo.

## Regras de desenho na tela

- **Taskbar em cima da tela (é como o dono usa):** ela pisa na fronteira entre a taskbar e as janelas, ou seja,
  a última linha do sprite (as patas) fica na borda de baixo da taskbar e o corpo fica dentro da taskbar. A
  simulação tem o botão "Taskbar em cima / Embaixo". Atenção ao tamanho: a taskbar do Windows 11 tem 48 px a 100%
  de escala, e a Kiara ampliada 2x tem 64 px de altura; nessa combinação a cabeça passaria do topo da tela. Ver
  na Fase 1 (1x cabe; com escala de 150% a taskbar tem 72 px e 2x cabe).

- **Tamanho nativo 32x32.** Amplie só por inteiro (2x é o padrão pensado pra taskbar) e sempre
  sem suavização: `image-rendering: pixelated` no CSS / `imageSmoothingEnabled = false` no canvas.
- **Patas na última linha** (linha 31 da célula): alinhe a base da célula com o chão da barra.
- **Virar de lado:** troque pra variante `_esquerda` (já espelhada) em vez de espelhar na hora.
  Ela olha pra direita nas versões normais.
- **Taskbar escura:** ela é preta, então use as variantes `_contorno` (borda grisalha G #a09287)
  quando o tema do Windows estiver escuro. Na taskbar clara, as versões sem contorno.
- **Cores:** a paleta oficial está em `sprites/palette.json` (não invente cores novas).

## Comportamento (rascunho do "cérebro")

A simulação https://claude.ai/artifact/GmRRzGRh512wQHAbToic6Y (código em
`sprites/tools/sim_template.html`, objeto `BRAIN`) tem a máquina de estados que o dono viu e
gostou: parada → andar/latir/correr; andando → parar/latir andando/latir/meia-volta/correr;
vira ao chegar na ponta da barra; toque nela = late. Chances e tempos estão lá e podem ser
ajustados.

"Latir andando" na simulação é montado por camadas (pernas do trote + cabeça do latido) com
`sprites/tools/sim_page.py`; **ainda não existe na folha final**. Se o app precisar, peça o
export dessa combinação (ou das camadas separadas) na sessão de sprites.

## Ainda NÃO aprovados (não use como final)

- **Correndo** (galope, 6×70 ms, `step_px` 2): em revisão (cabeça de corrida sendo corrigida).
- **Dormindo**: 4 opções esperando a escolha do dono (A/B sem travesseiro, C/D com travesseiro,
  estas num quadro 44x32 com o objeto `travesseiro`).
- **Ofegante desacoplado** (cabeça ofegante por cima de qualquer corpo, ex.: correndo ofegante): hoje sai
  pronto só parada (`ofegante`) e andando (`andando_ofegante`). O próximo passo é exportar em camadas
  (corpo sem cabeça + âncora da cabeça por frame + cabeças por expressão) pro app compor.
- **Transições** entre estados (parado → andando, andando → correndo, subir no travesseiro…).
- Sentada/idle, comendo + potinho, saltando, reação ao toque, câmera noturna, passeio, cocô,
  suéter: ainda não feitos.

Quando forem aprovados, entram aqui automaticamente pelo `export_final.py` (mesmo formato).
