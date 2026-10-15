// Teste da posição da faixa com valores de exemplo (sem Windows): `npm test`.
const assert = require('assert');
const L = require('../layout.js');

const disp = (id, x, w, h, sf, bar) => {
  const bounds = { x, y: 0, width: w, height: h };
  const workArea = bar === 'top' ? { x, y: 48, width: w, height: h - 48 }
    : bar === 'bottom' ? { x, y: 0, width: w, height: h - 48 }
    : bar === 'left' ? { x: x + 48, y: 0, width: w - 48, height: h }
    : { ...bounds };
  return { id, bounds, workArea, scaleFactor: sf };
};

let n = 0;
const check = (name, fn) => { fn(); n++; console.log('ok -', name); };

check('barra em cima a 100%: 1x (32 px cabe nos 48 px da barra), patas na borda de baixo da barra', () => {
  const d = disp(1, 0, 1920, 1080, 1, 'top');
  assert.strictEqual(L.taskbarSide(d), 'top');
  assert.strictEqual(L.taskbarHeight(d), 48);
  assert.strictEqual(L.pixelScale(d, 'auto'), 1);
  assert.deepStrictEqual(L.stripBounds(d, 'auto'), { x: 0, y: 16, width: 1920, height: 32 });
});

check('barra em cima a 150%: barra de 48 px lógicos = 72 físicos → 2 px físicos por px do sprite (Kiara com 64 px físicos)', () => {
  const d = { id: 1, bounds: { x: 0, y: 0, width: 1280, height: 720 }, workArea: { x: 0, y: 48, width: 1280, height: 672 }, scaleFactor: 1.5 };
  assert.strictEqual(L.pixelScale(d, 'auto'), 2);
  const s = L.stripBounds(d, 'auto');
  assert.strictEqual(s.height, 43);           // 64 físicos / 1,5 = 42,7 → 43 lógicos
  assert.strictEqual(s.y + s.height, 48);   // patas na borda de baixo da barra
  assert.ok(s.y >= 0);                       // não passa do topo da tela
});

check('barra em cima com 2x forçado no menu: obedece (pode passar do topo, escolha do dono)', () => {
  const d = disp(1, 0, 1920, 1080, 1, 'top');
  assert.strictEqual(L.pixelScale(d, 2), 2);
  assert.deepStrictEqual(L.stripBounds(d, 2), { x: 0, y: -16, width: 1920, height: 64 });
});

check('barra embaixo a 100%: 2x, patas no topo da barra', () => {
  const d = disp(1, 0, 1920, 1080, 1, 'bottom');
  assert.strictEqual(L.taskbarSide(d), 'bottom');
  assert.strictEqual(L.pixelScale(d, 'auto'), 2);
  assert.deepStrictEqual(L.stripBounds(d, 'auto'), { x: 0, y: 1032 - 64, width: 1920, height: 64 });
});

check('barra embaixo a 125%: escala inteira (round(2*1.25)=3 px físicos), faixa encostada na barra', () => {
  const d = disp(1, 0, 1536, 864, 1.25, 'bottom');
  assert.strictEqual(L.pixelScale(d, 'auto'), 3);
  const s = L.stripBounds(d, 'auto');
  assert.strictEqual(s.y + s.height, 864 - 48);
});

check('barra do lado: fallback no pé da tela', () => {
  const d = disp(1, 0, 1920, 1080, 1, 'left');
  assert.strictEqual(L.taskbarSide(d), 'left');
  const s = L.stripBounds(d, 'auto');
  assert.strictEqual(s.y + s.height, 1080);
  assert.strictEqual(s.x, 48);
});

check('dois monitores com a barra em cima: vizinhos dos dois lados', () => {
  const a = disp(1, 0, 1920, 1080, 1, 'top'), b = disp(2, 1920, 1280, 1024, 1, 'top');
  assert.strictEqual(L.neighbor([a, b], a, 'right'), b);
  assert.strictEqual(L.neighbor([a, b], b, 'left'), a);
  assert.strictEqual(L.neighbor([a, b], a, 'left'), null);
});

check('dois monitores com barras em lados diferentes: não passa de um pro outro', () => {
  const a = disp(1, 0, 1920, 1080, 1, 'top'), b = disp(2, 1920, 1920, 1080, 1, 'bottom');
  assert.strictEqual(L.neighbor([a, b], a, 'right'), null);
});

check('dois monitores com escalas diferentes (100% e 150%), barra em cima: cada um no seu tamanho', () => {
  const a = disp(1, 0, 1920, 1080, 1, 'top');
  const b = { id: 2, bounds: { x: 1920, y: 0, width: 1707, height: 960 }, workArea: { x: 1920, y: 48, width: 1707, height: 912 }, scaleFactor: 1.5 };
  assert.strictEqual(L.pixelScale(a, 'auto'), 1);
  assert.strictEqual(L.pixelScale(b, 'auto'), 2);
  assert.strictEqual(L.neighbor([a, b], a, 'right'), b);
});

console.log(`layout: ${n} casos ok`);
