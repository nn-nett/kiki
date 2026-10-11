# Bases da pose em pé (Etapa 1)

| Pasta | O que é | Status |
|---|---|---|
| `C2_32/` | Limpeza do C2 (32x32) feita por um subagente Sonnet em 4 rodadas | **Rejeitada**: o juiz Haiku (A/B embaralhado) preferiu o original nos 3 critérios (geral, pernas, rosto) |
| `C2_32_opus/` | Retoque mínimo do C2 original feito pelo Opus | `base_o3` = candidata atual (o2 venceu no rosto; a faixa de brilho no dorso foi tirada porque perdeu no geral). `base_o3_contorno` = mesma com contorno G pra taskbar escura |
| `D2_64/` | (removido) base 64x64 | O dono descartou o tamanho 64; o 32 é o máximo |
| `C2_32_testa/` | Variações da testa do 32 (pontos bege → preto, cristinha grisalha, sobrancelha bege/grisalha) | aguardando escolha do dono |
| `C2_16/`, `C2_8/`, `trio/` | (removidos) 16x16 e 8x8 | O dono achou fracos e ficou só com o 32 |
| `C2_32_sobrancelha/` | 5 sugestões de sobrancelha (1 px cinza na linha dos cinzas acima do olho, mais à direita) sobre a `v1_preta` escolhida pelo dono | escolhida: **s3** (ponta direita) |

**Resultado: `sprites/base/kiara_32.txt`** = s3 com buracos fechados (orelha, toquinho, patas da frente). Aprovado pelo dono com contorno G.
