// Montador por camadas da Kiara: corpo + cabeça + olho do piscar → quadro 32x32.
//
// Segue sprites/final/README.md ("Camadas"):
//   1. corpo do frame em (0, 0)
//   2. cabeça (a do frame, ou a da expressão de cabeça tocando) em pescoco - ancora + off
//   3. olho do piscar em posição da cabeça + olho
//   4. barra escura: contorno G em todo pixel transparente com vizinho opaco (cima/baixo/lados)
//   5. indo pra esquerda: espelha o quadro pronto
//
// Imagens aqui são { w, h, data } (RGBA, 4 bytes por pixel), iguais ao ImageData do navegador.
// O mesmo arquivo roda no app (navegador) e no teste (Node), por isso não usa nada do DOM.

(function (root) {
  const CELL = 32;
  const OUTLINE_G = [0xa0, 0x92, 0x87, 255];   // cor G da paleta (contorno grisalho)

  function blank(w = CELL, h = CELL) {
    return { w, h, data: new Uint8ClampedArray(w * h * 4) };
  }

  // Cola src em dst na posição (x, y). As peças só têm alfa 0 ou 255, então é copiar ou pular.
  function blit(dst, src, x, y) {
    for (let sy = 0; sy < src.h; sy++) {
      const dy = y + sy;
      if (dy < 0 || dy >= dst.h) continue;
      for (let sx = 0; sx < src.w; sx++) {
        const dx = x + sx;
        if (dx < 0 || dx >= dst.w) continue;
        const s = (sy * src.w + sx) * 4;
        if (src.data[s + 3] === 0) continue;
        const d = (dy * dst.w + dx) * 4;
        dst.data[d] = src.data[s]; dst.data[d + 1] = src.data[s + 1];
        dst.data[d + 2] = src.data[s + 2]; dst.data[d + 3] = src.data[s + 3];
      }
    }
  }

  function outline(img) {
    const out = { w: img.w, h: img.h, data: new Uint8ClampedArray(img.data) };
    const opaque = (x, y) => x >= 0 && y >= 0 && x < img.w && y < img.h && img.data[(y * img.w + x) * 4 + 3] > 0;
    for (let y = 0; y < img.h; y++) for (let x = 0; x < img.w; x++) {
      if (opaque(x, y)) continue;
      if (opaque(x + 1, y) || opaque(x - 1, y) || opaque(x, y + 1) || opaque(x, y - 1)) out.data.set(OUTLINE_G, (y * img.w + x) * 4);
    }
    return out;
  }

  function mirror(img) {
    const out = blank(img.w, img.h);
    for (let y = 0; y < img.h; y++) for (let x = 0; x < img.w; x++) {
      const s = (y * img.w + x) * 4, d = (y * img.w + (img.w - 1 - x)) * 4;
      out.data[d] = img.data[s]; out.data[d + 1] = img.data[s + 1]; out.data[d + 2] = img.data[s + 2]; out.data[d + 3] = img.data[s + 3];
    }
    return out;
  }

  // lib: { cabecas: { nome: { img, ancora, olho } } } com img já carregada ({w,h,data}).
  // req: { corpo: frame do corpo (com img carregada, pescoco, cabeca, cabeca_off),
  //        cabeca?: { cabeca, off } (expressão de cabeça tocando), olho?: img do remendo do piscar,
  //        contorno?: bool, esquerda?: bool }
  function compose(lib, req) {
    const fr = req.corpo;
    const img = blank();
    blit(img, fr.img, 0, 0);
    const headName = req.cabeca ? req.cabeca.cabeca : fr.cabeca;
    const off = req.cabeca ? req.cabeca.off : fr.cabeca_off;
    const h = lib.cabecas[headName];
    const hx = fr.pescoco[0] - h.ancora[0] + off[0];
    const hy = fr.pescoco[1] - h.ancora[1] + off[1];
    blit(img, h.img, hx, hy);
    if (req.olho && h.olho) blit(img, req.olho, hx + h.olho[0], hy + h.olho[1]);
    let out = req.contorno ? outline(img) : img;
    if (req.esquerda) out = mirror(out);
    return out;
  }

  const api = { CELL, blank, blit, outline, mirror, compose };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.KiaraCompose = api;
})(this);
