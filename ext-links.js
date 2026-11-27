// Solo nell'app Android/iOS (Capacitor). Sul sito web non fa nulla.
// 1) Link esterni (es. "Prova VideoGen"): si aprono nel browser di sistema (Custom Tab su Android,
//    Safari View su iOS) sopra l'app, invece di affidarsi a target="_blank" nella WebView.
// 2) Link interni a una cartella (es. /video/, /lufs-checker/): il server locale di Capacitor risponde
//    a ogni percorso senza "." con la home (index.html della radice), quindi la pagina si ricaricava
//    sulla home rotta (script relativi non trovati) invece di aprire la pagina giusta.
//    Qui il link punta direttamente al file: /video/ -> /video/index.html
(function () {
  var C = window.Capacitor;
  if (!C || !C.isNativePlatform || !C.isNativePlatform()) return;
  // 3) Le pagine video e tools chiamano /api/...: nell'app non c'è il server, quindi le chiamate vanno al sito
  //    (CapacitorHttp le fa passare dal canale nativo, senza problemi di CORS), come già fa la home per /api/cover.
  var f0 = window.fetch;
  if (f0) window.fetch = function (r, o) {
    if (typeof r === 'string' && r.indexOf('/api/') === 0) r = 'https://streampack.pages.dev' + r;
    return f0.call(window, r, o);
  };
  document.addEventListener('click', function (e) {
    if (e.defaultPrevented || e.button > 0) return;
    var a = e.target && e.target.closest && e.target.closest('a[href]');
    if (!a || a.hasAttribute('download')) return;
    var u;
    try { u = new URL(a.getAttribute('href'), location.href); } catch (_) { return; }
    if (!/^https?:$/.test(u.protocol)) return;
    if (u.host === location.host) {
      var p = u.pathname, last = p.split('/').pop();
      if (p === '/' || last.indexOf('.') >= 0) return; // home o file: il server locale li serve bene
      e.preventDefault();
      // /video/ -> /video/index.html ; /privacy -> /privacy.html (o /privacy/index.html se è una cartella)
      var cands = /\/$/.test(p) ? [p + 'index.html'] : [p + '.html', p + '/index.html'];
      var go = function (path) { var t = new URL(u.href); t.pathname = path; location.href = t.href; };
      if (cands.length === 1) return go(cands[0]);
      var get = window.CapacitorWebFetch || window.fetch; // il fetch originale della WebView, non quello di CapacitorHttp
      (function next(i) {
        if (i >= cands.length - 1) return go(cands[cands.length - 1]);
        get.call(window, cands[i]).then(function (r) { r.ok ? go(cands[i]) : next(i + 1); }, function () { next(i + 1); });
      })(0);
      return;
    }
    e.preventDefault();
    var B = C.Plugins && C.Plugins.Browser;
    var fallback = function () { location.href = u.href; }; // Capacitor lo passa comunque al browser esterno
    if (B && B.open) B.open({ url: u.href }).catch(fallback);
    else fallback();
  }, true);
})();
