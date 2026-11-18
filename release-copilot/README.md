# UploadMySong – Release Copilot

Estensione Chrome: prepari la release **una volta** (artista, titoli, generi, autori, explicit, data…) e poi la copi campo per campo nel form di **DistroKid, RouteNote, TuneCore o CD Baby**, nell'ordine giusto.

## Come si usa
1. **1 · Prepara**: compili il pacchetto. I controlli segnalano gli errori che fanno rifiutare le release (titoli in maiuscolo, "feat." nel titolo, autori senza cognome, data troppo vicina). **Suggerisci con AI** propone genere, lingua, descrizione e pitch Spotify.
2. **2 · Carica**: scegli il distributore, apri il sito, premi il pulsante verde e incolla (Ctrl+V). Il pulsante passa da solo al campo successivo.

## Perché copia e non compila da sola
I Termini di DistroKid vietano script e software di terzi sulle loro pagine e finestre sopra il sito. L'estensione quindi non tocca mai le pagine dei distributori: usa solo gli appunti. Nessun rischio di sospensione dell'account.

## Struttura
| File | Cosa fa |
|---|---|
| `extension/panel/distributors.js` | Ordine dei campi di ogni distributore. Per aggiungerne uno basta un blocco nuovo. |
| `extension/panel/panel.*` | Pannello laterale (Prepara / Carica) |
| `test/run_test.py` | Test in Chrome headless della copia guidata |

AI: endpoint `/api/release` del sito (Workers AI gratuito, 20 richieste al giorno per IP).

## Installarla (sviluppo)
Decomprimi `uploadmysong-extension.zip` → `chrome://extensions` → **Modalità sviluppatore** → **Carica estensione non pacchettizzata** → cartella decompressa.
