// App Android/iOS (Capacitor): i link esterni (es. "Prova VideoGen") si aprono nel browser di sistema
// (Custom Tab su Android, Safari View su iOS) sopra l'app, invece di affidarsi a target="_blank" nella WebView.
// Sul sito web non fa nulla.
(function () {
  var C = window.Capacitor;
  if (!C || !C.isNativePlatform || !C.isNativePlatform()) return;
  document.addEventListener('click', function (e) {
    var a = e.target && e.target.closest && e.target.closest('a[href]');
    if (!a) return;
    var u;
    try { u = new URL(a.getAttribute('href'), location.href); } catch (_) { return; }
    if (!/^https?:$/.test(u.protocol) || u.host === location.host) return;
    e.preventDefault();
    var B = C.Plugins && C.Plugins.Browser;
    var fallback = function () { location.href = u.href; }; // Capacitor lo passa comunque al browser esterno
    if (B && B.open) B.open({ url: u.href }).catch(fallback);
    else fallback();
  }, true);
})();
