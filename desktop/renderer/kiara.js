// Kiara Pixel Pal — a cachorrinha em si: "cérebro" (máquina de estados) + desenho.
//
// Lê a folha de sprites e o JSON exportados em sprites/final/ (formato descrito em
// sprites/final/README.md). Tudo em "px do sprite": a Kiara tem 32x32 e cada px do
// sprite vira `scale` px de tela (sempre inteiro, sem suavização).

const CELL = 32;

// Cérebro: igual ao da simulação aprovada (sprites/tools/sim_template.html, objeto BRAIN).
// dur = quanto tempo fica no estado (ms, sorteado entre os dois); null = até a animação acabar.
// Estados cuja animação ainda não está na folha final são ignorados automaticamente
// (ex.: "correndo" entra sozinho quando for aprovado e exportado).
const BRAIN = {
  parada:          { anim: 'parada',           dur: [1500, 4000], next: { andando: .50, latindo: .20, parada: .15, correndo: .15 } },
  andando:         { anim: 'andando',          dur: [2500, 7000], next: { parada: .35, andandoLatindo: .25, latindo: .15, meiaVolta: .10, correndo: .15 } },
  latindo:         { anim: 'latindo',          dur: null,         next: { parada: .5, andando: .5 } },
  andandoLatindo:  { anim: 'latindo_andando',  dur: null,         next: { andando: .6, parada: .4 } },
  correndo:        { anim: 'correndo',         dur: [1200, 3000], next: { ofegante: .5, andandoOfegante: .2, andando: .2, latindo: .1 } },
  ofegante:        { anim: 'ofegante',         dur: [2500, 5000], next: { parada: .5, andando: .3, andandoOfegante: .2 } },
  andandoOfegante: { anim: 'andando_ofegante', dur: [2000, 4500], next: { andando: .6, parada: .4 } },
};

const canvas = document.getElementById('stage');
const ctx = canvas.getContext('2d');

let sheet = null;        // JSON da folha
let sheetImg = null;     // imagem da folha
let alpha = null;        // canal alfa da folha (pra saber se o mouse está em cima dela)
let settings = { scale: 2, contorno: false, neighbors: { left: false, right: false } };
let W = 0;               // largura da faixa em px do sprite

const dog = {
  active: false, crossing: false,
  x: 40, dir: 1, state: 'parada', until: 0,
  frameI: 0, frameT: 0, cycles: 0,
};
let blink = null;       // piscar: { frames, imgs, imgsEsq, intervalo } (expressão por cima de qualquer animação)
const blinkClock = { i: -1, t: 0, next: 0 };
let lastDrawn = null;    // retângulo desenhado por último (pra limpar só ele)
let mouse = null;        // última posição do mouse (px CSS)
let overDog = false;

// ---------- utilidades ----------
const rnd = (a, b) => a + Math.random() * (b - a);
const hasAnim = (name) => !!(sheet && sheet.animations[name]);
const available = (state) => state === 'meiaVolta' ? available('andando') : !!BRAIN[state] && hasAnim(BRAIN[state].anim);

function pick(weights) {
  const ok = Object.entries(weights).filter(([k]) => available(k));
  const total = ok.reduce((t, [, w]) => t + w, 0);
  let r = Math.random() * total;
  for (const [k, w] of ok) { if ((r -= w) < 0) return k; }
  return ok.length ? ok[0][0] : 'parada';
}

// Nome da variante na folha: andando, andando_esquerda, andando_contorno, andando_contorno_esquerda...
function animName(state = dog.state) {
  let name = BRAIN[state].anim;
  if (settings.contorno && hasAnim(name + '_contorno')) name += '_contorno';
  if (dog.dir < 0 && hasAnim(name + '_esquerda')) name += '_esquerda';
  return name;
}
const currentAnim = () => sheet.animations[animName()];

// ---------- estados ----------
function setState(name, now = performance.now()) {
  if (name === 'meiaVolta') { dog.dir *= -1; name = 'andando'; }
  if (!available(name)) name = 'parada';
  dog.state = name;
  dog.frameI = 0;
  dog.frameT = now;
  const b = BRAIN[name];
  dog.until = b.dur ? now + rnd(...b.dur) : Infinity;
  dog.cycles = name === 'latindo' && Math.random() < .4 ? 2 : 1;   // às vezes late duas vezes seguidas
}

function bark() {
  if (dog.active && !dog.crossing) setState('latindo');
}

// ---------- tempo ----------
function tick(now) {
  if (!dog.active || dog.crossing) return;
  let anim = currentAnim();
  let d = anim.frames[dog.frameI].duration_ms;
  while (now - dog.frameT >= d) {
    dog.frameT += d;
    dog.frameI++;
    dog.x += anim.step_px || 0;   // as patas recuam isso por frame: andando assim ela não "patina"
    if (dog.frameI >= anim.frames.length) {
      dog.frameI = 0;
      if (BRAIN[dog.state].dur === null && --dog.cycles <= 0) { setState(pick(BRAIN[dog.state].next), now); }
    }
    if (checkEdges()) return;
    anim = currentAnim();
    d = anim.frames[dog.frameI].duration_ms;
  }
  if (now >= dog.until) setState(pick(BRAIN[dog.state].next), now);
  tickBlink(now);
}

// Piscar: relógio próprio, independente do que o corpo está fazendo.
function tickBlink(now) {
  if (!blink) return;
  if (blinkClock.i < 0) {
    if (now >= blinkClock.next) { blinkClock.i = 0; blinkClock.t = now; }
    return;
  }
  while (blinkClock.i >= 0 && now - blinkClock.t >= blink.frames[blinkClock.i].duration_ms) {
    blinkClock.t += blink.frames[blinkClock.i].duration_ms;
    if (++blinkClock.i >= blink.frames.length) { blinkClock.i = -1; blinkClock.next = now + rnd(...blink.intervalo); }
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
  window.kiki.leaveByEdge(side, dog.state).then((crossed) => {
    dog.crossing = false;
    if (crossed) { dog.active = false; draw(); } else { turn(); dog.frameT = performance.now(); }
  });
  return true;
}

// ---------- desenho ----------
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
  if (!dog.active || !sheetImg) return;
  const f = currentAnim().frames[dog.frameI];
  const r = dogRect();   // patas na última linha da célula = encostadas no topo da barra
  ctx.drawImage(sheetImg, f.x, f.y, f.w, f.h, r.x, r.y, r.w, r.h);
  if (blink && blinkClock.i >= 0 && f.olho) {   // remendo do olho (null = a animação já mexe no olho)
    const img = (dog.dir < 0 ? blink.imgsEsq : blink.imgs)[blinkClock.i], P = settings.scale;
    ctx.drawImage(img, r.x + f.olho[0] * P, r.y + f.olho[1] * P, img.width * P, img.height * P);
  }
  lastDrawn = r;
}

function loop(now) {
  tick(now);
  draw();
  updateHover();
  requestAnimationFrame(loop);
}

// ---------- mouse ----------
// A janela ocupa a largura toda da tela; só a Kiara deve "segurar" o clique.
// Confere o pixel do sprite sob o mouse (com 1 px de folga, porque as pernas são finas).
function isOverDog(mx, my) {
  if (!dog.active || !alpha) return false;
  const dpr = window.devicePixelRatio || 1, P = settings.scale, r = dogRect();
  const sx = Math.floor((mx * dpr - r.x) / P), sy = Math.floor((my * dpr - r.y) / P);
  if (sx < -1 || sy < -1 || sx > CELL || sy > CELL) return false;
  const f = currentAnim().frames[dog.frameI];
  for (let dy = -1; dy <= 1; dy++) for (let dx = -1; dx <= 1; dx++) {
    const px = sx + dx, py = sy + dy;
    if (px < 0 || py < 0 || px >= f.w || py >= f.h) continue;
    if (alpha[(f.y + py) * sheetImg.width + f.x + px] > 0) return true;
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
    img.onerror = reject;
    img.src = url;
  });
}

async function start() {
  const init = await window.kiki.init();
  if (!init) return;
  sheet = init.sheet;
  settings = init.settings;
  sheetImg = await loadImage(init.sheetUrl);
  const piscar = sheet.expressoes && sheet.expressoes.piscar;
  if (piscar) {
    try {
      const load = (f) => loadImage(new URL(f, init.baseUrl).href);
      blink = {
        frames: piscar.frames,
        intervalo: piscar.intervalo_ms,
        imgs: await Promise.all(piscar.frames.map(f => load(f.img))),
        imgsEsq: await Promise.all(piscar.frames.map(f => load(f.img_esquerda || f.img))),
      };
      blinkClock.next = performance.now() + rnd(...blink.intervalo);
    } catch { blink = null; }   // sem os remendos ela só não pisca
  }

  const c = document.createElement('canvas');
  c.width = sheetImg.width; c.height = sheetImg.height;
  const cx = c.getContext('2d', { willReadFrequently: true });
  cx.drawImage(sheetImg, 0, 0);
  const data = cx.getImageData(0, 0, c.width, c.height).data;
  alpha = new Uint8Array(c.width * c.height);
  for (let i = 0; i < alpha.length; i++) alpha[i] = data[i * 4 + 3];

  resize();
  if (init.active) {
    dog.active = true;
    dog.x = Math.floor(rnd(CELL, Math.max(CELL + 1, W - 2 * CELL)));
    dog.dir = Math.random() < .5 ? 1 : -1;
    setState('parada');
  }

  window.kiki.onSettings((s) => { settings = s; resize(); });
  window.kiki.onBark(bark);
  window.kiki.onEnter(({ from, state }) => {
    dog.active = true;
    dog.dir = from === 'left' ? 1 : -1;
    dog.x = from === 'left' ? -CELL : W;
    setState(BRAIN[state] && BRAIN[state].dur !== null && state !== 'parada' ? state : 'andando');
  });

  requestAnimationFrame(loop);
}

start();
