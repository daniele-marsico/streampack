/* StreamPack check: finds what is wrong with the ORIGINAL file before it is converted.
   Everything runs on the device: nothing is uploaded. Used by index.html (window.SPCheck)
   and by the Node tests in tools/check.test.mjs. */
(function (root) {
  'use strict';
  const SP = {};
  const str = (u8, o, n) => String.fromCharCode.apply(null, u8.subarray(o, o + n));
  const u32le = (u8, o) => (u8[o] | u8[o + 1] << 8 | u8[o + 2] << 16 | u8[o + 3] << 24) >>> 0;
  const u16le = (u8, o) => u8[o] | u8[o + 1] << 8;
  const u32be = (u8, o) => ((u8[o] << 24) | (u8[o + 1] << 16) | (u8[o + 2] << 8) | u8[o + 3]) >>> 0;
  const u16be = (u8, o) => (u8[o] << 8) | u8[o + 1];

  /* ---------- 1. Real format, read from the first bytes (a renamed MP3 is still an MP3) ---------- */
  function skipID3(u8) {
    let o = 0;
    while (o + 10 <= u8.length && str(u8, o, 3) === 'ID3') {
      const size = (u8[o + 6] & 127) << 21 | (u8[o + 7] & 127) << 14 | (u8[o + 8] & 127) << 7 | (u8[o + 9] & 127);
      o += 10 + size + ((u8[o + 5] & 0x10) ? 10 : 0);
    }
    return o;
  }
  SP.sniff = function (u8) {
    if (!u8 || u8.length < 12) return { kind: '', off: 0 };
    const off = skipID3(u8);
    const s = n => str(u8, off, n);
    let kind = '';
    if ((s(4) === 'RIFF' || s(4) === 'RF64') && str(u8, off + 8, 4) === 'WAVE') kind = 'wav';
    else if (s(4) === 'fLaC') kind = 'flac';
    else if (s(4) === 'FORM' && /^AIF[FC]$/.test(str(u8, off + 8, 4))) kind = 'aiff';
    else if (s(4) === 'OggS') kind = 'ogg';
    else if (str(u8, off + 4, 4) === 'ftyp') kind = /^(qt  )$/.test(str(u8, off + 8, 4)) ? 'mov' : 'm4a';
    else if (s(4) === 'caff') kind = 'caf';
    else if (s(4) === '#!AM') kind = 'amr';
    else if (u8[off] === 0xFF && (u8[off + 1] & 0xE0) === 0xE0) kind = (u8[off + 1] & 0x06) === 0 ? 'aac' : 'mp3';
    else if (off > 0) kind = 'mp3'; // ID3 tag followed by something we can't read: almost always MP3
    return { kind, off };
  };
  const LOSSY = new Set(['mp3', 'aac', 'm4a', 'ogg', 'amr', 'mov']);
  SP.isLossy = k => LOSSY.has(k);
  const ALIAS = { aif: 'aiff', aifc: 'aiff', mp4: 'm4a', m4v: 'm4a', '3gp': 'm4a', opus: 'ogg', oga: 'ogg', wave: 'wav', mpeg: 'mp3', mp2: 'mp3' };
  SP.extOf = name => { const m = /\.([a-z0-9]+)$/i.exec(name || ''); const e = m ? m[1].toLowerCase() : ''; return ALIAS[e] || e; };
  SP.label = k => ({ wav: 'WAV', flac: 'FLAC', aiff: 'AIFF', ogg: 'OGG', m4a: 'M4A/MP4', mov: 'MOV', caf: 'CAF', amr: 'AMR', aac: 'AAC', mp3: 'MP3' })[k] || (k || '?').toUpperCase();

  /* ---------- 2. Original specs from the header (decodeAudioData hides them) ---------- */
  function ext80(u8, o) { // IEEE 754 80-bit extended (AIFF sample rate)
    const e = ((u8[o] & 0x7F) << 8) | u8[o + 1];
    const m = u32be(u8, o + 2) * 4294967296 + u32be(u8, o + 6);
    return e === 0 && m === 0 ? 0 : Math.round(m * Math.pow(2, e - 16383 - 63));
  }
  SP.header = function (u8) {
    const { kind, off } = SP.sniff(u8);
    const out = { kind };
    try {
      if (kind === 'wav') {
        for (let o = off + 12; o + 8 <= u8.length;) {
          const id = str(u8, o, 4), size = u32le(u8, o + 4);
          if (id === 'fmt ') {
            let fmt = u16le(u8, o + 8);
            out.ch = u16le(u8, o + 10); out.sr = u32le(u8, o + 12); out.bits = u16le(u8, o + 22);
            if (fmt === 0xFFFE && size >= 40) fmt = u16le(u8, o + 32);
            out.float = fmt === 3; out.compressed = fmt !== 1 && fmt !== 3;
            break;
          }
          o += 8 + size + (size & 1);
        }
      } else if (kind === 'flac') {
        const b = off + 8 + 10; // STREAMINFO data starts after "fLaC" + 4-byte block header
        out.sr = (u8[b] << 12) | (u8[b + 1] << 4) | (u8[b + 2] >> 4);
        out.ch = ((u8[b + 2] >> 1) & 7) + 1;
        out.bits = (((u8[b + 2] & 1) << 4) | (u8[b + 3] >> 4)) + 1;
      } else if (kind === 'aiff') {
        for (let o = off + 12; o + 8 <= u8.length;) {
          const id = str(u8, o, 4), size = u32be(u8, o + 4);
          if (id === 'COMM') { out.ch = u16be(u8, o + 8); out.bits = u16be(u8, o + 14); out.sr = ext80(u8, o + 16); break; }
          o += 8 + size + (size & 1);
        }
      }
    } catch (e) { /* partial header: keep what we have */ }
    return out;
  };

  // AIFF/AIFC PCM → Float32 channels. Browsers on Android/Chrome can't decode AIFF, so StreamPack does it.
  SP.decodeAIFF = function (u8) {
    const { kind, off } = SP.sniff(u8);
    if (kind !== 'aiff') return null;
    const aifc = str(u8, off + 8, 4) === 'AIFC';
    let ch = 0, frames = 0, bits = 0, sr = 0, comp = 'NONE', data = -1;
    for (let o = off + 12; o + 8 <= u8.length;) {
      const id = str(u8, o, 4), size = u32be(u8, o + 4);
      if (id === 'COMM') { ch = u16be(u8, o + 8); frames = u32be(u8, o + 10); bits = u16be(u8, o + 14); sr = ext80(u8, o + 16); if (aifc) comp = str(u8, o + 26, 4); }
      else if (id === 'SSND') data = o + 16 + u32be(u8, o + 8);
      o += 8 + size + (size & 1);
    }
    const le = comp === 'sowt', fl = /^fl32$/i.test(comp);
    if (!ch || !sr || data < 0 || !(comp === 'NONE' || le || fl) || (fl ? bits !== 32 : ![8, 16, 24, 32].includes(bits))) return null;
    const bps = bits / 8, avail = Math.floor((u8.length - data) / (bps * ch)), n = Math.min(frames || avail, avail);
    const v = new DataView(u8.buffer, u8.byteOffset, u8.byteLength), out = [];
    for (let c = 0; c < ch; c++) out.push(new Float32Array(n));
    for (let i = 0, o = data; i < n; i++) for (let c = 0; c < ch; c++, o += bps) {
      let x;
      if (fl) x = v.getFloat32(o, le);
      else if (bits === 8) x = v.getInt8(o) / 128;
      else if (bits === 16) x = v.getInt16(o, le) / 32768;
      else if (bits === 24) { const a = le ? (u8[o + 2] << 16 | u8[o + 1] << 8 | u8[o]) : (u8[o] << 16 | u8[o + 1] << 8 | u8[o + 2]); x = ((a << 8) >> 8) / 8388608; }
      else x = v.getInt32(o, le) / 2147483648;
      out[c][i] = x;
    }
    return { sr, ch, chans: out };
  };

  /* ---------- 3. Clipping, DC offset, sample peak; silence at the edges (after DC removal) ---------- */
  SP.scan = function (L, R) {
    const n = L.length, mono = L === R, CLIP = 0.999;
    let peak = 0, sumL = 0, sumR = 0, clips = 0, runL = 0, runR = 0;
    for (let i = 0; i < n; i++) {
      const l = L[i], r = R[i], al = l < 0 ? -l : l, ar = r < 0 ? -r : r;
      if (al > peak) peak = al; if (ar > peak) peak = ar;
      sumL += l; sumR += r;
      if (al >= CLIP) { if (++runL === 3) clips++; } else runL = 0;
      if (!mono) { if (ar >= CLIP) { if (++runR === 3) clips++; } else runR = 0; }
    }
    return { peak, clips, dc: [n ? sumL / n : 0, n ? sumR / n : 0] };
  };
  // Silence = no movement around the level of the edge sample, so a constant offset can't hide it
  SP.edges = function (L, R, sr) {
    const n = L.length, SIL = 0.001; // -60 dBFS
    if (!n) return { silent: true, lead: 0, tail: 0, first: -1, last: -1 };
    const moved = (i, bl, br) => { const l = L[i] - bl, r = R[i] - br; return l > SIL || l < -SIL || r > SIL || r < -SIL; };
    // baseline 20 ms in from each edge: resamplers ramp in/out over the very first and last samples
    const g = Math.min(Math.round(0.02 * sr), n - 1), a = g, z = n - 1 - g;
    let first = -1, last = -1;
    for (let i = a, bl = L[a], br = R[a]; i < n; i++) if (moved(i, bl, br)) { first = i; break; }
    if (first < 0) return { silent: true, lead: n / sr, tail: 0, first: -1, last: -1 };
    for (let i = Math.max(z, first), bl = L[i], br = R[i]; i >= first; i--) if (moved(i, bl, br)) { last = i; break; }
    if (last < 0) last = n - 1;
    return { silent: false, lead: first / sr, tail: (n - 1 - last) / sr, first, last };
  };
  SP.removeDC = function (L, R, dc) {
    const [a, b] = dc;
    if (a) for (let i = 0; i < L.length; i++) L[i] -= a;
    if (R !== L && b) for (let i = 0; i < R.length; i++) R[i] -= b;
  };

  /* ---------- 4. True peak, ITU-R BS.1770-4 Annex 2 (4x oversampling, 48-tap polyphase FIR) ---------- */
  const H = [
    [0.0017089843750, 0.0109863281250, -0.0196533203125, 0.0332031250000, -0.0594482421875, 0.1373291015625, 0.9721679687500, -0.1022949218750, 0.0476074218750, -0.0266113281250, 0.0148925781250, -0.0083007812500],
    [-0.0291748046875, 0.0292968750000, -0.0517578125000, 0.0891113281250, -0.1665039062500, 0.4650878906250, 0.7797851562500, -0.2003173828125, 0.1015625000000, -0.0582275390625, 0.0330810546875, -0.0189208984375],
    [-0.0189208984375, 0.0330810546875, -0.0582275390625, 0.1015625000000, -0.2003173828125, 0.7797851562500, 0.4650878906250, -0.1665039062500, 0.0891113281250, -0.0517578125000, 0.0292968750000, -0.0291748046875],
    [-0.0083007812500, 0.0148925781250, -0.0266113281250, 0.0476074218750, -0.1022949218750, 0.9721679687500, 0.1373291015625, -0.0594482421875, 0.0332031250000, -0.0196533203125, 0.0109863281250, 0.0017089843750],
  ];
  function tpChannel(x, gate) {
    // Only the stretches near the loudest samples can hold inter-sample peaks above the sample peak,
    // so the filter runs where |x| is within 6 dB of the peak: same result, a fraction of the work on a phone.
    let m = 0;
    const n = x.length;
    for (let i = 11; i < n; i++) {
      const a = x[i - 6], b = x[i - 5];
      if ((a < 0 ? -a : a) < gate && (b < 0 ? -b : b) < gate) continue;
      for (let p = 0; p < 4; p++) {
        const h = H[p];
        let y = 0;
        for (let j = 0; j < 12; j++) y += h[j] * x[i - j];
        if (y < 0) y = -y;
        if (y > m) m = y;
      }
    }
    return m;
  }
  SP.truePeak = function (L, R, samplePeak) {
    const gate = samplePeak * 0.5;
    let m = Math.max(samplePeak, tpChannel(L, gate));
    if (R !== L) m = Math.max(m, tpChannel(R, gate));
    return m;
  };
  SP.db = x => 20 * Math.log10(Math.max(x, 1e-9));

  /* ---------- 5. Loudness (BS.1770 integrated) + loudness range (EBU Tech 3342), one pass ---------- */
  SP.kWeight = function (L, R, sr) {
    let K = Math.tan(Math.PI * 1681.974450955533 / sr), Q = 0.7071752369554196;
    const Vh = Math.pow(10, 3.999843853973347 / 20), Vb = Math.pow(Vh, 0.4996667741545416);
    let a0 = 1 + K / Q + K * K;
    const sb = [(Vh + Vb * K / Q + K * K) / a0, 2 * (K * K - Vh) / a0, (Vh - Vb * K / Q + K * K) / a0], sa = [2 * (K * K - 1) / a0, (1 - K / Q + K * K) / a0];
    K = Math.tan(Math.PI * 38.13547087602444 / sr); Q = 0.5003270373238773; a0 = 1 + K / Q + K * K;
    const ha = [2 * (K * K - 1) / a0, (1 - K / Q + K * K) / a0];
    const run = x => {
      const y = new Float32Array(x.length);
      let x1 = 0, x2 = 0, y1 = 0, y2 = 0, z1 = 0, z2 = 0;
      for (let i = 0; i < x.length; i++) {
        const v = x[i], s1 = sb[0] * v + sb[1] * x1 + sb[2] * x2 - sa[0] * y1 - sa[1] * y2;
        x2 = x1; x1 = v; y2 = y1; y1 = s1;
        const s2 = s1 - 2 * z1 + z2 - ha[0] * (y[i - 1] || 0) - ha[1] * (y[i - 2] || 0);
        z2 = z1; z1 = s1; y[i] = s2;
      }
      return y;
    };
    const kL = run(L);
    return [kL, R === L ? kL : run(R)];
  };
  SP.loudness = function (kL, kR, sr) {
    const n = kL.length, P = new Float64Array(n + 1);
    for (let i = 0; i < n; i++) P[i + 1] = P[i] + kL[i] * kL[i] + kR[i] * kR[i];
    const ld = x => -0.691 + 10 * Math.log10(x);
    // integrated: 400 ms blocks, 75% overlap, gates -70 LUFS and -10 LU
    const bs = Math.round(0.4 * sr), st = Math.round(0.1 * sr), z = [];
    if (n < bs) z.push(P[n] / Math.max(n, 1)); else for (let i = 0; i + bs <= n; i += st) z.push((P[i + bs] - P[i]) / bs);
    const abs = z.filter(x => ld(x) > -70);
    let I = -70;
    if (abs.length) {
      const rel = ld(abs.reduce((a, b) => a + b, 0) / abs.length) - 10;
      const g = abs.filter(x => ld(x) > rel);
      I = ld(g.reduce((a, b) => a + b, 0) / g.length);
    }
    // range: 3 s short-term windows every 100 ms, gates -70 LUFS and -20 LU, 10th→95th percentile
    let LRA = null;
    const ws = Math.round(3 * sr);
    if (n >= ws) {
      const s = [];
      for (let i = 0; i + ws <= n; i += st) s.push((P[i + ws] - P[i]) / ws);
      const a = s.filter(x => ld(x) > -70);
      if (a.length) {
        const rel = ld(a.reduce((p, q) => p + q, 0) / a.length) - 20;
        const v = a.filter(x => ld(x) > rel).map(ld).sort((p, q) => p - q);
        if (v.length) { const q = f => v[Math.min(v.length - 1, Math.round(f * (v.length - 1)))]; LRA = q(0.95) - q(0.10); }
      }
    }
    return { I, LRA };
  };

  /* ---------- 6. Codes: ISRC and UPC/EAN barcode ---------- */
  SP.isrc = function (raw) {
    const v = String(raw || '').toUpperCase().replace(/^ISRC[:\s]*/, '').replace(/[\s\-_.]/g, '');
    if (!v) return { ok: null, v };
    if (v.length !== 12) return { ok: false, v, err: 'len' };
    if (!/^[A-Z]{2}[A-Z0-9]{3}\d{7}$/.test(v)) return { ok: false, v, err: 'fmt' };
    return { ok: true, v, pretty: `${v.slice(0, 2)}-${v.slice(2, 5)}-${v.slice(5, 7)}-${v.slice(7)}`, year: v.slice(5, 7) };
  };
  SP.barcode = function (raw) {
    const v = String(raw || '').replace(/[\s\-]/g, '');
    if (!v) return { ok: null, v };
    if (!/^\d+$/.test(v)) return { ok: false, v, err: 'fmt' };
    if (v.length !== 12 && v.length !== 13) return { ok: false, v, err: 'len' };
    const d = v.split('').map(Number), chk = d.pop();
    let sum = 0;
    for (let i = d.length - 1, w = 3; i >= 0; i--, w = 4 - w) sum += d[i] * w;
    const want = (10 - sum % 10) % 10;
    return want === chk ? { ok: true, v, type: v.length === 12 ? 'UPC' : 'EAN' } : { ok: false, v, err: 'check', want };
  };

  /* ---------- 7. Cover: colour mode and transparency of the original, "blank" covers ---------- */
  SP.imageInfo = function (u8) {
    const out = {};
    if (!u8 || u8.length < 30) return out;
    if (u8[0] === 0xFF && u8[1] === 0xD8) {
      out.kind = 'jpg';
      for (let o = 2; o + 9 < u8.length;) {
        if (u8[o] !== 0xFF) { o++; continue; }
        const mk = u8[o + 1];
        if (mk === 0xFF) { o++; continue; }
        if (mk === 0xD8 || mk === 0x01 || (mk >= 0xD0 && mk <= 0xD7)) { o += 2; continue; }
        const len = u16be(u8, o + 2);
        if (mk >= 0xC0 && mk <= 0xCF && mk !== 0xC4 && mk !== 0xC8 && mk !== 0xCC) {
          const nc = u8[o + 9];
          out.mode = nc === 4 ? 'cmyk' : nc === 1 ? 'gray' : 'rgb';
          break;
        }
        if (mk === 0xDA) break;
        o += 2 + len;
      }
    } else if (str(u8, 1, 3) === 'PNG') {
      out.kind = 'png';
      const t = u8[25];
      out.mode = t === 0 || t === 4 ? 'gray' : 'rgb';
      out.alpha = t === 4 || t === 6;
    } else if (str(u8, 0, 4) === 'RIFF' && str(u8, 8, 4) === 'WEBP') out.kind = 'webp';
    return out;
  };
  // pixels: RGBA bytes of a small thumbnail. Returns the spread of brightness (0 = one flat colour).
  SP.flatness = function (px) {
    let s = 0, s2 = 0, n = 0;
    for (let i = 0; i < px.length; i += 4) { const y = 0.2126 * px[i] + 0.7152 * px[i + 1] + 0.0722 * px[i + 2]; s += y; s2 += y * y; n++; }
    if (!n) return 0;
    const m = s / n;
    return Math.sqrt(Math.max(0, s2 / n - m * m));
  };

  /* ---------- 8. Whole-file report (browser only): used by the LUFS checker pages ---------- */
  SP.analyze = async function (file) {
    const ab = await file.arrayBuffer();
    const h = SP.header(new Uint8Array(ab.slice(0, 65536)));
    const OAC = root.OfflineAudioContext || root.webkitOfflineAudioContext;
    const sr = Math.max(8000, Math.min(48000, h.sr || 48000)); // hi-res is measured at 48 kHz: same LUFS, much less memory on a phone
    let buf = null;
    if (h.kind === 'aiff') {
      const p = SP.decodeAIFF(new Uint8Array(ab));
      if (p) {
        const n = Math.max(1, p.chans[0].length), ctx = new OAC(p.ch, Math.max(1, Math.ceil(n * sr / p.sr)), sr), b = ctx.createBuffer(p.ch, n, p.sr);
        p.chans.forEach((c, i) => b.getChannelData(i).set(c));
        if (p.sr === sr) buf = b;
        else { const s = ctx.createBufferSource(); s.buffer = b; s.connect(ctx.destination); s.start(); buf = await ctx.startRendering(); }
      }
    }
    if (!buf) buf = await new Promise((res, rej) => { const c = new OAC(2, 1, sr); const q = c.decodeAudioData(ab, res, rej); if (q && q.then) q.then(res, rej); });
    const rate = buf.sampleRate, L = buf.getChannelData(0), R = buf.numberOfChannels > 1 ? buf.getChannelData(1) : L;
    const sc = SP.scan(L, R), ed = SP.edges(L, R, rate), tp = SP.truePeak(L, R, sc.peak);
    const k = SP.kWeight(L, R, rate), lo = SP.loudness(k[0], k[1], rate);
    return { h, ext: SP.extOf(file.name), ch: h.ch || buf.numberOfChannels, dur: L.length / rate, peak: sc.peak, clips: sc.clips, dc: sc.dc,
      silent: ed.silent, lead: ed.lead, tail: ed.tail, tp, I: lo.I, LRA: lo.LRA };
  };

  if (typeof module === 'object' && module.exports) module.exports = SP; else root.SPCheck = SP;
})(typeof self !== 'undefined' ? self : this);
