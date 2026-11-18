// English by default, Italian when the browser is in Italian.
(function () {
  const it = /^it\b/i.test(navigator.language || '');
  const T = {
    en: {
      fill: 'Fill the form', files: 'Files for this upload', cover: 'Cover', track: 'Track', tracksWord: 'tracks',
      noPkg: 'No release ready yet. Open the side panel and prepare it.', openPanel: 'Open release package',
      ok: 'filled', missing: 'not found', empty: 'empty in package', option: 'option not in list', nofile: 'choose the file above', error: 'error', skip: '',
      point: 'Point it out', pickHint: 'Click the field on the page for: ', saved: 'Field remembered. Fill again.',
      review: 'Check everything, then press the site\'s submit button yourself.', reset: 'Forget pointed fields',
      summary: (a, b) => `${a} of ${b} fields filled`,
    },
    it: {
      fill: 'Compila il form', files: 'File per questo caricamento', cover: 'Copertina', track: 'Traccia', tracksWord: 'tracce',
      noPkg: 'Nessuna release pronta. Apri il pannello laterale e preparala.', openPanel: 'Apri pacchetto release',
      ok: 'compilato', missing: 'non trovato', empty: 'vuoto nel pacchetto', option: 'opzione non presente', nofile: 'scegli il file qui sopra', error: 'errore', skip: '',
      point: 'Indica il campo', pickHint: 'Clicca sulla pagina il campo per: ', saved: 'Campo memorizzato. Compila di nuovo.',
      review: 'Controlla tutto, poi premi tu il pulsante di invio del sito.', reset: 'Dimentica i campi indicati',
      summary: (a, b) => `${a} campi su ${b} compilati`,
    },
  };
  window.RC_T = T[it ? 'it' : 'en'];
  window.RC_LANG = it ? 'it' : 'en';
})();
