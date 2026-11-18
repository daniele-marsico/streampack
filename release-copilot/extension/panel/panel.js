// Side panel: the release package, prepared once and reused on every distributor.
const API = 'https://streampack.pages.dev/api/release'; // also served at uploadmysong.controllinghub.com
const IT = /^it\b/i.test(navigator.language || '');
const L = IT ? {
  tagline: 'Prepara una volta, compila ovunque', release: 'Release', artist: 'Nome artista', type: 'Tipo', releaseDate: 'Data di uscita',
  releaseTitle: 'Titolo album / EP', primaryGenre: 'Genere principale', secondaryGenre: 'Genere secondario', language: 'Lingua',
  label: 'Etichetta', copyrightYear: 'Anno ©', copyrightOwner: 'Titolare ©', aiUsage: 'Uso di AI nella musica',
  aiNone: 'Nessuno', aiPartial: 'In parte (es. strumenti, voce)', aiFull: 'Generata con AI', description: 'Descrizione / bio della release',
  tracks: 'Tracce', addTrack: '+ Aggiungi traccia', remove: 'Rimuovi', title: 'Titolo brano', version: 'Versione (es. Remix)',
  featuring: 'Featuring', songwriters: 'Autori, nome e cognome reali (separati da virgola)', producers: 'Produttori',
  previewStart: 'Inizio anteprima', explicit: 'Testo esplicito', instrumental: 'Strumentale', lyrics: 'Testo',
  about: 'Di cosa parla, che sound ha (per l\'AI)', aiGo: 'Suggerisci con AI', checks: 'Controlli prima dell\'invio',
  howto: 'Apri la pagina di caricamento di DistroKid o RouteNote e premi il pulsante Release Copilot in basso a destra.',
  export: 'Esporta .json', import: 'Importa .json', clear: 'Svuota tutto', confirmClear: 'Svuotare il pacchetto release?',
  aiBusy: 'Sto pensando…', aiErr: 'AI non disponibile ora, riprova più tardi.', aiLimit: 'Limite giornaliero raggiunto.', use: 'Usa',
  allGood: 'Tutto a posto', need: (f) => `Manca: ${f}`,
  cCaps: (t) => `"${t}": niente titoli tutti in maiuscolo, gli store li rifiutano`,
  cFeatTitle: (t) => `"${t}": togli "feat." dal titolo e mettilo nel campo Featuring`,
  cJunk: (t) => `"${t}": niente "Official", "Audio", "Video" o emoji nel titolo`,
  cWriter: (w) => `Autore "${w}": serve nome e cognome reali (Spotify li richiede)`,
  cArtistFeat: 'Nel nome artista non mettere "feat." o "&": usa i campi dedicati',
  cDate: 'Uscita tra meno di 7 giorni: carica almeno 2-4 settimane prima per il pitch su Spotify',
  cPast: 'La data di uscita è nel passato',
  cSingle: 'Single con più tracce: scegli EP o Album',
} : {
  tagline: 'Prepare once, fill everywhere', release: 'Release', artist: 'Artist name', type: 'Type', releaseDate: 'Release date',
  releaseTitle: 'Album / EP title', primaryGenre: 'Primary genre', secondaryGenre: 'Secondary genre', language: 'Language',
  label: 'Label', copyrightYear: '© year', copyrightOwner: '© owner', aiUsage: 'AI use in the music',
  aiNone: 'None', aiPartial: 'Partly (e.g. instruments, vocals)', aiFull: 'AI-generated', description: 'Release description / bio',
  tracks: 'Tracks', addTrack: '+ Add track', remove: 'Remove', title: 'Song title', version: 'Version (e.g. Remix)',
  featuring: 'Featuring', songwriters: 'Songwriters, real first and last name (comma separated)', producers: 'Producers',
  previewStart: 'Preview start', explicit: 'Explicit lyrics', instrumental: 'Instrumental', lyrics: 'Lyrics',
  about: 'What it is about and how it sounds (for the AI)', aiGo: 'Suggest with AI', checks: 'Checks before upload',
  howto: 'Open the DistroKid or RouteNote upload page and press the Release Copilot button at the bottom right.',
  export: 'Export .json', import: 'Import .json', clear: 'Clear all', confirmClear: 'Clear the release package?',
  aiBusy: 'Thinking…', aiErr: 'AI unavailable right now, try later.', aiLimit: 'Daily limit reached.', use: 'Use',
  allGood: 'All good', need: (f) => `Missing: ${f}`,
  cCaps: (t) => `"${t}": no all-caps titles, stores reject them`,
  cFeatTitle: (t) => `"${t}": remove "feat." from the title and use the Featuring field`,
  cJunk: (t) => `"${t}": no "Official", "Audio", "Video" or emoji in titles`,
  cWriter: (w) => `Songwriter "${w}": needs real first and last name (Spotify requires it)`,
  cArtistFeat: 'Do not put "feat." or "&" in the artist name: use the dedicated fields',
  cDate: 'Release in under 7 days: upload 2-4 weeks ahead to pitch on Spotify',
  cPast: 'The release date is in the past',
  cSingle: 'Single with more than one track: choose EP or Album',
};
document.querySelectorAll('[data-t]').forEach((n) => { if (L[n.dataset.t]) n.textContent = L[n.dataset.t]; });

const REL = ['artist', 'type', 'releaseDate', 'releaseTitle', 'primaryGenre', 'secondaryGenre', 'language', 'label', 'copyrightYear', 'copyrightOwner', 'aiUsage', 'description', 'about'];
const blankTrack = () => ({ title: '', version: '', featuring: '', songwriters: [], producers: '', isrc: '', previewStart: '', explicit: false, instrumental: false, lyrics: '' });
let pkg;

const $ = (s) => document.querySelector(s);
const save = () => { chrome.storage.local.set({ pkg }); renderChecks(); };

function parseWriters(s) {
  return s.split(',').map((x) => x.trim()).filter(Boolean).map((full) => {
    const p = full.split(/\s+/);
    return { first: p.slice(0, -1).join(' ') || p[0], last: p.length > 1 ? p[p.length - 1] : '' };
  });
}
const writersText = (w) => (w || []).map((x) => `${x.first} ${x.last}`.trim()).join(', ');

function renderTracks() {
  const box = $('#tracks');
  box.innerHTML = '';
  pkg.tracks.forEach((t, i) => {
    const n = $('#trackTpl').content.cloneNode(true);
    n.querySelectorAll('[data-t]').forEach((x) => { if (L[x.dataset.t]) x.textContent = L[x.dataset.t]; });
    n.querySelector('.num').textContent = `${IT ? 'Traccia' : 'Track'} ${i + 1}`;
    n.querySelectorAll('[data-f]').forEach((inp) => {
      const f = inp.dataset.f;
      if (inp.type === 'checkbox') inp.checked = !!t[f];
      else inp.value = f === 'songwriters' ? writersText(t[f]) : (t[f] || '');
      inp.addEventListener(inp.type === 'checkbox' ? 'change' : 'input', () => {
        t[f] = inp.type === 'checkbox' ? inp.checked : f === 'songwriters' ? parseWriters(inp.value) : inp.value;
        save();
      });
    });
    const del = n.querySelector('.del');
    if (pkg.tracks.length < 2) del.remove();
    else del.onclick = () => { pkg.tracks.splice(i, 1); renderTracks(); save(); };
    box.appendChild(n);
  });
  $('.multi').style.display = pkg.type === 'single' ? 'none' : '';
}

function renderRelease() {
  REL.forEach((k) => {
    const el = document.getElementById(k);
    el.value = pkg[k] || '';
    el.oninput = el.onchange = () => {
      pkg[k] = el.value;
      if (k === 'type') renderTracks();
      save();
    };
  });
}

function checks() {
  const out = [];
  const need = [];
  if (!pkg.artist) need.push(L.artist);
  if (!pkg.releaseDate) need.push(L.releaseDate);
  if (!pkg.primaryGenre) need.push(L.primaryGenre);
  if (!pkg.language) need.push(L.language);
  if (pkg.type !== 'single' && !pkg.releaseTitle) need.push(L.releaseTitle);
  pkg.tracks.forEach((t, i) => {
    if (!t.title) need.push(`${L.title} ${i + 1}`);
    if (!t.songwriters.length) need.push(`${L.songwriters.split(',')[0]} ${i + 1}`);
  });
  if (need.length) out.push(['bad', L.need(need.join(', '))]);
  if (/\b(feat|ft)\.?\s|&/i.test(pkg.artist || '')) out.push(['warn', L.cArtistFeat]);
  if (pkg.type === 'single' && pkg.tracks.length > 1) out.push(['warn', L.cSingle]);
  const titles = [pkg.type !== 'single' && pkg.releaseTitle, ...pkg.tracks.map((t) => t.title)].filter(Boolean);
  titles.forEach((t) => {
    if (t.length > 3 && t === t.toUpperCase() && /[A-Z]/.test(t)) out.push(['warn', L.cCaps(t)]);
    if (/\b(feat|ft)\.?\s/i.test(t)) out.push(['warn', L.cFeatTitle(t)]);
    if (/\b(official|audio|video|lyric video)\b/i.test(t) || /\p{Extended_Pictographic}/u.test(t)) out.push(['warn', L.cJunk(t)]);
  });
  pkg.tracks.forEach((t) => t.songwriters.forEach((w) => { if (!w.last) out.push(['warn', L.cWriter(w.first)]); }));
  if (pkg.releaseDate) {
    const days = (new Date(pkg.releaseDate) - new Date(new Date().toDateString())) / 864e5;
    if (days < 0) out.push(['bad', L.cPast]);
    else if (days < 7) out.push(['warn', L.cDate]);
  }
  if (!out.length) out.push(['ok', L.allGood]);
  return out;
}
function renderChecks() {
  $('#checks').innerHTML = checks().map(([c, m]) => `<li class="${c}">${c === 'ok' ? '✓' : c === 'bad' ? '✗' : '!'} ${esc(m)}</li>`).join('');
}
const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

// AI: suggestions only. Nothing is applied until the artist taps "Use".
$('#ai').onclick = async () => {
  const b = $('#ai'), out = $('#aiOut');
  b.disabled = true; b.textContent = L.aiBusy; out.innerHTML = '';
  try {
    const r = await fetch(API, {
      method: 'POST', headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ artist: pkg.artist, title: pkg.releaseTitle || pkg.tracks[0].title, type: pkg.type, about: pkg.about, lyrics: pkg.tracks[0].lyrics, lang: IT ? 'Italian' : 'English' }),
    });
    const d = await r.json();
    if (!r.ok) throw new Error(d.error === 'limit' ? L.aiLimit : L.aiErr);
    const rows = [
      ['primaryGenre', L.primaryGenre, d.primaryGenre], ['secondaryGenre', L.secondaryGenre, d.secondaryGenre],
      ['language', L.language, d.language], ['description', L.description, d.description],
    ].filter((x) => x[2]);
    out.innerHTML = rows.map(([k, lab, v]) => `<div class="sugg"><div class="muted">${esc(lab)}</div><div>${esc(v)}</div><button data-k="${k}">${L.use}</button></div>`).join('')
      + (d.pitch ? `<div class="sugg"><div class="muted">Spotify pitch</div><div>${esc(d.pitch)}</div></div>` : '')
      + (d.mood ? `<div class="sugg"><div class="muted">Mood</div><div>${esc(d.mood)}</div></div>` : '');
    out.querySelectorAll('button[data-k]').forEach((btn) => (btn.onclick = () => {
      const k = btn.dataset.k; pkg[k] = rows.find((x) => x[0] === k)[2];
      renderRelease(); save(); btn.disabled = true;
    }));
  } catch (e) {
    out.innerHTML = `<p class="muted">${esc(e.message || L.aiErr)}</p>`;
  }
  b.disabled = false; b.textContent = L.aiGo;
};

$('#addTrack').onclick = () => { pkg.tracks.push(blankTrack()); if (pkg.type === 'single' && pkg.tracks.length > 1) pkg.type = 'ep'; renderRelease(); renderTracks(); save(); };
$('#export').onclick = () => {
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob([JSON.stringify(pkg, null, 2)], { type: 'application/json' }));
  a.download = `${(pkg.artist || 'release')}-${(pkg.releaseTitle || pkg.tracks[0].title || 'release')}.json`.replace(/[^\w.-]+/g, '_');
  a.click();
};
$('#import').onchange = async (e) => {
  const f = e.target.files[0]; if (!f) return;
  try { pkg = normalize(JSON.parse(await f.text())); renderRelease(); renderTracks(); save(); } catch (err) { alert('JSON?'); }
};
$('#clear').onclick = () => { if (confirm(L.confirmClear)) { pkg = normalize({}); renderRelease(); renderTracks(); save(); } };

function normalize(p) {
  p = p || {};
  p.type = p.type || 'single';
  p.aiUsage = p.aiUsage || 'none';
  p.copyrightYear = p.copyrightYear || String(new Date().getFullYear());
  p.tracks = (p.tracks && p.tracks.length ? p.tracks : [blankTrack()]).map((t) => ({ ...blankTrack(), ...t, songwriters: Array.isArray(t.songwriters) ? t.songwriters : parseWriters(String(t.songwriters || '')) }));
  return p;
}

chrome.storage.local.get('pkg', (o) => {
  pkg = normalize(o.pkg);
  renderRelease(); renderTracks(); renderChecks();
});

// ---------- Tab 2: guided copy into the distributor's form ----------
Object.assign(L, IT ? {
  tabPrep: '1 · Prepara', tabUp: '2 · Carica', dist: 'Distributore', copyHow: 'Premi il pulsante verde, incolla nel campo del sito (Ctrl+V) e ripeti. Puoi anche toccare un campo qualsiasi per copiarlo.',
  restart: 'Ricomincia da capo', open: (n) => `Apri ${n} ↗`, next: (l) => `📋 Copia: ${l}`, allDone: '✓ Tutto copiato. Controlla e invia sul sito.',
  fileHint: 'carica il file convertito', pick: (v) => `seleziona: ${v}`, empty: '(vuoto, salta)', copied: 'Copiato', release: 'Release',
} : {
  tabPrep: '1 · Prepare', tabUp: '2 · Upload', dist: 'Distributor', copyHow: 'Press the green button, paste into the site field (Ctrl+V) and repeat. You can also tap any field to copy it.',
  restart: 'Start over', open: (n) => `Open ${n} ↗`, next: (l) => `📋 Copy: ${l}`, allDone: '✓ All copied. Check and submit on the site.',
  fileHint: 'upload the converted file', pick: (v) => `select: ${v}`, empty: '(empty, skip)', copied: 'Copied', release: 'Release',
});
L.howto = IT ? 'Quando è tutto pronto passa a "2 · Carica".' : 'When everything is ready, go to "2 · Upload".';
L.tagline = IT ? 'Il tuo brano pronto per ogni distributore' : 'Your song, ready for every distributor';
['tabPrep', 'tabUp', 'dist', 'copyHow', 'restart', 'howto', 'tagline'].forEach((k) => document.querySelectorAll(`[data-t="${k}"]`).forEach((n) => (n.textContent = L[k])));

const sel = $('#dist');
Object.entries(DISTRIBUTORS).forEach(([k, d]) => sel.add(new Option(d.name, k)));
let done = new Set();
function rows() {
  const d = DISTRIBUTORS[sel.value];
  const out = [{ head: L.release }];
  d.release.forEach(([k, label, fn, kind]) => out.push({ id: 'r.' + k, label, kind, value: kind === 'file' ? '' : String(fn(pkg, null, IT) || '') }));
  pkg.tracks.forEach((t, i) => {
    out.push({ head: `${IT ? 'Traccia' : 'Track'} ${i + 1}${t.title ? ' · ' + t.title : ''}` });
    d.track.forEach(([k, label, fn, kind]) => out.push({ id: `t${i}.${k}`, label, kind, value: kind === 'file' ? '' : String(fn(pkg, t, IT) || '') }));
  });
  return out;
}
const copyable = (r) => r.id && !r.kind && r.value;
function renderUp() {
  const d = DISTRIBUTORS[sel.value];
  $('#openDist').href = d.url;
  $('#openDist').textContent = L.open(d.name);
  const list = rows();
  const nxt = list.find((r) => copyable(r) && !done.has(r.id));
  $('#next').textContent = nxt ? L.next(nxt.label) : L.allDone;
  $('#next').disabled = !nxt;
  $('#next').onclick = () => nxt && copy(nxt);
  $('#fields').innerHTML = list.map((r) => r.head ? `<div class="fhead">${esc(r.head)}</div>` : `<div class="field ${r.kind === 'file' ? 'file' : ''} ${!r.value && r.kind !== 'file' ? 'empty' : ''} ${done.has(r.id) ? 'done' : ''} ${nxt && nxt.id === r.id ? 'cur' : ''}" data-id="${r.id}"><span class="k">${esc(r.label)}</span><span class="v">${esc(r.kind === 'file' ? L.fileHint : r.kind === 'choice' ? L.pick(r.value) : r.value || L.empty)}</span></div>`).join('');
  $('#fields').querySelectorAll('.field').forEach((el) => {
    const r = list.find((x) => x.id === el.dataset.id);
    if (copyable(r)) el.onclick = () => copy(r);
  });
}
async function copy(r) {
  try { await navigator.clipboard.writeText(r.value); } catch (e) {
    const ta = document.createElement('textarea'); ta.value = r.value; document.body.appendChild(ta); ta.select(); document.execCommand('copy'); ta.remove();
  }
  done.add(r.id);
  renderUp();
  const b = $('#next'); const old = b.textContent; b.textContent = `✓ ${L.copied}: ${r.label}`;
  setTimeout(() => { if (b.textContent.startsWith('✓ ' + L.copied)) renderUp(); }, 900);
}
sel.onchange = () => { done = new Set(); chrome.storage.local.set({ dist: sel.value }); renderUp(); };
$('#restart').onclick = () => { done = new Set(); renderUp(); };
const show = (up) => { $('#up').hidden = !up; $('#prep').hidden = up; $('#tabUp').classList.toggle('on', up); $('#tabPrep').classList.toggle('on', !up); if (up) renderUp(); window.scrollTo(0, 0); };
$('#tabUp').onclick = () => show(true);
$('#tabPrep').onclick = () => show(false);
chrome.storage.local.get('dist', (o) => { if (o.dist && DISTRIBUTORS[o.dist]) sel.value = o.dist; });
