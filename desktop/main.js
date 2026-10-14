// Kiara Pixel Pal — processo principal (Electron).
//
// Ideia geral: uma janela transparente, sem borda, do tamanho de uma "faixa"
// logo acima da barra de tarefas, em CADA monitor. A Kiara é desenhada dentro
// dessa faixa (renderer/kiara.js). A janela deixa os cliques passarem pro que
// está atrás dela, menos quando o mouse está em cima da Kiara.
//
// Só um monitor "tem" a Kiara por vez. Quando ela sai pela borda de um monitor
// e existe outro monitor colado daquele lado, ela passa pra lá.

const { app, BrowserWindow, screen, Tray, Menu, ipcMain, nativeImage, nativeTheme } = require('electron');
const { execFile } = require('child_process');
const path = require('path');
const fs = require('fs');
const { pathToFileURL } = require('url');

const CELL = 32;   // tamanho nativo do sprite (32x32)

// ---------- onde estão os sprites ----------
// Em desenvolvimento lê direto de sprites/final/ (o que a sessão de sprites exporta).
// No .exe empacotado, o electron-builder copia esses arquivos pra resources/sprites.
const SPRITES_DIR = app.isPackaged
  ? path.join(process.resourcesPath, 'sprites')
  : path.join(__dirname, '..', 'sprites', 'final');
const SHEET_PNG = path.join(SPRITES_DIR, 'kiara-sprites.png');
const SHEET_JSON = path.join(SPRITES_DIR, 'kiara-sprites.json');

// ---------- preferências (salvas entre execuções) ----------
const CONFIG_FILE = path.join(app.getPath('userData'), 'config.json');
const DEFAULTS = { zoom: 2, contorno: 'auto', visivel: true };
let config = { ...DEFAULTS };
try { config = { ...DEFAULTS, ...JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf8')) }; } catch { /* primeira vez */ }
function saveConfig() {
  try { fs.writeFileSync(CONFIG_FILE, JSON.stringify(config, null, 2)); } catch { /* sem problema */ }
}

// ---------- estado ----------
const windows = new Map();   // display.id -> BrowserWindow
let activeDisplayId = null;  // monitor onde a Kiara está agora
let tray = null;
let taskbarDark = nativeTheme.shouldUseDarkColors;

// ---------- tema da barra de tarefas ----------
// A cor da barra do Windows segue o "modo do Windows" (SystemUsesLightTheme),
// que pode ser diferente do "modo dos apps". Lê do registro; se falhar, usa o tema dos apps.
function readTaskbarTheme() {
  if (process.platform !== 'win32') { setTaskbarDark(nativeTheme.shouldUseDarkColors); return; }
  execFile('reg', ['query', 'HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize', '/v', 'SystemUsesLightTheme'],
    { windowsHide: true }, (err, out) => {
      const m = !err && /SystemUsesLightTheme\s+REG_DWORD\s+0x([0-9a-f]+)/i.exec(out);
      setTaskbarDark(m ? parseInt(m[1], 16) === 0 : nativeTheme.shouldUseDarkColors);
    });
}
function setTaskbarDark(dark) {
  if (dark === taskbarDark) return;
  taskbarDark = dark;
  broadcastSettings();
}
function useOutline() {
  return config.contorno === 'auto' ? taskbarDark : config.contorno === 'sim';
}

// ---------- geometria ----------
// Px de tela (físicos) por px do sprite: sempre inteiro, pra não borrar o pixel art
// mesmo com escala do Windows em 125%/150%.
function pixelScale(display) {
  return Math.max(1, Math.round(config.zoom * display.scaleFactor));
}

// A faixa fica com a base encostada no topo da barra de tarefas (fim da "área de trabalho").
function stripBounds(display) {
  const wa = display.workArea;
  const height = Math.ceil(CELL * pixelScale(display) / display.scaleFactor);
  return { x: wa.x, y: wa.y + wa.height - height, width: wa.width, height };
}

// Monitor colado à esquerda/direita deste (com alguma sobreposição vertical).
function neighbor(display, side) {
  const b = display.bounds;
  return screen.getAllDisplays().find(d => {
    if (d.id === display.id) return false;
    const o = d.bounds;
    const touches = side === 'right' ? o.x === b.x + b.width : o.x + o.width === b.x;
    const overlap = o.y < b.y + b.height && o.y + o.height > b.y;
    return touches && overlap;
  }) || null;
}

function settingsFor(display) {
  return {
    scale: pixelScale(display),
    contorno: useOutline(),
    neighbors: { left: !!neighbor(display, 'left'), right: !!neighbor(display, 'right') },
  };
}

function broadcastSettings() {
  for (const d of screen.getAllDisplays()) {
    const win = windows.get(d.id);
    if (win && !win.isDestroyed()) win.webContents.send('kiki:settings', settingsFor(d));
  }
}

// ---------- janelas ----------
function createWindow(display) {
  const win = new BrowserWindow({
    ...stripBounds(display),
    transparent: true,
    frame: false,
    resizable: false,
    movable: false,
    minimizable: false,
    maximizable: false,
    skipTaskbar: true,
    focusable: false,
    hasShadow: false,
    alwaysOnTop: true,
    show: false,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
      backgroundThrottling: false,
    },
  });
  win.setAlwaysOnTop(true, 'screen-saver');   // acima da barra de tarefas
  win.setIgnoreMouseEvents(true, { forward: true });
  win.loadFile(path.join(__dirname, 'renderer', 'index.html'));
  win.once('ready-to-show', () => { if (config.visivel) win.showInactive(); });
  win.displayId = display.id;
  windows.set(display.id, win);
  return win;
}

function rebuildWindows() {
  for (const win of windows.values()) if (!win.isDestroyed()) win.destroy();
  windows.clear();
  const displays = screen.getAllDisplays();
  if (!displays.some(d => d.id === activeDisplayId)) activeDisplayId = screen.getPrimaryDisplay().id;
  for (const d of displays) createWindow(d);
}

function displayOf(event) {
  const win = BrowserWindow.fromWebContents(event.sender);
  return win && screen.getAllDisplays().find(d => d.id === win.displayId);
}

// ---------- conversa com a página (renderer) ----------
ipcMain.handle('kiki:init', (event) => {
  const display = displayOf(event);
  if (!display) return null;
  return {
    sheetUrl: pathToFileURL(SHEET_PNG).href,
    sheet: JSON.parse(fs.readFileSync(SHEET_JSON, 'utf8')),
    settings: settingsFor(display),
    active: display.id === activeDisplayId,
  };
});

// Mouse em cima da Kiara: a janela passa a receber cliques; fora dela, cliques atravessam.
ipcMain.on('kiki:mouse', (event, overDog) => {
  const win = BrowserWindow.fromWebContents(event.sender);
  if (win) win.setIgnoreMouseEvents(!overDog, { forward: true });
});

// Ela saiu pela borda. Se houver monitor vizinho, passa pra ele e responde true.
ipcMain.handle('kiki:edge', (event, { side, state }) => {
  const display = displayOf(event);
  const next = display && neighbor(display, side);
  const target = next && windows.get(next.id);
  if (!target || target.isDestroyed()) return false;
  activeDisplayId = next.id;
  target.webContents.send('kiki:enter', { from: side === 'right' ? 'left' : 'right', state });
  return true;
});

// ---------- bandeja (ícone perto do relógio) ----------
function trayIcon() {
  try {
    const sheet = JSON.parse(fs.readFileSync(SHEET_JSON, 'utf8'));
    const f = sheet.animations.parada.frames[0];
    return nativeImage.createFromPath(SHEET_PNG).crop({ x: f.x, y: f.y, width: f.w, height: f.h });
  } catch {
    return nativeImage.createEmpty();
  }
}

function buildTrayMenu() {
  const setZoom = (z) => { config.zoom = z; saveConfig(); rebuildWindows(); buildTrayMenu(); };
  const setOutline = (c) => { config.contorno = c; saveConfig(); broadcastSettings(); buildTrayMenu(); };
  const menu = Menu.buildFromTemplate([
    { label: 'Kiara 🐕', enabled: false },
    { type: 'separator' },
    {
      label: config.visivel ? 'Esconder a Kiara' : 'Mostrar a Kiara',
      click: () => { config.visivel = !config.visivel; saveConfig(); applyVisibility(); buildTrayMenu(); },
    },
    { label: 'Latir!', click: () => windows.get(activeDisplayId)?.webContents.send('kiki:bark') },
    {
      label: 'Tamanho',
      submenu: [1, 2, 3].map(z => ({ label: `${z}x`, type: 'radio', checked: config.zoom === z, click: () => setZoom(z) })),
    },
    {
      label: 'Contorno grisalho',
      submenu: [
        { label: 'Automático (barra escura = com contorno)', type: 'radio', checked: config.contorno === 'auto', click: () => setOutline('auto') },
        { label: 'Sempre', type: 'radio', checked: config.contorno === 'sim', click: () => setOutline('sim') },
        { label: 'Nunca', type: 'radio', checked: config.contorno === 'nao', click: () => setOutline('nao') },
      ],
    },
    {
      label: 'Abrir junto com o Windows',
      type: 'checkbox',
      checked: app.getLoginItemSettings().openAtLogin,
      click: (item) => app.setLoginItemSettings({ openAtLogin: item.checked }),
    },
    { type: 'separator' },
    { label: 'Sair', click: () => app.quit() },
  ]);
  tray.setContextMenu(menu);
}

function applyVisibility() {
  for (const win of windows.values()) {
    if (win.isDestroyed()) continue;
    if (config.visivel) win.showInactive(); else win.hide();
  }
}

// ---------- inicialização ----------
if (!app.requestSingleInstanceLock()) {
  app.quit();
} else {
  app.whenReady().then(() => {
    activeDisplayId = screen.getPrimaryDisplay().id;
    rebuildWindows();

    tray = new Tray(trayIcon());
    tray.setToolTip('Kiara Pixel Pal');
    tray.on('click', () => { config.visivel = !config.visivel; saveConfig(); applyVisibility(); buildTrayMenu(); });
    buildTrayMenu();

    readTaskbarTheme();
    nativeTheme.on('updated', readTaskbarTheme);
    setInterval(readTaskbarTheme, 60 * 1000);

    // A barra do Windows às vezes "sobe" por cima de outras janelas; reafirma o topo de vez em quando.
    setInterval(() => {
      for (const win of windows.values()) if (!win.isDestroyed()) win.setAlwaysOnTop(true, 'screen-saver');
    }, 10 * 1000);

    // Monitor ligado/desligado, resolução ou barra mudaram: refaz as faixas.
    let pending = null;
    const onDisplaysChanged = () => { clearTimeout(pending); pending = setTimeout(rebuildWindows, 500); };
    screen.on('display-added', onDisplaysChanged);
    screen.on('display-removed', onDisplaysChanged);
    screen.on('display-metrics-changed', onDisplaysChanged);
  });

  // Fechar as janelas não fecha o app: ele vive na bandeja até "Sair".
  app.on('window-all-closed', () => {});
}
