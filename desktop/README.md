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

- Anda, para e late sozinha em cima da barra (mesmo "cérebro" da simulação aprovada).
- **Pisca** de vez em quando, em qualquer coisa que estiver fazendo.
- Fica **ofegante** (língua de fora) depois de correr, parada ou andando. Isso só aparece quando a
  corrida for aprovada.
- Chegou na ponta da tela: dá meia-volta. Se tiver outro monitor colado daquele lado, ela
  **passa pro outro monitor**.
- **Clicou nela = ela late.** Fora dela, os cliques passam direto pro que está atrás.
- Barra escura → usa a versão com **contorno grisalho** (automático; dá pra forçar no menu).

## Menu da bandeja (ícone perto do relógio)

- Mostrar/Esconder a Kiara (clicar no ícone também alterna)
- Latir!
- Tamanho: 1x, 2x (padrão), 3x
- Contorno grisalho: Automático / Sempre / Nunca
- Abrir junto com o Windows
- Sair

## Como funciona (pra quem for mexer)

| Arquivo | O que faz |
|---|---|
| `main.js` | Cria uma faixa transparente em cima da barra em cada monitor, a bandeja, o tema e a passagem entre monitores. |
| `preload.js` | Ponte segura entre a página e o `main.js`. |
| `renderer/kiara.js` | O "cérebro" (estados, sorteios, tempos) e o desenho da Kiara. |

- Os sprites vêm direto de `../sprites/final/` (`kiara-sprites.png` + `.json`). Quando a sessão
  de sprites aprovar uma animação nova e exportar, o app pega sozinho. Por exemplo, **correndo**
  entra no sorteio automaticamente assim que existir na folha.
- Pixel art sempre nítido: cada px do sprite vira um número **inteiro** de px de tela, mesmo
  com o Windows em 125% ou 150%.
- Ela anda `step_px` por frame (vem do JSON), igual as patas recuam, então não "patina".
- As preferências ficam salvas em `%APPDATA%\kiara-pixel-pal\config.json`.

## Ainda não tem

Dormir, comer + potinho, pular, reação especial ao toque, câmera noturna, passeio de coleira,
cocô e suéter. Esses dependem dos sprites da Fase 0.
