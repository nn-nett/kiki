// Onde fica a faixa da Kiara em cada monitor (contas puras, testáveis sem Windows).
//
// O Electron dá, por monitor: bounds (a tela inteira), workArea (a tela sem a barra de tarefas)
// e scaleFactor (escala do Windows: 1 = 100%, 1.5 = 150%...). Comparando bounds com workArea
// dá pra saber de que lado a barra está e qual a altura dela.

const CELL = 32;   // a Kiara tem 32x32 px de sprite

function taskbarSide(display) {
  const b = display.bounds, wa = display.workArea;
  if (wa.y > b.y) return 'top';
  if (wa.y + wa.height < b.y + b.height) return 'bottom';
  if (wa.x > b.x) return 'left';
  if (wa.x + wa.width < b.x + b.width) return 'right';
  return 'none';   // barra escondida automaticamente (ou sem barra)
}

// Altura da barra em px "lógicos" (DIP), só faz sentido com a barra em cima ou embaixo.
function taskbarHeight(display) {
  const b = display.bounds, wa = display.workArea;
  const side = taskbarSide(display);
  if (side === 'top') return wa.y - b.y;
  if (side === 'bottom') return b.y + b.height - (wa.y + wa.height);
  return 0;
}

// Px de tela (físicos) por px do sprite: sempre inteiro, pra não borrar o pixel art.
// zoom 'auto': barra em cima = maior tamanho que cabe na altura da barra (ela não pode passar
// do topo da tela); nos outros casos, 2x. zoom 1/2/3 = forçado pelo menu da bandeja.
function pixelScale(display, zoom) {
  const sf = display.scaleFactor || 1;
  if (zoom === 'auto') {
    if (taskbarSide(display) === 'top') {
      const barPhys = Math.round(taskbarHeight(display) * sf);
      return Math.max(1, Math.floor(barPhys / CELL));
    }
    return Math.max(1, Math.round(2 * sf));
  }
  return Math.max(1, Math.round(zoom * sf));
}

// Retângulo (DIP) da faixa transparente. As patas ficam na borda de baixo da faixa.
// - Barra em cima: borda de baixo da faixa = borda de baixo da barra (ela pisa na fronteira
//   entre a barra e as janelas, com o corpo dentro da barra).
// - Barra embaixo: borda de baixo da faixa = topo da barra (ela anda em cima da barra).
// - Barra do lado ou escondida: no pé da tela (fallback).
function stripBounds(display, zoom) {
  const wa = display.workArea, sf = display.scaleFactor || 1;
  const height = Math.ceil(CELL * pixelScale(display, zoom) / sf);
  const side = taskbarSide(display);
  const floor = side === 'top' ? wa.y : wa.y + wa.height;
  return { x: wa.x, y: floor - height, width: wa.width, height };
}

// "Lado do chão" pra decidir se dois monitores se ligam: em cima ou embaixo.
const floorSide = (display) => taskbarSide(display) === 'top' ? 'top' : 'bottom';

// Monitor colado à esquerda/direita deste, com sobreposição vertical e barra do mesmo lado.
function neighbor(displays, display, side) {
  const b = display.bounds;
  return displays.find(d => {
    if (d.id === display.id) return false;
    const o = d.bounds;
    const touches = side === 'right' ? o.x === b.x + b.width : o.x + o.width === b.x;
    const overlap = o.y < b.y + b.height && o.y + o.height > b.y;
    return touches && overlap && floorSide(d) === floorSide(display);
  }) || null;
}

module.exports = { CELL, taskbarSide, taskbarHeight, pixelScale, stripBounds, neighbor };
