// Ponte segura entre a página da Kiara e o processo principal.
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('kiki', {
  init: () => ipcRenderer.invoke('kiki:init'),
  setMouseOverDog: (over) => ipcRenderer.send('kiki:mouse', over),
  leaveByEdge: (side, state) => ipcRenderer.invoke('kiki:edge', { side, state }),
  onSettings: (fn) => ipcRenderer.on('kiki:settings', (_e, s) => fn(s)),
  onEnter: (fn) => ipcRenderer.on('kiki:enter', (_e, info) => fn(info)),
  onBark: (fn) => ipcRenderer.on('kiki:bark', () => fn()),
});
