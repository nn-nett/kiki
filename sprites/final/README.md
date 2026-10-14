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
| `galeria.html` | Página com tudo animado, lida só destes arquivos (prova de que estão íntegros). |

## Animações aprovadas

Cada uma existe em 4 versões: `<nome>`, `<nome>_esquerda`, `<nome>_contorno`,
`<nome>_contorno_esquerda`.

| Nome | Frames | Durações (ms) | Ciclo | `step_px` | Uso |
|---|---|---|---|---|---|
| `parada` | 1 | 500 | 0,5 s | 0 | em pé, parada |
| `andando` | 6 | 100 cada | 0,6 s | 1 | trote, andando pela barra |
| `latindo` | 7 | 300, 90, 170, 100, 90, 170, 100 | 1,02 s | 0 | late parada (2 latidos por ciclo, com tranco) |

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

## Regras de desenho na tela

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
- **Piscar** e **ofegante** (língua pra fora): expressões desacopladas, por cima de qualquer corpo
  (remendo do olho / cabeça ofegante). Prévia https://claude.ai/artifact/NwRJaKgDuVaZGukfRDMjxw; já
  aparecem na simulação como teste. Quando aprovadas, o export ganha camadas pro app compor.
- **Transições** entre estados (parado → andando, andando → correndo, subir no travesseiro…).
- Sentada/idle, comendo + potinho, saltando, reação ao toque, câmera noturna, passeio, cocô,
  suéter: ainda não feitos.

Quando forem aprovados, entram aqui automaticamente pelo `export_final.py` (mesmo formato).
