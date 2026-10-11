# Bases da pose em pé (Etapa 1)

| Pasta | O que é | Status |
|---|---|---|
| `C2_32/` | Limpeza do C2 (32x32) feita por um subagente Sonnet em 4 rodadas | **Rejeitada**: o juiz Haiku (A/B embaralhado) preferiu o original nos 3 critérios (geral, pernas, rosto) |
| `C2_32_opus/` | Retoque mínimo do C2 original feito pelo Opus | `base_o3` = candidata atual (o2 venceu no rosto; a faixa de brilho no dorso foi tirada porque perdeu no geral). `base_o3_contorno` = mesma com contorno G pra taskbar escura |
| `D2_64/` | Redesenho limpo do D2 (64x64) por subagente Sonnet em 4 rodadas (`base_r4`), depois máscara grisalha do rosto reforçada pelo Opus (`base_o5`) | `base_r4` venceu o original no juiz Haiku (geral, rosto, pernas); `base_o5` venceu o r4 no rosto de "cachorra idosa". **`base_o5` = candidata atual**; `base_o5_contorno` com contorno G |
