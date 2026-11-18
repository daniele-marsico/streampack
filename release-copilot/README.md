# StreamPack Release Copilot

Estensione Chrome: prepari la release **una volta** (artista, titoli, generi, autori, explicit, data…) e la usi per compilare in un clic i form di caricamento di **DistroKid** e **RouteNote**. L'invio lo premi sempre tu: l'estensione non clicca mai "Submit".

## Come funziona
- **Pannello laterale** (icona dell'estensione): il pacchetto release, salvato nel browser. Controlli automatici sugli errori che fanno rifiutare le release (titoli in maiuscolo, "feat." nel titolo, autori senza cognome, data troppo vicina). Pulsante **Suggerisci con AI** per genere, lingua, descrizione e pitch Spotify (endpoint `/api/release` del server StreamPack, Workers AI gratuito, 20 richieste al giorno per IP).
- **Sul sito del distributore** compare il pulsante *Release Copilot* in basso a destra: scegli copertina e audio (meglio se convertiti con StreamPack), premi **Compila il form**.
- I campi si trovano per **etichetta** (label, aria-label, placeholder, testo vicino), non con selettori fissi. Se un campo non viene trovato: **Indica il campo** → clic sul campo della pagina → viene ricordato per quel sito.
- Nessuna AI nella compilazione: è deterministica, veloce e gratuita.

## Struttura
| File | Cosa fa |
|---|---|
| `extension/adapters/*.js` | Mappa campi pacchetto → etichette del form, una per distributore. Per aggiungere TuneCore, CD Baby ecc. basta un file nuovo. |
| `extension/filler.js` | Motore di compilazione (testo, date, menu, sì/no, file) compatibile con i form React |
| `extension/content.js` | Pannellino sulla pagina del distributore, modalità "indica il campo" |
| `extension/panel/` | Pannello laterale con il pacchetto release |
| `test/` | Form finto stile DistroKid + test in Chrome headless (`python3 test/run_test.py`) |

## Installarla (sviluppo)
1. Scarica `release-copilot.zip` e decomprimilo.
2. Chrome → `chrome://extensions` → attiva **Modalità sviluppatore** → **Carica estensione non pacchettizzata** → scegli la cartella `extension`.

## Da fare
- Verificare le etichette sui form veri di DistroKid e RouteNote (servono account e Chrome collegato).
- Controllare i Termini di servizio di ciascun distributore prima della pubblicazione sul Chrome Web Store.
