// Generic form-filling engine. No AI: deterministic, fast, free.
// It never presses submit: the artist always reviews and sends the form.
(function () {
  const norm = (s) => String(s || '').replace(/\s+/g, ' ').replace(/[*:]+/g, '').trim();
  const visible = (el) => {
    if (el.type === 'file') return true; // upload inputs are often hidden behind a button
    const r = el.getBoundingClientRect();
    const st = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && st.visibility !== 'hidden' && st.display !== 'none';
  };

  // Everything a human would read as this control's label
  function labelOf(el) {
    const parts = [];
    if (el.id) document.querySelectorAll(`label[for="${CSS.escape(el.id)}"]`).forEach((l) => parts.push(l.textContent));
    const wrap = el.closest('label');
    if (wrap) parts.push(wrap.textContent);
    if (el.getAttribute('aria-label')) parts.push(el.getAttribute('aria-label'));
    const lb = el.getAttribute('aria-labelledby');
    if (lb) lb.split(/\s+/).forEach((id) => { const n = document.getElementById(id); if (n) parts.push(n.textContent); });
    if (el.placeholder) parts.push(el.placeholder);
    if (parts.length) return norm(parts.join(' '));
    // Fallback: nearest text before the control, within a few ancestors
    let node = el;
    for (let up = 0; up < 3 && node; up++) {
      let sib = node.previousElementSibling;
      while (sib) {
        const t = norm(sib.textContent);
        if (t && t.length < 120) return t;
        sib = sib.previousElementSibling;
      }
      node = node.parentElement;
    }
    return norm(el.name || el.id);
  }
  // For radio/checkbox groups: the question, not the option
  function groupLabelOf(el) {
    const fs = el.closest('fieldset');
    if (fs) { const lg = fs.querySelector('legend'); if (lg) return norm(lg.textContent); }
    const grp = el.closest('[role="radiogroup"],[role="group"]');
    if (grp) {
      const l = grp.getAttribute('aria-label') || (grp.getAttribute('aria-labelledby') && (document.getElementById(grp.getAttribute('aria-labelledby')) || {}).textContent);
      if (l) return norm(l);
    }
    // Text before the first radio of the same name
    const first = el.name ? document.querySelector(`input[name="${CSS.escape(el.name)}"]`) : el;
    let node = first.closest('label') || first;
    for (let up = 0; up < 4 && node; up++) {
      let sib = node.previousElementSibling;
      while (sib) {
        if (!sib.querySelector || !sib.querySelector('input')) {
          const t = norm(sib.textContent);
          if (t && t.length < 160) return t;
        }
        sib = sib.previousElementSibling;
      }
      node = node.parentElement;
    }
    return norm(el.name);
  }

  function controlsFor(kind) {
    if (kind === 'file') return [...document.querySelectorAll('input[type=file]')];
    if (kind === 'select') return [...document.querySelectorAll('select')].filter(visible);
    if (kind === 'choice') return [...document.querySelectorAll('input[type=radio],input[type=checkbox],select')].filter(visible);
    return [...document.querySelectorAll('input:not([type]),input[type=text],input[type=date],input[type=email],input[type=number],input[type=search],textarea')].filter(visible);
  }

  function findAll(field, used) {
    const pool = controlsFor(field.kind).filter((el) => !used.has(el) && !el.disabled);
    const out = [];
    const seenGroups = new Set();
    for (const el of pool) {
      const isChoice = el.type === 'radio' || el.type === 'checkbox';
      if (field.kind === 'choice' && isChoice) {
        const g = el.name || el.id;
        if (seenGroups.has(g)) continue;
        if (field.match.some((re) => re.test(groupLabelOf(el)) || re.test(labelOf(el)))) { seenGroups.add(g); out.push(el); }
        continue;
      }
      const lab = labelOf(el);
      let ok = field.match.some((re) => re.test(lab));
      if (!ok && field.kind === 'file' && field.accept) ok = field.accept.test(el.accept || '');
      if (ok) out.push(el);
    }
    return out;
  }

  function fire(el) {
    el.dispatchEvent(new Event('input', { bubbles: true }));
    el.dispatchEvent(new Event('change', { bubbles: true }));
    el.dispatchEvent(new Event('blur', { bubbles: true }));
  }
  function setText(el, v) {
    const proto = el.tagName === 'TEXTAREA' ? HTMLTextAreaElement.prototype : HTMLInputElement.prototype;
    const setter = Object.getOwnPropertyDescriptor(proto, 'value').set; // works with React-controlled inputs
    el.focus();
    setter.call(el, v);
    fire(el);
  }
  function toDate(el, iso) {
    if (el.type === 'date' || !/^\d{4}-\d{2}-\d{2}$/.test(iso)) return iso;
    const [y, m, d] = iso.split('-');
    const hint = (el.placeholder || '').toLowerCase();
    if (/^dd/.test(hint)) return `${d}/${m}/${y}`;
    if (/^mm/.test(hint)) return `${m}/${d}/${y}`;
    return iso;
  }
  const simplify = (s) => norm(s).toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9]+/g, ' ').trim();
  function pickOption(sel, want) {
    const w = simplify(want);
    const opts = [...sel.options].filter((o) => !o.disabled && o.value !== '');
    return opts.find((o) => simplify(o.textContent) === w) || opts.find((o) => simplify(o.value) === w)
      || opts.find((o) => simplify(o.textContent).startsWith(w)) || opts.find((o) => simplify(o.textContent).includes(w));
  }
  const YES = /^(yes|si|sì|explicit|true)\b/i, NO = /^(no|clean|not explicit|false)\b/i;
  function setChoice(el, v) {
    const yes = v === 'yes';
    if (el.tagName === 'SELECT') {
      const o = [...el.options].find((o) => (yes ? YES : NO).test(norm(o.textContent)));
      if (!o) return 'option';
      el.value = o.value; fire(el); return 'ok';
    }
    if (el.type === 'checkbox') { if (el.checked !== yes) el.click(); return 'ok'; }
    const group = el.name ? [...document.querySelectorAll(`input[type=radio][name="${CSS.escape(el.name)}"]`)] : [el];
    const target = group.find((r) => (yes ? YES : NO).test(labelOf(r)));
    if (!target) return 'option';
    if (!target.checked) target.click();
    return 'ok';
  }
  function setFile(el, file) {
    const dt = new DataTransfer();
    dt.items.add(file);
    el.files = dt.files;
    fire(el);
    el.dispatchEvent(new Event('drop', { bubbles: true }));
  }

  function setValue(el, field, v, files) {
    if (field.kind === 'file') {
      const f = files && files[v];
      if (!f) return 'nofile';
      setFile(el, f); return 'ok';
    }
    if (field.kind === 'choice') return setChoice(el, v);
    if (el.tagName === 'SELECT') {
      const o = pickOption(el, v);
      if (!o) return 'option';
      el.value = o.value; fire(el); return 'ok';
    }
    setText(el, field.kind === 'date' ? toDate(el, v) : v);
    return 'ok';
  }

  // Stable-enough selector for a control the user pointed at
  function cssPath(el) {
    if (el.id && document.querySelectorAll('#' + CSS.escape(el.id)).length === 1) return '#' + CSS.escape(el.id);
    if (el.name) {
      const s = `${el.tagName.toLowerCase()}[name="${el.name}"]`;
      if (document.querySelectorAll(s).length === 1) return s;
    }
    const parts = [];
    for (let n = el; n && n.nodeType === 1 && n !== document.body; n = n.parentElement) {
      let i = 1, s = n.previousElementSibling;
      while (s) { if (s.tagName === n.tagName) i++; s = s.previousElementSibling; }
      parts.unshift(`${n.tagName.toLowerCase()}:nth-of-type(${i})`);
    }
    return 'body > ' + parts.join(' > ');
  }

  // Fill the page. overrides: { "track.title.0": "css selector", ... }
  function fill(adapter, pkg, files, overrides) {
    const used = new Set();
    const report = [];
    const run = (field, scope, i, value) => {
      const id = `${scope}.${field.key}${scope === 'track' ? '.' + i : ''}`;
      const entry = { id, key: field.key, label: field.label, track: scope === 'track' ? i : null, status: 'missing' };
      report.push(entry);
      if (value === undefined || value === null || value === '' || value === false && field.kind !== 'choice') {
        entry.status = field.skipIfEmpty ? 'skip' : 'empty';
        return;
      }
      let el = null;
      if (overrides && overrides[id]) el = document.querySelector(overrides[id]);
      if (!el) {
        // Controls already filled are excluded, so for track N the first
        // remaining match in page order is track N's field.
        el = findAll(field, used)[0] || null;
      }
      if (!el) return;
      used.add(el);
      // A radio group answers one question: retire all its options together
      if (el.type === 'radio' && el.name) document.querySelectorAll(`input[type=radio][name="${CSS.escape(el.name)}"]`).forEach((r) => used.add(r));
      try { entry.status = setValue(el, field, String(value), files); } catch (e) { entry.status = 'error'; }
      if (entry.status === 'ok' && el.type !== 'file') el.classList.add('rc-filled');
    };
    adapter.release.forEach((f) => run(f, 'release', 0, f.value(pkg)));
    (pkg.tracks || []).forEach((t, i) => adapter.track.forEach((f) => run(f, 'track', i, f.value(pkg, t, i))));
    return report;
  }

  window.RC_FILLER = { fill, cssPath, labelOf };
})();
