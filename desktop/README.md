# Kiara Pixel Pal — Windows (Fase 1)

A Kiara passeando em cima da barra de tarefas do Windows 11.

## Como rodar no seu PC (Windows)

1. Instale o **Node.js** (versão LTS) em https://nodejs.org. É só next, next, next.
2. Baixe o projeto (`git clone` ou "Download ZIP" no GitHub) e abra a pasta `desktop`
   num terminal (no Explorer: clique com o botão direito dentro da pasta → "Abrir no Terminal").
3. Na primeira vez, rode:
   ```
   npm install
   ```
   (baixa o Electron, uns 100 MB; só precisa fazer uma vez.)
4. Pra soltar a Kiara:
   ```
   npm start
   ```

Pra fechar: ícone da Kiara perto do relógio (às vezes fica escondido na setinha `^`) → **Sair**.

### Gerar um .exe (opcional)

```
npm run dist
```
Cria `desktop/dist/Kiara Pixel Pal x.y.z.exe` (portátil, não precisa instalar). O Windows pode
avisar "editor desconhecido" porque o app não é assinado: "Mais informações" → "Executar assim mesmo".

## O que ela faz

- **Barra em cima da tela** (como o dono usa): ela pisa na fronteira entre a barra e as janelas,
  com as patas na borda de baixo da barra e o corpo dentro dela. **Barra embaixo**: ela anda em
  cima da barra. **Barra do lado**: fica no pé da tela (não é o caso pensado; avise se usar assim).
- Cada quadro é **montado na hora por camadas**: corpo + cabeça + olho. Por isso ela combina as
  coisas sozinha: parada, andando, latir parada, **latir andando**, ofegante parada, **ofegante
  andando** e **piscar em qualquer uma delas** (inclusive latindo).
- **Cansaço**: andar enche um medidor (e ficar parada esvazia). Depois de uns 20 s de caminhada
  somados, ela fica ofegante por 3-6 s (parada ou andando) e o medidor zera. É o lugar da
  corrida até a corrida ser aprovada.
- Chegou na ponta da tela: dá meia-volta. Se tiver outro monitor colado daquele lado **com a barra
  do mesmo lado**, ela passa pro outro monitor.
- **Clicou nela = ela late**: parada, late com o tranco no corpo; andando, late sem parar de andar.
  Fora dela, os cliques passam direto pro que está atrás.
- Barra escura → **contorno grisalho** (automático; dá pra forçar no menu).

## O "cérebro" (números pra ajustar)

Tudo fica no objeto `BRAIN`, no começo de `renderer/kiara.js`. Valores de hoje:

| O quê | Valor | Por quê |
|---|---|---|
| Parada | 2-5 s | nada de troca o tempo todo |
| Andando | 3-8 s | idem |
| Depois de parada | anda 55%, late 20%, meia-volta e anda 15%, continua parada 10% | |
| Depois de andando | para 60%, meia-volta 20%, para e late 20% | |
| Pausa antes de latir | 0,4-0,9 s parada | pausa antes da ação (ver `sprites/ANALISE.md`) |
| Latidos por vez | 1 (60%) ou 2 (40%) | |
| Intervalo mínimo entre latidos | 6 s | |
| Latir andando | em média 1 a cada ~17 s andando | |
| Cansaço | +1/s andando, -0,5/s parada; limite 20; ofegante 3-6 s; 50% continua andando | |
| Piscar | a cada 2,5-7 s (vem do JSON), sempre ligado | |
| Ritmos | passo 100 ms, respiração 130 ms, latido 300/90/170/100 ms | vêm do JSON; cada um no seu relógio |

Quando o dono aprovar esse ritmo, a simulação (`sprites/tools/sim_template.html`) precisa ganhar o
mesmo cérebro, pra continuarem iguais.

## Tamanho

- **Automático** (padrão): com a barra em cima, o maior tamanho inteiro que cabe na altura da
  barra (a 100% de escala do Windows a barra tem 48 px, então ela fica com 32 px = 1x; a 150% cabe
  64 px físicos = 2x). Com a barra embaixo, 2x.
- O menu da bandeja pode forçar 1x, 2x ou 3x. Com a barra em cima, 2x a 100% passa um pouco do
  topo da tela (a cabeça corta).

## Menu da bandeja (ícone perto do relógio)

- Mostrar/Esconder a Kiara (clicar no ícone também alterna)
- Latir!
- Tamanho: Automático (padrão), 1x, 2x, 3x
- Contorno grisalho: Automático / Sempre / Nunca
- Abrir junto com o Windows
- Sair

## Como funciona (pra quem for mexer)

| Arquivo | O que faz |
|---|---|
| `main.js` | Cria uma faixa transparente em cada monitor, a bandeja, o tema e a passagem entre monitores. |
| `layout.js` | Contas de posição: de que lado está a barra, altura, tamanho automático, vizinhos. |
| `preload.js` | Ponte segura entre a página e o `main.js`. |
| `renderer/compose.js` | Monta o quadro: corpo → cabeça → olho → contorno → espelho (igual ao `sprites/final/README.md`). |
| `renderer/kiara.js` | O "cérebro" (três relógios: corpo, cabeça, piscar) e o desenho. |
| `demo/index.html` | Página de demonstração no navegador, com uma barra falsa em cima e botões. |
| `test/` | Testes que rodam sem Windows (`npm test`). |

- Lê as camadas de `../sprites/final/camadas/` + `kiara-sprites.json`. Nada de sprite é desenhado
  no app: se faltar algo, peça pra sessão de sprites.
- Pixel art sempre nítido: cada px do sprite vira um número **inteiro** de px de tela.
- Ela anda `step_px` por frame do corpo (vem do JSON), igual as patas recuam: não "patina".
- As preferências ficam salvas em `%APPDATA%\kiara-pixel-pal\config.json`.

### Testes (sem Windows)

```
npm test
```
- `test/camadas.test.js`: monta todas as animações aprovadas por camadas e compara pixel a pixel
  com `kiara-sprites.png`, nas 4 versões (hoje 80 quadros, todos iguais).
- `test/layout.test.js`: posição da faixa com barra em cima/embaixo/do lado, 100%/125%/150%,
  dois monitores.

Demonstração no navegador: na raiz do projeto rode `python -m http.server 8765` e abra
http://localhost:8765/desktop/demo/index.html

## Ainda não tem

Correr e dormir (esperando aprovação), comer + potinho, pular, reação especial ao toque (rabo
abanando), sentada, câmera noturna, passeio de coleira, cocô e suéter. Dependem dos sprites da Fase 0.
Quando a corrida for aprovada, o cérebro precisa de um estado novo pra ela (o cansaço passa a vir
da corrida).
