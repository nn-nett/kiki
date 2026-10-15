// Kiara Pixel Pal — a cachorrinha em si: "cérebro" + desenho por camadas.
//
// Cada quadro é MONTADO na hora (renderer/compose.js): corpo + cabeça + olho do piscar,
// a partir das camadas exportadas em sprites/final/ (ver sprites/final/README.md, "Camadas").
// Três relógios independentes:
//   - corpo: parada, andando, latindo (com o tranco no tronco), ofegante parada
//   - cabeça por cima do corpo: normal, "latir" (1 ou 2 latidos) ou "ofegante" (enquanto cansada)
//   - piscar: sempre ligado, por cima de tudo, a cada 2,5-7 s
// Tudo em "px do sprite": a Kiara tem 32x32 e cada px do sprite vira `scale` px de tela.

const { CELL, compose } = window.KiaraCompose;

// ======================================================================================
// CÉREBRO — todos os números de comportamento num lugar só (documentados no README).
// Tempos em milissegundos; [a, b] = sorteado entre a e b.
// ======================================================================================
const BRAIN = {
  // Corpo: quanto tempo fica em cada estado e o que pode vir depois (chances somam 1).
  parada:  { dur: [2000, 5000], next: { andando: .55, latir: .20, meiaVolta: .15, parada: .10 } },
  andando: { dur: [3000, 8000], next: { parada: .60, meiaVolta: .20, pararELatir: .20 } },
  pausaAntesDeLatir: [400, 900],      // pausa curta parada antes de latir
  // Latido: quantos AU! por vez e o intervalo mínimo entre um latido e outro.
  latidos: { 1: .6, 2: .4 },
  intervaloEntreLatidos: 6000,
  latirAndandoMediaMs: 17000,         // andando, em média 1 latido a cada ~17 s
  // Cansaço (no lugar da corrida, que ainda não foi aprovada): um medidor em segundos.
  cansaco: {
    sobeAndando: 1,                   // +1 por segundo andando
    descendoParada: 0.5,              // -0,5 por segundo parada
    limite: 20,                       // passou de ~20 s de caminhada somados: fica ofegante
    ofeganteDur: [3000, 6000],
    continuaAndando: .5,              // chance de ficar ofegante andando (senão para, ofegante)
  },
  // Piscar: intervalo vem do JSON (expressoes.piscar.intervalo_ms); este é o padrão se faltar.
  piscarIntervalo: [2500, 7000],
};

const canvas = document.getElementById('stage');
const ctx = canvas.getContext('2d');
const cellCanvas = document.createElement('canvas');   // quadro 32x32 montado
cellCanvas.width = CELL; cellCanvas.height = CELL;
const cellCtx = cellCanvas.getContext('2d');

let lib = null;          // camadas carregadas: { corpos, cabecas, expressoesCabeca, piscar }
let settings = { scale: 2, contorno: false, neighbors: { left: false, right: false } };
let W = 0;               // largura da faixa em px do sprite

const dog = {
  active: false, crossing: false,
  x: 40, dir: 1,
  body: 'parada', bodyI: 0, bodyT: 0, until: 0,
  barkFrames: 0,         // quantos frames do corpo "latindo" tocar (1 + 3 por latido)
  head: null,            // expressão de cabeça: { name, i, t, end }
  afterPause: null,      // 'latir' = a pausa atual termina num latido
  lastBarkAt: -Infinity,
  fatigue: 0,            // medidor de cansaço (s)
  tiredUntil: 0,         // > agora = está ofegante
};
const blinkClock = { i: -1, t: 0, next: 0 };
let lastNow = 0;
let lastDrawn = null;    // retângulo desenhado por último (pra limpar só ele)
let lastCell = null;     // último quadro montado (pra saber se o mouse está em cima dela)
let mouse = null;        // última posição do mouse (px CSS)
let overDog = false;

// ---------- utilidades ----------
const rnd = (a, b) => a + Math.random() * (b - a);
const isTired = (now) => now < dog.tiredUntil;
const canBark = (now) => now - dog.lastBarkAt >= BRAIN.intervaloEntreLatidos;
const hasBody = (name) => !!(lib && lib.corpos[name]);
const hasHead = (name) => !!(lib && lib.expressoesCabeca[name]);

function pick(weights) {
  const entries = Object.entries(weights);
  let r = Math.random() * entries.reduce((t, [, w]) => t + w, 0);
  for (const [k, w] of entries) { if ((r -= w) < 0) return k; }
  return entries[0][0];
}
const pickBarks = () => Number(pick(BRAIN.latidos));

// ---------- corpo ----------
function setBody(name, now, until) {
  if (!hasBody(name)) name = 'parada';
  dog.body = name;
  dog.bodyI = 0;
  dog.bodyT = now;
  const b = BRAIN[name];
  dog.until = until !== undefined ? until : b ? now + rnd(...b.dur) : Infinity;
}

// Late parada: corpo "latindo" (preparação 300 ms → AU! → volta; 2º latido opcional).
function barkStanding(now, n = pickBarks()) {
  const frames = lib.corpos.latindo.frames.length;
  setBody('latindo', now, Infinity);
  dog.barkFrames = Math.min(frames, 1 + 3 * n);
  dog.head = null;
  dog.afterPause = null;
}

// Late andando: só a cabeça late, as pernas continuam.
function barkWalking(now, n = pickBarks()) {
  const frames = lib.expressoesCabeca.latir.frames.length;
  dog.head = { name: 'latir', i: 0, t: now, end: Math.min(frames, 3 * n) };
}

function startTired(now) {
  dog.tiredUntil = now + rnd(...BRAIN.cansaco.ofeganteDur);
  if (dog.body === 'andando' && Math.random() < BRAIN.cansaco.continuaAndando) {
    dog.until = Math.max(dog.until, dog.tiredUntil);   // continua andando, ofegante
    dog.head = { name: 'ofegante', i: 0, t: now };
  } else {
    restTired(now);
  }
}

// Ofegante parada: usa o corpo "ofegante" (peito mexendo) se existir; senão parada + cabeça ofegante.
function restTired(now) {
  if (hasBody('ofegante')) { setBody('ofegante', now, dog.tiredUntil); dog.head = null; }
  else { setBody('parada', now, dog.tiredUntil); dog.head = { name: 'ofegante', i: 0, t: now }; }
}

function endTired(now) {
  dog.tiredUntil = 0;
  dog.fatigue = 0;
  if (dog.head && dog.head.name === 'ofegante') dog.head = null;
  if (dog.body === 'ofegante') setBody('parada', now);
}

function endBark(now) {
  dog.lastBarkAt = now;
  if (isTired(now)) {
    if (dog.body === 'latindo') restTired(now);
    else if (hasHead('ofegante')) dog.head = { name: 'ofegante', i: 0, t: now };
  } else if (dog.body === 'latindo') {
    setBody(Math.random() < .3 ? 'andando' : 'parada', now);
  }
}

// O tempo do estado acabou: decide o próximo.
function decide(now) {
  if (dog.afterPause === 'latir') { barkStanding(now); return; }
  const from = dog.body === 'andando' ? 'andando' : 'parada';
  let next = pick(BRAIN[from].next);
  if ((next === 'latir' || next === 'pararELatir') && !canBark(now)) next = 'parada';
  switch (next) {
    case 'latir': barkStanding(now); break;
    case 'pararELatir':
      setBody('parada', now, now + rnd(...BRAIN.pausaAntesDeLatir));
      dog.afterPause = 'latir';
      break;
    case 'meiaVolta': dog.dir *= -1; setBody('andando', now); break;
    default: setBody(next, now);
  }
}

// Clique nela = late, no corpo em que estiver.
function bark(now = performance.now()) {
  if (!dog.active || dog.crossing || dog.body === 'latindo') return;
  if (dog.head && dog.head.name === 'latir') return;
  if (dog.body === 'andando') barkWalking(now);
  else barkStanding(now);
}

// ---------- relógios ----------
function tick(now) {
  const dt = Math.min(1000, Math.max(0, now - lastNow));
  lastNow = now;
  if (!dog.active || dog.crossing || !lib) return;

  // 1) corpo
  let body = lib.corpos[dog.body];
  let d = body.frames[dog.bodyI].duration_ms;
  while (now - dog.bodyT >= d) {
    dog.bodyT += d;
    dog.bodyI++;
    dog.x += (body.step_px || 0) * dog.dir;   // as patas recuam isso por frame: ela não "patina"
    if (dog.body === 'latindo' && dog.bodyI >= dog.barkFrames) { dog.bodyI = 0; endBark(now); }
    else if (dog.bodyI >= body.frames.length) dog.bodyI = 0;
    if (checkEdges()) return;
    body = lib.corpos[dog.body];
    d = body.frames[dog.bodyI].duration_ms;
  }

  // 2) cabeça (não vale durante o corpo "latindo", que já tem a cabeça do latido)
  if (dog.head && dog.body !== 'latindo') {
    const ex = lib.expressoesCabeca[dog.head.name];
    let hd = ex.frames[dog.head.i].duration_ms;
    while (dog.head && now - dog.head.t >= hd) {
      dog.head.t += hd;
      dog.head.i++;
      const end = dog.head.end || ex.frames.length;
      if (dog.head.i >= end) {
        if (ex.loop) dog.head.i = 0;
        else { dog.head = null; endBark(now); break; }
      }
      hd = ex.frames[dog.head.i].duration_ms;
    }
  }

  // 3) cansaço: sobe andando, desce parada; passou do limite, fica ofegante
  const c = BRAIN.cansaco;
  if (!isTired(now)) {
    dog.fatigue = Math.max(0, dog.fatigue + (dog.body === 'andando' ? c.sobeAndando : -c.descendoParada) * dt / 1000);
    if (dog.fatigue >= c.limite && dog.body !== 'latindo' && !dog.head && !dog.afterPause && hasHead('ofegante')) startTired(now);
  }

  // 4) latir andando, de vez em quando
  if (dog.body === 'andando' && !dog.head && !isTired(now) && canBark(now) && Math.random() < dt / BRAIN.latirAndandoMediaMs) {
    barkWalking(now);
  }

  if (dog.tiredUntil && now >= dog.tiredUntil) endTired(now);   // descansou: medidor zera
  if (now >= dog.until) decide(now);
  tickBlink(now);
}

// Piscar: relógio próprio, independente do resto.
function tickBlink(now) {
  if (!lib.piscar) return;
  if (blinkClock.i < 0) {
    if (now >= blinkClock.next) { blinkClock.i = 0; blinkClock.t = now; }
    return;
  }
  const fr = lib.piscar.frames;
  while (blinkClock.i >= 0 && now - blinkClock.t >= fr[blinkClock.i].duration_ms) {
    blinkClock.t += fr[blinkClock.i].duration_ms;
    if (++blinkClock.i >= fr.length) { blinkClock.i = -1; blinkClock.next = now + rnd(...lib.piscar.intervalo); }
  }
}

// Chegou na ponta da barra: passa pro monitor vizinho (se houver) ou dá meia-volta.
// Com vizinho, ela anda até sumir pela borda; sem vizinho, vira um pouquinho antes.
function checkEdges() {
  const right = settings.neighbors.right ? W : W - CELL - 2;
  const left = settings.neighbors.left ? -CELL : 2;
  let side = null;
  if (dog.dir > 0 && dog.x >= right) side = 'right';
  if (dog.dir < 0 && dog.x <= left) side = 'left';
  if (!side) return false;

  const turn = () => { dog.x = Math.max(2, Math.min(dog.x, W - CELL - 2)); dog.dir *= -1; };
  if (!settings.neighbors[side]) { turn(); return false; }

  dog.crossing = true;
  window.kiki.leaveByEdge(side, dog.body).then((crossed) => {
    dog.crossing = false;
    if (crossed) { dog.active = false; draw(); } else { turn(); dog.bodyT = performance.now(); }
  });
  return true;
}

// ---------- desenho ----------
function currentCell() {
  const corpo = lib.corpos[dog.body].frames[dog.bodyI];
  let cabeca = null;
  if (dog.head && dog.body !== 'latindo') cabeca = lib.expressoesCabeca[dog.head.name].frames[dog.head.i];
  const olho = lib.piscar && blinkClock.i >= 0 ? lib.piscar.imgs[blinkClock.i] : null;
  return compose(lib, { corpo, cabeca, olho, contorno: settings.contorno, esquerda: dog.dir < 0 });
}

function resize() {
  const dpr = window.devicePixelRatio || 1;
  canvas.width = Math.round(window.innerWidth * dpr);
  canvas.height = Math.round(window.innerHeight * dpr);
  canvas.style.width = window.innerWidth + 'px';
  canvas.style.height = window.innerHeight + 'px';
  W = Math.floor(canvas.width / settings.scale);
  if (!settings.neighbors.right) dog.x = Math.min(dog.x, W - CELL - 2);
  ctx.imageSmoothingEnabled = false;
  lastDrawn = null;
  ctx.clearRect(0, 0, canvas.width, canvas.height);
}

function dogRect() {
  const P = settings.scale;
  return { x: dog.x * P, y: canvas.height - CELL * P, w: CELL * P, h: CELL * P };
}

function draw() {
  if (lastDrawn) ctx.clearRect(lastDrawn.x, lastDrawn.y, lastDrawn.w, lastDrawn.h);
  lastDrawn = null;
  lastCell = null;
  if (!dog.active || !lib) return;
  const cell = currentCell();
  cellCtx.putImageData(new ImageData(cell.data, CELL, CELL), 0, 0);
  const r = dogRect();   // patas na última linha da célula = na borda de baixo da faixa
  ctx.drawImage(cellCanvas, 0, 0, CELL, CELL, r.x, r.y, r.w, r.h);
  lastDrawn = r;
  lastCell = cell;
}

function loop(now) {
  tick(now);
  draw();
  updateHover();
  requestAnimationFrame(loop);
}

// ---------- mouse ----------
// A janela ocupa a largura toda da tela; só a Kiara deve "segurar" o clique.
// Confere o pixel do quadro sob o mouse (com 1 px de folga, porque as pernas são finas).
function isOverDog(mx, my) {
  if (!dog.active || !lastCell) return false;
  const dpr = window.devicePixelRatio || 1, P = settings.scale, r = dogRect();
  const sx = Math.floor((mx * dpr - r.x) / P), sy = Math.floor((my * dpr - r.y) / P);
  for (let dy = -1; dy <= 1; dy++) for (let dx = -1; dx <= 1; dx++) {
    const px = sx + dx, py = sy + dy;
    if (px < 0 || py < 0 || px >= CELL || py >= CELL) continue;
    if (lastCell.data[(py * CELL + px) * 4 + 3] > 0) return true;
  }
  return false;
}

function updateHover() {
  const over = !!mouse && isOverDog(mouse.x, mouse.y);
  if (over === overDog) return;
  overDog = over;
  document.body.classList.toggle('over', over);
  window.kiki.setMouseOverDog(over);
}

window.addEventListener('mousemove', (e) => { mouse = { x: e.clientX, y: e.clientY }; });
window.addEventListener('mouseleave', () => { mouse = null; });
window.addEventListener('mousedown', (e) => { if (isOverDog(e.clientX, e.clientY)) bark(); });   // toque nela = late
window.addEventListener('resize', resize);

// ---------- início ----------
function loadImage(url) {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.onload = () => resolve(img);
    img.onerror = () => reject(new Error('não carregou ' + url));
    img.src = url;
  });
}

// Imagem → { w, h, data } (pixels RGBA), o formato do compose.js.
async function loadPixels(url) {
  const img = await loadImage(url);
  const c = document.createElement('canvas');
  c.width = img.width; c.height = img.height;
  const cx = c.getContext('2d', { willReadFrequently: true });
  cx.drawImage(img, 0, 0);
  return { w: img.width, h: img.height, data: cx.getImageData(0, 0, img.width, img.height).data };
}

async function loadLayers(sheet, baseUrl) {
  const url = (rel) => new URL(rel, baseUrl).href;
  const cam = sheet.camadas;
  const corpos = {};
  for (const [name, c] of Object.entries(cam.corpos)) {
    corpos[name] = { ...c, frames: await Promise.all(c.frames.map(async f => ({ ...f, img: await loadPixels(url(f.img)) }))) };
  }
  const cabecas = {};
  for (const [name, h] of Object.entries(cam.cabecas)) cabecas[name] = { ...h, img: await loadPixels(url(h.img)) };
  let piscar = null;
  const p = sheet.expressoes && sheet.expressoes.piscar;
  if (p) {
    try {
      piscar = { frames: p.frames, intervalo: p.intervalo_ms || BRAIN.piscarIntervalo, imgs: await Promise.all(p.frames.map(f => loadPixels(url(f.img)))) };
    } catch { piscar = null; }   // sem os remendos ela só não pisca
  }
  return { corpos, cabecas, expressoesCabeca: cam.expressoes_cabeca || {}, piscar };
}

async function start() {
  const init = await window.kiki.init();
  if (!init) return;
  settings = init.settings;
  lib = await loadLayers(init.sheet, init.baseUrl);
  if (lib.piscar) blinkClock.next = performance.now() + rnd(...lib.piscar.intervalo);

  resize();
  lastNow = performance.now();
  if (init.active) {
    dog.active = true;
    dog.x = Math.floor(rnd(CELL, Math.max(CELL + 1, W - 2 * CELL)));
    dog.dir = Math.random() < .5 ? 1 : -1;
    setBody('parada', lastNow);
  }

  window.kiki.onSettings((s) => { settings = s; resize(); });
  window.kiki.onBark(() => bark());
  window.kiki.onEnter(({ from }) => {
    const now = performance.now();
    dog.active = true;
    dog.dir = from === 'left' ? 1 : -1;
    dog.x = from === 'left' ? -CELL : W;
    dog.head = null;
    setBody('andando', now);
  });

  requestAnimationFrame(loop);
}

start();

// Pra depurar (página de demonstração e testes): acesso ao estado por fora.
window.kikiDebug = { dog, bark, BRAIN, blinkClock, setBody, barkStanding, barkWalking, startTired, isTired: () => isTired(performance.now()) };
