/* Minimal FLAC encoder (16-bit, 2 ch): fixed predictors + Rice coding, left/side stereo. */
(function (g) {
  const CRC8 = new Uint8Array(256), CRC16 = new Uint16Array(256);
  for (let i = 0; i < 256; i++) {
    let c = i; for (let j = 0; j < 8; j++) c = c & 0x80 ? ((c << 1) ^ 0x07) & 0xff : (c << 1) & 0xff; CRC8[i] = c;
    let d = i << 8; for (let j = 0; j < 8; j++) d = d & 0x8000 ? ((d << 1) ^ 0x8005) & 0xffff : (d << 1) & 0xffff; CRC16[i] = d;
  }
  function Writer(size) { this.buf = new Uint8Array(size); this.pos = 0; this.acc = 0; this.n = 0; }
  Writer.prototype.grow = function () { const b = new Uint8Array(this.buf.length * 2); b.set(this.buf); this.buf = b; };
  Writer.prototype.bits = function (v, n) { // n <= 24
    v &= (1 << n) - 1; this.acc = (this.acc << n) | v; this.n += n;
    while (this.n >= 8) { if (this.pos >= this.buf.length) this.grow(); this.n -= 8; this.buf[this.pos++] = (this.acc >>> this.n) & 0xff; }
    this.acc &= (1 << this.n) - 1;
  };
  Writer.prototype.zeros = function (q) { while (q > 16) { this.bits(0, 16); q -= 16; } if (q) this.bits(0, q); };
  Writer.prototype.align = function () { if (this.n) this.bits(0, 8 - this.n); };
  Writer.prototype.bytes = function (arr) { for (const b of arr) this.bits(b, 8); };

  const zz = r => (r >= 0 ? 2 * r : -2 * r - 1);
  function residual(x, o, i) {
    switch (o) {
      case 0: return x[i];
      case 1: return x[i] - x[i - 1];
      case 2: return x[i] - 2 * x[i - 1] + x[i - 2];
      case 3: return x[i] - 3 * x[i - 1] + 3 * x[i - 2] - x[i - 3];
      default: return x[i] - 4 * x[i - 1] + 6 * x[i - 2] - 4 * x[i - 3] + x[i - 4];
    }
  }
  function plan(x, n) { // choose order and rice parameter, return estimated bits
    let allSame = true; for (let i = 1; i < n; i++) if (x[i] !== x[0]) { allSame = false; break; }
    if (allSame) return { constant: true, bits: 0 };
    let best = null;
    for (let o = 0; o <= Math.min(4, n - 1); o++) {
      let s = 0; for (let i = o; i < n; i++) s += zz(residual(x, o, i));
      if (!best || s < best.s) best = { o, s };
    }
    const m = n - best.o, mean = best.s / Math.max(m, 1);
    let k0 = mean > 1 ? Math.floor(Math.log2(mean)) : 0, bk = 0, bc = Infinity;
    for (let k = Math.max(0, k0 - 1); k <= Math.min(14, k0 + 1); k++) {
      let c = m * (k + 1); for (let i = best.o; i < n; i++) c += zz(residual(x, best.o, i)) >>> k;
      if (c < bc) { bc = c; bk = k; }
    }
    return { o: best.o, k: bk, bits: bc };
  }
  function subframe(w, x, n, bps, p) {
    w.bits(0, 1);
    if (p.constant) { w.bits(0, 6); w.bits(0, 1); w.bits(x[0], bps); return; }
    w.bits(0b001000 | p.o, 6); w.bits(0, 1);
    for (let i = 0; i < p.o; i++) w.bits(x[i], bps);
    w.bits(0, 2); w.bits(0, 4); w.bits(p.k, 4); // rice, partition order 0
    const k = p.k, mask = (1 << k) - 1;
    for (let i = p.o; i < n; i++) {
      const u = zz(residual(x, p.o, i));
      w.zeros(u >>> k); w.bits(1, 1); if (k) w.bits(u & mask, k);
    }
  }
  function utf8(num) {
    if (num < 0x80) return [num];
    const out = []; let bytes = num < 0x800 ? 2 : num < 0x10000 ? 3 : num < 0x200000 ? 4 : num < 0x4000000 ? 5 : 6;
    for (let i = bytes - 1; i > 0; i--) { out.unshift(0x80 | (num & 0x3f)); num = Math.floor(num / 64); }
    out.unshift(((0xff00 >> bytes) & 0xff) | num);
    return out;
  }
  // L, R: Int16Array of equal length; returns Uint8Array
  g.encodeFLAC = function (L, R, sr) {
    const N = L.length, BS = 4096, w = new Writer(Math.max(1 << 16, N * 3));
    w.bytes([0x66, 0x4c, 0x61, 0x43]); // fLaC
    w.bits(0x80, 8); w.bits(34, 24); // last-metadata flag, STREAMINFO, length 34
    w.bits(BS, 16); w.bits(BS, 16); w.bits(0, 24); w.bits(0, 24);
    w.bits(sr >>> 4, 16); w.bits(sr & 15, 4); w.bits(1, 3); w.bits(15, 5);
    w.bits(Math.floor(N / 2 ** 32), 4); w.bits(Math.floor(N / 65536) & 0xffff, 16); w.bits(N & 0xffff, 16);
    for (let i = 0; i < 16; i++) w.bits(0, 8); // MD5 unknown
    const S = new Int32Array(BS);
    for (let f = 0, off = 0; off < N; f++, off += BS) {
      const n = Math.min(BS, N - off), l = L.subarray(off, off + n), r = R.subarray(off, off + n), s = S.subarray(0, n);
      for (let i = 0; i < n; i++) s[i] = l[i] - r[i];
      const pl = plan(l, n), pr = plan(r, n), ps = plan(s, n);
      const side = ps.bits + n < pr.bits; // side needs one extra bit per warm-up sample; rough check
      const start = w.pos;
      const hdr = [0xff, 0xf8, ((n === BS ? 12 : 7) << 4) | 9, ((side ? 8 : 1) << 4) | (4 << 1)];
      hdr.push(...utf8(f));
      if (n !== BS) hdr.push((n - 1) >> 8, (n - 1) & 0xff);
      let c = 0; for (const b of hdr) c = CRC8[c ^ b];
      w.bytes(hdr); w.bits(c, 8);
      subframe(w, l, n, 16, pl);
      if (side) subframe(w, s, n, 17, ps); else subframe(w, r, n, 16, pr);
      w.align();
      let c16 = 0; for (let i = start; i < w.pos; i++) c16 = ((c16 << 8) & 0xffff) ^ CRC16[(c16 >> 8) ^ w.buf[i]];
      w.bits(c16 >> 8, 8); w.bits(c16 & 0xff, 8);
    }
    return w.buf.subarray(0, w.pos);
  };
})(typeof self !== 'undefined' ? self : globalThis);
