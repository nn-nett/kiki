// Teste: montar as animações aprovadas por camadas tem que dar EXATAMENTE os frames da folha
// oficial (kiara-sprites.png), nas 4 versões (normal, _esquerda, _contorno, _contorno_esquerda).
// Roda sem Windows: `npm test`.
const fs = require('fs');
const path = require('path');
const { PNG } = require('pngjs');
const { compose } = require('../renderer/compose.js');

const FINAL = path.join(__dirname, '..', '..', 'sprites', 'final');
const meta = JSON.parse(fs.readFileSync(path.join(FINAL, 'kiara-sprites.json'), 'utf8'));
const load = (rel) => { const p = PNG.sync.read(fs.readFileSync(path.join(FINAL, rel))); return { w: p.width, h: p.height, data: p.data }; };
const sheet = load(meta.sheet);

function crop(f) {
  const out = { w: f.w, h: f.h, data: Buffer.alloc(f.w * f.h * 4) };
  for (let y = 0; y < f.h; y++) sheet.data.copy(out.data, y * f.w * 4, ((f.y + y) * sheet.w + f.x) * 4, ((f.y + y) * sheet.w + f.x + f.w) * 4);
  return out;
}

const cam = meta.camadas;
const lib = { cabecas: {} };
for (const [n, c] of Object.entries(cam.cabecas)) lib.cabecas[n] = { ...c, img: load(c.img) };
const piscar = meta.expressoes.piscar.frames.map(f => load(f.img));

const VERSOES = [['', false, false], ['_esquerda', false, true], ['_contorno', true, false], ['_contorno_esquerda', true, true]];
let ok = 0, fail = 0;
for (const [nome, corpo] of Object.entries(cam.corpos)) {
  corpo.frames.forEach((fr, k) => {
    const frame = { ...fr, img: load(fr.img) };
    // "piscando" = parada com o piscar tocando nos frames 1..3 (meio, fechado, meio)
    const olho = nome === 'piscando' && k > 0 ? piscar[k - 1] : null;
    for (const [suf, contorno, esquerda] of VERSOES) {
      const got = compose(lib, { corpo: frame, olho, contorno, esquerda });
      const ref = crop(meta.animations[nome + suf].frames[k]);
      if (Buffer.compare(Buffer.from(got.data), ref.data) === 0) ok++;
      else { fail++; console.log(`ERRO: ${nome}${suf} frame ${k} não bate`); }
    }
  });
}
console.log(`camadas: ${ok} frames iguais à folha oficial, ${fail} diferentes`);
process.exit(fail || !ok ? 1 : 0);
