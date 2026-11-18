/* ==========================================================================
   keith-ui-settings.js — First-Party Vanilla ES6 Right-Side UI Kit Drawer
   Zero jQuery, zero external framework required. Works with any UI stack.
   ========================================================================== */

(function () {
  'use strict';

  const STORAGE_KEY = 'keith_ui_preferences_v1';

  const PRESET_SWATCHES = [
    { id: 'preset_1',  hex: '#5bcfc5', onInk: '#000000', label: 'Mint Teal' },
    { id: 'preset_2',  hex: '#6610f2', onInk: '#ffffff', label: 'Indigo' },
    { id: 'preset_3',  hex: '#0ea5e9', onInk: '#000000', label: 'Sky Blue' },
    { id: 'preset_4',  hex: '#4d06a5', onInk: '#ffffff', label: 'Deep Purple' },
    { id: 'preset_5',  hex: '#dc3545', onInk: '#ffffff', label: 'Crimson' },
    { id: 'preset_6',  hex: '#fd7e14', onInk: '#000000', label: 'Orange' },
    { id: 'preset_7',  hex: '#ffc107', onInk: '#000000', label: 'Amber' },
    { id: 'preset_8',  hex: '#18181b', onInk: '#ffffff', label: 'Obsidian' },
    { id: 'preset_9',  hex: '#20c997', onInk: '#000000', label: 'Emerald' },
    { id: 'preset_10', hex: '#17a2b8', onInk: '#000000', label: 'Cyan' },
    { id: 'preset_11', hex: '#94618e', onInk: '#ffffff', label: 'Plum' },
    { id: 'preset_12', hex: '#343a40', onInk: '#ffffff', label: 'Slate' },
    { id: 'preset_13', hex: '#2563eb', onInk: '#ffffff', label: 'Royal Blue' },
    { id: 'preset_14', hex: '#4885ed', onInk: '#000000', label: ' Cobalt' },
    { id: 'preset_15', hex: '#4cb32b', onInk: '#000000', label: 'Forest Green' },
  ];

  const DEFAULT_PREFERENCES = {
    theme: 'light',
    primary: 'preset_1',
    brand: 'preset_1',
    header: 'preset_1',
    sidebar: 'preset_1',
    layout: 'vertical',
    sidebarMode: 'full',
    container: 'fluid',
    font: 'Plus Jakarta Sans',
  };

  function readPreferences() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      return raw ? Object.assign({}, DEFAULT_PREFERENCES, JSON.parse(raw)) : Object.assign({}, DEFAULT_PREFERENCES);
    } catch (_err) {
      return Object.assign({}, DEFAULT_PREFERENCES);
    }
  }

  function savePreferences(nextPrefs) {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(nextPrefs));
    } catch (_err) {}
  }

  function findSwatch(presetId) {
    return PRESET_SWATCHES.find((item) => item.id === presetId) || PRESET_SWATCHES[0];
  }

  function applyPreferences(prefs) {
    const root = document.documentElement;
    root.setAttribute('data-ui-theme', prefs.theme);
    root.setAttribute('data-ui-primary', prefs.primary);
    root.setAttribute('data-ui-brand', prefs.brand);
    root.setAttribute('data-ui-header', prefs.header);
    root.setAttribute('data-ui-sidebar', prefs.sidebar);
    root.setAttribute('data-ui-layout', prefs.layout);
    root.setAttribute('data-ui-sidebar-mode', prefs.sidebarMode);
    root.setAttribute('data-ui-container', prefs.container);
    root.style.setProperty('--ui-font-sans', `"${prefs.font}", system-ui, -apple-system, sans-serif`);

    const applySurfaceToken = (regionKey, bgVar, inkVar) => {
      if (prefs[regionKey] === 'preset_1') {
        root.style.removeProperty(bgVar);
        root.style.removeProperty(inkVar);
        return;
      }
      const swatch = findSwatch(prefs[regionKey]);
      root.style.setProperty(bgVar, swatch.hex);
      root.style.setProperty(inkVar, swatch.onInk);
    };

    applySurfaceToken('brand', '--ui-brand-bg', '--on-brand');
    applySurfaceToken('header', '--ui-header-bg', '--on-header');
    applySurfaceToken('sidebar', '--ui-sidebar-bg', '--on-sidebar');
  }

  function mountSettingsDrawer() {
    if (document.getElementById('keithUiSettingsRoot')) return;
    let currentPrefs = readPreferences();
    applyPreferences(currentPrefs);

    const styleEl = document.createElement('style');
    styleEl.textContent = `
      .ui-settings-trigger{position:fixed;right:0;top:45%;z-index:1040;background:var(--ui-primary);color:var(--on-primary);border:none;border-radius:10px 0 0 10px;padding:10px 12px;cursor:pointer;font-weight:700;box-shadow:0 4px 14px rgba(0,0,0,.18)}
      .ui-settings-drawer{position:fixed;top:0;right:0;width:320px;max-width:90vw;height:100vh;z-index:1050;background:var(--ui-surface);color:var(--ui-ink);border-left:1px solid var(--ui-border);box-shadow:-8px 0 28px rgba(0,0,0,.18);transform:translateX(100%);transition:transform 180ms cubic-bezier(.23,1,.32,1);display:flex;flex-direction:column}
      .ui-settings-drawer[data-open="true"]{transform:translateX(0)}
      .ui-swatch-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:8px}
      .ui-swatch-btn{height:30px;border-radius:8px;border:2px solid rgba(0,0,0,.15);cursor:pointer}
      .ui-swatch-btn[aria-pressed="true"]{outline:2px solid var(--ui-ink);outline-offset:2px}
    `;
    document.head.appendChild(styleEl);

    const container = document.createElement('div');
    container.id = 'keithUiSettingsRoot';
    container.className = 'no-print';

    const buildSwatchGroup = (field) =>
      PRESET_SWATCHES.map(
        (s) =>
          `<button type="button" class="ui-swatch-btn" data-pref-field="${field}" data-pref-val="${s.id}" aria-label="${s.label}" aria-pressed="${currentPrefs[field] === s.id}" style="background:${s.hex}"></button>`
      ).join('');

    container.innerHTML = `
      <button type="button" class="ui-settings-trigger" id="keithUiOpenBtn" aria-label="Open Theme Settings">Theme</button>
      <aside class="ui-settings-drawer" id="keithUiDrawer" data-open="false" aria-label="Theme Settings">
        <div style="padding:16px;border-bottom:1px solid var(--ui-border);display:flex;justify-content:space-between;align-items:center">
          <strong style="font-size:1rem">Theme & Layout Settings</strong>
          <button type="button" id="keithUiCloseBtn" class="ui-btn ui-btn-soft" style="padding:4px 10px">Close</button>
        </div>
        <div style="padding:16px;overflow-y:auto;flex:1;display:flex;flex-direction:column;gap:16px;font-size:.875rem">
          <div>
            <label for="keithUiThemeSelect" style="display:block;font-weight:700;margin-bottom:6px">Color Mode</label>
            <select id="keithUiThemeSelect" data-pref-select="theme" style="width:100%;padding:8px;border-radius:8px;border:1px solid var(--ui-border);background:var(--ui-surface);color:var(--ui-ink)">
              <option value="light">Light Mode</option>
              <option value="dark">Dark Mode</option>
            </select>
          </div>
          <div><div style="font-weight:700;margin-bottom:6px">Primary Color</div><div class="ui-swatch-grid">${buildSwatchGroup('primary')}</div></div>
          <div><div style="font-weight:700;margin-bottom:6px">Sidebar Color</div><div class="ui-swatch-grid">${buildSwatchGroup('sidebar')}</div></div>
          <div><div style="font-weight:700;margin-bottom:6px">Top Header Color</div><div class="ui-swatch-grid">${buildSwatchGroup('header')}</div></div>
          <div>
            <label for="keithUiLayoutSelect" style="display:block;font-weight:700;margin-bottom:6px">Menu Layout</label>
            <select id="keithUiLayoutSelect" data-pref-select="layout" style="width:100%;padding:8px;border-radius:8px;border:1px solid var(--ui-border);background:var(--ui-surface);color:var(--ui-ink)">
              <option value="vertical">Side Menu (Vertical)</option>
              <option value="horizontal">Top Menu (Horizontal)</option>
            </select>
          </div>
          <div>
            <label for="keithUiSidebarModeSelect" style="display:block;font-weight:700;margin-bottom:6px">Sidebar Size</label>
            <select id="keithUiSidebarModeSelect" data-pref-select="sidebarMode" style="width:100%;padding:8px;border-radius:8px;border:1px solid var(--ui-border);background:var(--ui-surface);color:var(--ui-ink)">
              <option value="full">Full Width</option>
              <option value="mini">Collapsed Icons (Mini)</option>
              <option value="compact">Compact</option>
              <option value="floating">Floating Island</option>
            </select>
          </div>
          <div>
            <label for="keithUiFontSelect" style="display:block;font-weight:700;margin-bottom:6px">Font Style</label>
            <select id="keithUiFontSelect" data-pref-select="font" style="width:100%;padding:8px;border-radius:8px;border:1px solid var(--ui-border);background:var(--ui-surface);color:var(--ui-ink)">
              <option value="Plus Jakarta Sans">Plus Jakarta Sans</option>
              <option value="Inter">Inter</option>
              <option value="DM Sans">DM Sans</option>
              <option value="Cairo">Cairo</option>
            </select>
          </div>
        </div>
        <div style="padding:14px 16px;border-top:1px solid var(--ui-border)">
          <button type="button" id="keithUiResetBtn" class="ui-btn ui-btn-outline" style="width:100%">Reset Default Settings</button>
        </div>
      </aside>
    `;
    document.body.appendChild(container);

    const drawer = document.getElementById('keithUiDrawer');
    document.getElementById('keithUiOpenBtn').addEventListener('click', () => drawer.setAttribute('data-open', 'true'));
    document.getElementById('keithUiCloseBtn').addEventListener('click', () => drawer.setAttribute('data-open', 'false'));

    const syncControls = () => {
      container.querySelectorAll('[data-pref-select]').forEach((selectEl) => {
        selectEl.value = currentPrefs[selectEl.getAttribute('data-pref-select')];
      });
      container.querySelectorAll('[data-pref-field]').forEach((btn) => {
        const key = btn.getAttribute('data-pref-field');
        btn.setAttribute('aria-pressed', String(currentPrefs[key] === btn.getAttribute('data-pref-val')));
      });
    };
    syncControls();

    container.addEventListener('click', (event) => {
      const swatchBtn = event.target.closest('[data-pref-field]');
      if (!swatchBtn) return;
      currentPrefs[swatchBtn.getAttribute('data-pref-field')] = swatchBtn.getAttribute('data-pref-val');
      savePreferences(currentPrefs);
      applyPreferences(currentPrefs);
      syncControls();
    });

    container.addEventListener('change', (event) => {
      const selectEl = event.target.closest('[data-pref-select]');
      if (!selectEl) return;
      currentPrefs[selectEl.getAttribute('data-pref-select')] = selectEl.value;
      savePreferences(currentPrefs);
      applyPreferences(currentPrefs);
    });

    document.getElementById('keithUiResetBtn').addEventListener('click', () => {
      currentPrefs = Object.assign({}, DEFAULT_PREFERENCES);
      savePreferences(currentPrefs);
      applyPreferences(currentPrefs);
      syncControls();
    });
  }

  applyPreferences(readPreferences());
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', mountSettingsDrawer);
  } else {
    mountSettingsDrawer();
  }

  window.KeithUI = { readPreferences, savePreferences, applyPreferences };
})();
