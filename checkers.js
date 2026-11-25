/* Free checker pages (LUFS checker, ISRC/UPC checker). Texts come from <script id="ui" type="application/json">,
   the measuring is done by check.js. Nothing is uploaded. */
(function () {
  'use strict';
  const UI = JSON.parse(document.getElementById('ui').textContent);
  const L = document.documentElement.lang || 'en';
  const $ = s => document.querySelector(s);
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]);
  const nf = (x, d = 1) => x.toLocaleString(L, { minimumFractionDigits: d, maximumFractionDigits: d });
  const sgn = x => (x > 0.05 ? '+' : '') + nf(x);
  const SP = window.SPCheck;

  /* ---------------- LUFS checker ---------------- */
  // Spotify publishes -14 LUFS; the others are the values most often measured (see the note under the table)
  const PLAT = [['Spotify', -14], ['YouTube', -14], ['Apple Music', -16], ['Amazon Music', -14], ['TIDAL', -14], ['Deezer', -15]];
  function lufsTool() {
    const inp = $('#f'), out = $('#res');
    inp.onchange = async () => {
      const f = inp.files[0]; inp.value = ''; if (!f) return;
      out.innerHTML = `<div class="card"><p style="margin:0"><b>${esc(f.name)}</b></p><p class="msg">${esc(UI.measuring)}</p></div>`;
      await new Promise(z => setTimeout(z, 30));
      try { render(f, await SP.analyze(f)); }
      catch (e) { console.error(e); out.innerHTML = `<div class="card"><p style="margin:0"><b>${esc(f.name)}</b></p><p class="warn">⚠︎ ${esc(UI.err)}</p></div>`; }
    };
    function render(f, r) {
      const h = r.h, kind = SP.label(h.kind || r.ext);
      const spec = [kind + (h.bits ? (h.float ? ' 32-bit float' : ` ${h.bits}-bit`) : ''), h.sr ? `${nf(h.sr / 1000, h.sr % 1000 ? 1 : 0)} kHz` : '', r.ch === 1 ? 'mono' : r.ch > 2 ? r.ch + ' ch' : UI.stereo].filter(Boolean).join(' · ');
      const tpdb = SP.db(r.tp), d = Math.round(r.dur);
      const notes = [];
      const w = t => notes.push(`<li class="w">⚠︎ ${esc(t)}</li>`), ok = t => notes.push(`<li class="ok">✓ ${esc(t)}</li>`);
      if (r.silent) w(UI.silent);
      if (h.kind && r.ext && r.ext !== h.kind && !(r.ext === 'm4a' && (h.kind === 'aac' || h.kind === 'mov'))) w(UI.mis.replace('{e}', r.ext).replace('{k}', SP.label(h.kind)));
      if (SP.isLossy(h.kind || r.ext)) w(UI.lossy.replace('{k}', kind));
      if (r.ch === 1) w(UI.mono);
      if (r.clips >= 3) w(UI.clip.replace('{n}', r.clips));
      if (!r.silent && r.lead > 2) w(UI.lead.replace('{s}', nf(r.lead)));
      if (!r.silent && r.tail > 5) w(UI.tail.replace('{s}', nf(r.tail)));
      if (Math.max(Math.abs(r.dc[0]), Math.abs(r.dc[1])) > 1e-3) w(UI.dc);
      if (tpdb > -0.95) w(UI.tpw); else ok(UI.tpok);
      const rows = PLAT.map(([n, t]) => {
        const diff = r.I - t;
        const v = diff > 0.5 ? UI.down.replace('{d}', nf(diff)) : diff < -0.5 ? UI.below.replace('{d}', nf(-diff)) : UI.same;
        return `<tr><td><b>${n}</b></td><td>${nf(t, 0)} LUFS</td><td>${esc(v)}</td></tr>`;
      }).join('');
      out.innerHTML = `<div class="card res">
        <p style="margin:0"><b>${esc(f.name)}</b></p>
        <div class="big">${r.silent ? '–' : nf(r.I)} <small>LUFS</small></div>
        <table class="kv"><tbody>
          <tr><th>${esc(UI.TP)}</th><td>${sgn(tpdb)} dBTP</td></tr>
          <tr><th>${esc(UI.LRA)}</th><td>${r.LRA == null ? '–' : nf(r.LRA) + ' LU'}</td></tr>
          <tr><th>${esc(UI.file)}</th><td>${esc(spec)}</td></tr>
          <tr><th>${esc(UI.dur)}</th><td>${Math.floor(d / 60)}:${String(d % 60).padStart(2, '0')}</td></tr>
        </tbody></table>
        <ul class="issues">${notes.join('')}</ul>
        <h3>${esc(UI.plat)}</h3>
        <table><thead><tr>${UI.cols.map(c => `<th>${esc(c)}</th>`).join('')}</tr></thead><tbody>${rows}</tbody></table>
        <p class="msg">${esc(UI.note)}</p>
        <a class="btn" href="${esc(UI.fixUrl)}">${esc(UI.fix)}</a>
      </div>`;
    }
  }

  /* ---------------- ISRC / UPC-EAN checker ---------------- */
  function isrcTool() {
    const ii = $('#isrc'), uu = $('#upc'), oi = $('#res-isrc'), ou = $('#res-upc');
    let names = null; try { names = new Intl.DisplayNames([L], { type: 'region' }); } catch (e) { }
    const SPECIAL = { QM: UI.us, QZ: UI.us, QT: UI.us, ZZ: UI.intl };
    const country = c => {
      if (SPECIAL[c]) return [SPECIAL[c], true];
      let n = ''; try { n = names ? names.of(c) : ''; } catch (e) { }
      return n && n !== c ? [n, true] : [c, false];
    };
    const yearOf = yy => { const now = new Date().getFullYear() % 100; return (+yy <= now + 1 ? 2000 : 1900) + +yy; };
    const link = (href, t) => `<a class="btn ghost" target="_blank" rel="noopener" href="${esc(href)}">${esc(t)} ↗</a>`;
    function run() {
      const i = SP.isrc(ii.value);
      if (i.ok === null) oi.innerHTML = '';
      else if (i.ok) {
        const [cn, known] = country(i.v.slice(0, 2));
        oi.innerHTML = `<p class="ok">✓ ${esc(UI.isrcOk)} · <b>${esc(i.pretty)}</b></p>
          <table class="kv"><tbody>
          <tr><th>${esc(UI.country)}</th><td>${esc(i.v.slice(0, 2))}${known ? ' · ' + esc(cn) : ''}</td></tr>
          <tr><th>${esc(UI.reg)}</th><td>${esc(i.v.slice(2, 5))}</td></tr>
          <tr><th>${esc(UI.year)}</th><td>${yearOf(i.year)}</td></tr>
          <tr><th>${esc(UI.num)}</th><td>${esc(i.v.slice(7))}</td></tr></tbody></table>
          ${known ? '' : `<p class="warn">⚠︎ ${esc(UI.ctryWarn)}</p>`}
          <p class="msg">${esc(UI.find)}</p>${link('https://open.spotify.com/search/isrc%3A' + i.v, 'Spotify')} ${link('https://musicbrainz.org/isrc/' + i.v, 'MusicBrainz')}`;
      } else if (i.err === 'len' && i.v.length < 12) oi.innerHTML = `<p class="msg">${esc(UI.isrcLen)}</p>`;
      else oi.innerHTML = `<p class="warn">⚠︎ ${esc(i.err === 'len' ? UI.isrcLen : UI.isrcFmt)}</p>`;
      const u = SP.barcode(uu.value);
      if (u.ok === null) ou.innerHTML = '';
      else if (u.ok) ou.innerHTML = `<p class="ok">✓ ${esc(UI.upcOk.replace('{t}', u.type))} · <b>${esc(u.v)}</b></p>
          <p class="msg">${esc(UI.findRel || UI.find)}</p>${link('https://open.spotify.com/search/upc%3A' + u.v, 'Spotify')} ${link('https://musicbrainz.org/search?type=release&method=advanced&query=barcode%3A' + u.v, 'MusicBrainz')}`;
      else if (u.err === 'len' && u.v.length < 12) ou.innerHTML = `<p class="msg">${esc(UI.upcLen)}</p>`;
      else ou.innerHTML = `<p class="warn">⚠︎ ${esc(u.err === 'check' ? UI.upcChk.replace('{d}', u.want) : u.err === 'len' ? UI.upcLen : UI.upcFmt)}</p>`;
    }
    ii.oninput = run; uu.oninput = run;
    const q = new URLSearchParams(location.search);
    if (q.get('isrc')) ii.value = q.get('isrc');
    if (q.get('upc')) uu.value = q.get('upc');
    run();
  }

  if ($('#f')) lufsTool();
  if ($('#isrc')) isrcTool();
})();
