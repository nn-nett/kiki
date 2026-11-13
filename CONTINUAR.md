# Como continuar numa sessão nova

Pacote de passagem de bastão (13/11). Com este arquivo, o `CLAUDE.md` e o `STATUS.md`, uma sessão nova
continua de onde a anterior parou, sem depender da memória da conversa.

## 1. Começo de sessão

1. Branch `claude/charming-gates-tf2lki` (repo `nn-nett/kiki`): `git pull origin claude/charming-gates-tf2lki`.
2. Leia nesta ordem:
   - `CLAUDE.md` (já carrega sozinho);
   - `STATUS.md`: o que está validado, o que falta e a sugestão pra cada pendência;
   - este arquivo;
   - `sprites/ANALISE.md`: o que o dono aprova e por quê, e a reanálise de 11/11;
   - o log da animação em que vai mexer (`sprites/parts/32/*_log.md`).
3. Dependências: `pip install -r sprites/requirements.txt` (só Pillow é obrigatório pras ferramentas do rig).
4. Primeira mensagem pro dono: em poucas linhas, o que está validado, o que falta e as perguntas pendentes,
   numeradas, com a sugestão de cada uma.

## 2. Método (multi-agentes)

O passo a passo de cada rodada está na skill do projeto **`rodada-animacao`**
(`.claude/skills/rodada-animacao/SKILL.md`). Ajuste fino de poucos pixels usa a skill **`ajuste-sprite`**.

Resumo dos papéis:
- **Sessão principal: diretor de arte.** Conversa, decide, revisa e publica. Desenha ou revisa ela mesma as
  peças de identidade: cabeça, rosto, vistas novas.
- **Subagentes desenhistas** (Agent `general-purpose`, em background, um por frente de trabalho, em paralelo):
  variações, frames do meio, espelhos, scripts. Recebem o briefing da skill, criam só arquivos novos com sufixo da
  rodada e não commitam.
- **Juiz Haiku** (Agent com `model: "haiku"`): A/B fechado com duas imagens e um critério, e conferência frame a
  frame.

## 3. Regras do dono (não negociáveis)

- **Regra de ouro:** nada vira final sem a aprovação visual dele. Fase 0 antes da Fase 1. Na Fase 0, nunca avançar
  um sprite sem aprovação.
- **Explicar simples, em português.** Ele é iniciante e acompanha pelo celular.
- **Tudo o que for mostrado vai com o spritemap junto** (frames numerados, grade, régua). Ele dá print no frame e
  aponta o pixel.
- **Prévias sem contorno.** O contorno G existe só na saída final.
- **Mostrar sempre a galeria do que já foi aprovado**, "pra garantirmos que não estamos perdendo as coisas".
- Commits pequenos, push nesta branch, sem PR. Atualizar `CLAUDE.md` e `STATUS.md` a cada sessão.
- Material da Square Enix (FF1) e referências de terceiros ficam fora do git (`sprites/extern/`).

## 4. Páginas publicadas (artifacts)

Pra atualizar uma página existente, publique com o parâmetro `url` dela. Numa sessão nova, a ferramenta pede
pra ler a página antes; depois disso pode publicar por cima.

| Página | Link | Arquivo de origem |
|---|---|---|
| Galeria (tudo o que está validado) | https://claude.ai/artifact/Cg5sdrUGvrXio7Wn9rx6oe | `sprites/final/galeria.html` |
| Simulação na taskbar | https://claude.ai/artifact/GmRRzGRh512wQHAbToic6Y | `sprites/tools/sim_page.py` → `sprites/previews/simulacao/` |
| Olhar pro outro lado (rodada 5) | https://claude.ai/artifact/3UZmRxjPuafFXo6uhw1674 | `sprites/previews/virar/kiara_virar.html` |
| Expressões (ofegante A2/M/A3, piscar) | https://claude.ai/artifact/NwRJaKgDuVaZGukfRDMjxw | `sprites/previews/expressoes/kiara_expressoes.html` |
| Correndo (galopes) | https://claude.ai/artifact/8mDaYnhGo8hGKTrh5hvmm1 | `sprites/previews/correndo/kiara_correndo.html` |
| Dormindo | (sem página; offline) | `sprites/previews/dormindo/kiara_dormindo.html` |

## 5. Comandos que mais se usa

```
# montar uma receita em PNGs (sempre com --parts!)
python3 sprites/tools/rig.py sprites/anims/X.json --out <scratch>/rig --parts sprites/parts/32
# página animada com spritemap (e o PNG do spritemap pra mandar junto)
python3 sprites/tools/page.py --out <scratch>/p.html --title "..." --intro "..." --mapa mapa.png "Nome|nota|pasta"
# conferências: lint com contorno (tamanho 32) e bancada (ampliado + tamanho real)
python3 sprites/tools/lint.py --size 32 32 <scratch>/rig/X_contorno
python3 -c "import sys; sys.path.insert(0,'sprites/tools'); from bancada import *; show('x.png',[('X',frames_of('X'))])"
# ajuste fino de pixels com variantes (ver skill ajuste-sprite)
python3 sprites/tools/tweak.py show PEÇA --rows a-b --cols c-d
# depois de uma aprovação: arquivos finais + galeria
python3 sprites/tools/export_final.py
# conferir uma página sem erro (o playwright do Python pode não estar instalado)
/opt/pw-browsers/chromium --headless --no-sandbox --window-size=420,1500 --screenshot=out.png file:///caminho/pagina.html
```

## 6. Lições técnicas (pra não repetir erro)

- `rig.py` sem `--parts sprites/parts/32` procura as peças no lugar errado e falha.
- O worker da sessão pode reiniciar no meio do trabalho, e o scratchpad pode sumir junto. Commite trabalho em
  andamento com frequência. As ferramentas reutilizáveis ficam em `sprites/tools/`, não no scratch.
- Espelhar uma peça: inverter as linhas, recalcular `@anchor` e `@socket` e tirar o socket do olho (o remendo
  do piscar é desenhado pra direita; a esquerda sai espelhando o quadro pronto).
- `export_camadas.py` só converte receitas que usam a peça `upper`. As outras já vêm em camadas.
- O piscar de frente usa um remendo único pros dois olhos (`olho_frente_meio`/`_fechado`, no socket `olho`), pra o
  app continuar com um remendo por cabeça.
- A simulação ainda não roda quadros mais largos que 32. O galope v5 tem 40 e a cama com travesseiro tem 44.
- Subagentes podem bater no limite de uso. Quando liberar, retome o mesmo agente com SendMessage.
