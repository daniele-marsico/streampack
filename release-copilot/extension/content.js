// On-page copilot: a small floating panel on DistroKid / RouteNote upload pages.
(function () {
  if (window.__rcLoaded) return;
  window.__rcLoaded = true;
  const T = window.RC_T;
  const adapter = Object.values(window.RC_ADAPTERS || {}).find((a) => a.host.test(location.hostname));
  if (!adapter) return;
  // Only show where there is an upload form
  const hasForm = () => document.querySelectorAll('input,select,textarea').length >= 4;

  const store = {
    get: (k) => new Promise((r) => chrome.storage.local.get(k, (o) => r(o[k]))),
    set: (k, v) => new Promise((r) => chrome.storage.local.set({ [k]: v }, r)),
  };
  const ovKey = 'overrides:' + location.hostname.replace(/^www\./, '');
  const files = {}; // picked on this page: { cover: File, 'audio:0': File }

  const host = document.createElement('div');
  host.id = 'rc-root';
  const root = host.attachShadow({ mode: 'open' });
  root.innerHTML = `
  <style>
    :host { all: initial; }
    .fab { position: fixed; right: 18px; bottom: 18px; z-index: 2147483646; background: #111827; color: #fff; border: 0; border-radius: 999px;
      padding: 12px 16px; font: 600 14px system-ui, sans-serif; box-shadow: 0 6px 20px rgba(0,0,0,.25); cursor: pointer; display: flex; gap: 8px; align-items: center; }
    .fab img { width: 20px; height: 20px; border-radius: 5px; }
    .box { position: fixed; right: 18px; bottom: 72px; z-index: 2147483646; width: 340px; max-height: 70vh; overflow: auto; background: #fff; color: #111827;
      border-radius: 14px; box-shadow: 0 12px 40px rgba(0,0,0,.25); font: 13px/1.4 system-ui, sans-serif; padding: 14px; display: none; }
    .box.open { display: block; }
    h3 { margin: 0 0 4px; font-size: 15px; } .muted { color: #6b7280; font-size: 12px; }
    .row { display: flex; align-items: center; gap: 8px; margin: 6px 0; } .row label { flex: 1; }
    input[type=file] { font-size: 11px; max-width: 170px; }
    button.main { width: 100%; margin: 10px 0 6px; padding: 10px; border: 0; border-radius: 10px; background: #16a34a; color: #fff; font: 600 14px system-ui; cursor: pointer; }
    button.link { background: none; border: 0; color: #2563eb; cursor: pointer; padding: 0; font: 12px system-ui; }
    ul { list-style: none; padding: 0; margin: 8px 0; } li { display: flex; justify-content: space-between; gap: 6px; padding: 4px 0; border-bottom: 1px solid #f3f4f6; }
    .ok { color: #16a34a; } .bad { color: #dc2626; } .warn { color: #d97706; }
    .note { background: #fef3c7; border-radius: 8px; padding: 8px; margin-top: 8px; font-size: 12px; }
  </style>
  <button class="fab" id="fab"><img src="${chrome.runtime.getURL('icons/icon-32.png')}" alt="">Release Copilot</button>
  <div class="box" id="box"></div>`;
  const $ = (s) => root.querySelector(s);

  async function render(report) {
    const pkg = await store.get('pkg');
    const box = $('#box');
    if (!pkg || !pkg.tracks || !pkg.tracks.length || !pkg.artist) {
      box.innerHTML = `<h3>${adapter.name}</h3><p>${T.noPkg}</p><button class="main" id="open">${T.openPanel}</button>`;
      $('#open').onclick = () => chrome.runtime.sendMessage({ type: 'openPanel' });
      return;
    }
    const title = pkg.releaseTitle || pkg.tracks[0].title;
    let html = `<h3>${esc(pkg.artist)} – ${esc(title)}</h3><div class="muted">${adapter.name} · ${pkg.tracks.length} ${T.tracksWord}</div>
      <div class="muted" style="margin-top:8px">${T.files}</div>
      <div class="row"><label>${T.cover}${files.cover ? ' ✓' : ''}</label><input type="file" accept="image/*" data-k="cover"></div>`;
    pkg.tracks.forEach((t, i) => {
      html += `<div class="row"><label>${i + 1}. ${esc(t.title || T.track)}${files['audio:' + i] ? ' ✓' : ''}</label><input type="file" accept="audio/*,.wav,.flac" data-k="audio:${i}"></div>`;
    });
    html += `<button class="main" id="fill">${T.fill}</button>`;
    if (report) {
      const shown = report.filter((r) => r.status !== 'skip');
      const done = shown.filter((r) => r.status === 'ok').length;
      html += `<div><b>${T.summary(done, shown.length)}</b></div><ul>`;
      shown.forEach((r) => {
        const cls = r.status === 'ok' ? 'ok' : r.status === 'empty' ? 'warn' : 'bad';
        const name = (r.track !== null ? `${r.track + 1}. ` : '') + r.label;
        const act = ['missing', 'option', 'error'].includes(r.status) ? ` <button class="link" data-pick="${r.id}" data-name="${esc(name)}">${T.point}</button>` : '';
        html += `<li><span>${esc(name)}</span><span class="${cls}">${T[r.status] || r.status}${act}</span></li>`;
      });
      html += `</ul><div class="note">${T.review}</div><p><button class="link" id="reset">${T.reset}</button></p>`;
    }
    box.innerHTML = html;
    box.querySelectorAll('input[type=file]').forEach((inp) => {
      inp.onchange = () => { if (inp.files[0]) { files[inp.dataset.k] = inp.files[0]; render(report); } };
    });
    $('#fill').onclick = doFill;
    box.querySelectorAll('[data-pick]').forEach((b) => (b.onclick = () => pick(b.dataset.pick, b.dataset.name)));
    const rs = $('#reset');
    if (rs) rs.onclick = async () => { await store.set(ovKey, {}); render(report); };
  }
  const esc = (s) => String(s || '').replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

  let last = null;
  async function doFill() {
    const pkg = await store.get('pkg');
    const overrides = (await store.get(ovKey)) || {};
    last = window.RC_FILLER.fill(adapter, pkg, files, overrides);
    render(last);
  }

  // "Point it out": the next click on a form control binds it to this field
  function pick(id, name) {
    $('#box').classList.remove('open');
    const tip = document.createElement('div');
    tip.textContent = T.pickHint + name + '  (Esc)';
    Object.assign(tip.style, { position: 'fixed', top: '12px', left: '50%', transform: 'translateX(-50%)', zIndex: 2147483647, background: '#111827', color: '#fff', padding: '10px 14px', borderRadius: '10px', font: '600 14px system-ui' });
    document.body.appendChild(tip);
    document.documentElement.classList.add('rc-picking');
    let hovered = null;
    const target = (e) => {
      const el = e.target.closest('input,select,textarea,label');
      if (!el) return null;
      if (el.tagName === 'LABEL') return el.control || el.querySelector('input,select,textarea');
      return el;
    };
    const over = (e) => { if (hovered) hovered.classList.remove('rc-hover'); hovered = target(e); if (hovered) hovered.classList.add('rc-hover'); };
    const done = () => {
      document.removeEventListener('mouseover', over, true);
      document.removeEventListener('click', click, true);
      document.removeEventListener('keydown', key, true);
      document.documentElement.classList.remove('rc-picking');
      if (hovered) hovered.classList.remove('rc-hover');
      tip.remove();
      $('#box').classList.add('open');
    };
    const click = async (e) => {
      const el = target(e);
      if (!el) return;
      e.preventDefault(); e.stopPropagation();
      const ov = (await store.get(ovKey)) || {};
      ov[id] = window.RC_FILLER.cssPath(el);
      await store.set(ovKey, ov);
      done();
      doFill();
    };
    const key = (e) => { if (e.key === 'Escape') done(); };
    document.addEventListener('mouseover', over, true);
    document.addEventListener('click', click, true);
    document.addEventListener('keydown', key, true);
  }

  function mount() {
    if (document.getElementById('rc-root') || !hasForm()) return;
    document.body.appendChild(host);
    $('#fab').onclick = () => { $('#box').classList.toggle('open'); render(last); };
  }
  mount();
  // Upload pages are often single-page apps: retry when the page changes
  new MutationObserver(() => mount()).observe(document.documentElement, { childList: true, subtree: true });
  chrome.storage.onChanged.addListener((c) => { if (c.pkg && $('#box').classList.contains('open')) render(last); });
})();
