# Status da Kiara: o que está validado e o que falta

Painel único do projeto. Atualizado em 13/11. Quem aprova é o dono, vendo. Nada entra como validado sem
ele dizer, e tudo o que está validado está em `sprites/final/` com `"status": "VALIDADO"` em
`sprites/final/aprovadas.json`.

Fase atual: **Fase 0 (sprites)**, nesta branch (`claude/charming-gates-tf2lki`). O app do Windows (Fase 1)
anda em outra sessão, na branch `claude/pixel-pai-windows-bar-qx0qjl`, com o prompt
`prompts/app_animacoes_compostas.md`.

## ✅ Validado (pronto pro app)

Todas as animações em 32x32, em 4 versões (normal, `_esquerda`, `_contorno` pra taskbar escura e
`_contorno_esquerda`). Ver animado: Galeria https://claude.ai/artifact/Cg5sdrUGvrXio7Wn9rx6oe

| Animação | Receita | O que o dono disse |
|---|---|---|
| `parada` (pose base, em pé de lado) | `anims/stand.json` | pose base aprovada (`sprites/base/kiara_32.txt`) |
| `andando` (trote B, 6×100 ms, 1 px/frame) | `anims/walk_b.json` | "o trote b tá ótimo", "já temos frames pra Kiki andando" |
| `latindo` (com tranco) | `anims/latir_tranco.json` | "o latido com tranco tá perfeito" |
| `piscando` + remendo do olho (cai por cima de qualquer animação) | `anims/piscar.json` | "ofegante e piscada validados" (15/10) |
| `ofegante` parada (língua A) | `anims/ofegante.json` | validado em 15/10; **em revisão**, ver abaixo |
| `andando_ofegante` (composição: passo 100 ms + boca 130 ms, sem sincronizar) | composição em `aprovadas.json` | "andando tá ok, perfeito" (15/10) |

Também validado (decisões que valem pra tudo):
- Tamanho único **32x32** ("só 32"); o 64, o 16 e o 8 saíram.
- **Contorno grisalho G** pra taskbar escura (as prévias são feitas sem contorno, a pedido dele).
- Proporção P1, barriga 2 px mais funda toda preta, peito mais fundo, toquinho do rabo 1 px mais alto.
- Olho castanho com 1 px de brilho; nada de olho azulado.
- Língua do ofegante com a ponta reta (opção A); queixo desce com a respiração.

Pronto a pedido do dono (estrutura, conferido pixel a pixel contra os 80 frames finais):
- **Componentes separados**: corpo sem cabeça, cabeças soltas e olho, pra montar combinações (ex.: piscar
  latindo). Ficam em `sprites/final/camadas/` e na chave `camadas` do JSON.
- **Taskbar em cima da tela**: é como ele usa. Ela pisa na borda de baixo da taskbar.

## ⏳ Falta o dono validar

1. **Olhar pro outro lado (rodada 5, de 11/11)**
   - Página: https://claude.ai/artifact/3UZmRxjPuafFXo6uhw1674
   - Quadro antes/depois: `sprites/previews/virar/quadro_rodada5.png`
   - Três animações:
     - `virar_B5`: meia-volta, começa na `parada` e termina na `parada_esquerda`.
     - `virar_A5`: olhar pra trás, por cima do ombro.
     - `olhar_voce5`: vira a cabeça, olha pra você, pisca com os dois olhos e volta. Ideia pra reação ao mouse ou ao clique.
   - Pergunta aberta: a orelha é castanha por dentro no perfil e escura de frente (como nas fotos). Fica assim, ou escurece a do perfil?
   - Ao aprovar:
     - Pôr as três em `aprovadas.json`.
     - O export precisa aprender o remendo de piscar dos dois olhos (`olho_frente_meio`/`_fechado`).
     - A meia-volta precisa avisar o app que ela termina virada pro outro lado.
   - Histórico: `sprites/parts/32/virar_log.md`.
2. **Ofegante parada**
   - Opções:
     - `ofegante_A2`: a barriga toda estufa.
     - `ofegante_M`: meio-termo.
     - `ofegante_A3`: só o peito.
   - Página: https://claude.ai/artifact/NwRJaKgDuVaZGukfRDMjxw
   - Sugestão: **M**. Em tamanho real as três ficam praticamente iguais.
   - Ao escolher, trocar a receita do `ofegante` em `aprovadas.json`, rodar `export_final.py` e a simulação (`sim_page.py --pant`).
3. **Galope (correndo)**
   - Nenhuma versão aprovada. Opções na página https://claude.ai/artifact/8mDaYnhGo8hGKTrh5hvmm1:
     - v4 (`run`) e v5 (`galope_v5`);
     - as mesmas com pescoço +2/+4;
     - corpo +3/+4.
   - Diagnóstico (`sprites/ANALISE.md`): a v4 encolhe demais ("dwarfismo") e a v5 estica demais e fica rígida.
   - Sugestão: refazer começando pelas **duas poses-chave** (recolhida e esticada), aprovar as duas e só então desenhar os frames do meio.
   - Histórico: `sprites/parts/32/run_log.md`.
4. **Dormindo**
   - Quatro opções:
     - A: de barriga.
     - B: enrolada.
     - C: apoiada no travesseiro.
     - D: inteira em cima do travesseiro.
   - Prévia offline: `sprites/previews/dormindo/kiara_dormindo.html` (republicar como página se precisar).
   - Sugestão: **D** com travesseiro, ou **A** sem.
   - Depois da escolha: respiração (2-3 frames) e a transição "subir no travesseiro".
   - Histórico: `sprites/parts/32/dormir_log.md`.

## 🔲 Ainda não começado

- Transições entre estados (parado → andando, andando → parado, parado → latindo...), pedidas em 14/10.
- Sentada/idle.
- Comendo e o potinho de ração (a paleta do pote precisa sair do terracota e ir pro bege-pedra e berinjela das fotos).
- Saltando.
- Reação ao toque, com o rabo abanando. Sugestão: separar o toquinho como peça própria, como foi feito com a cabeça.
- Câmera noturna.
- Passeio de coleira.
- Fazendo cocô e o objeto cocô.
- Suéter listrado.
