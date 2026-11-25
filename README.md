# StreamPack

Converti audio e copertina negli standard di Spotify e dei distributori (DistroKid, RouteNote, TuneCore, CD Baby…), dal telefono.

- Audio → FLAC / MP3 320 kbps / WAV, 44,1 kHz 16-bit stereo, volume opzionale a -14 LUFS
- Copertina → 3000×3000 JPG RGB, anche generata con AI (Cloudflare Workers AI, piano gratuito)
- Controllo del file originale prima della conversione (`check.js`): formato reale letto dai byte (un MP3 rinominato .wav viene scoperto), specifiche originali, sorgente compressa, mono, clipping, silenzi a inizio/fine, DC offset, loudness integrata e range (LRA), true peak ITU-R BS.1770-4
- Correzioni automatiche: DC offset, silenzi (opzione "Taglia i silenzi"), limite -1 dBTP in true peak con il volume per Spotify
- Copertina: CMYK → RGB, trasparenza, copertine "a tinta unita" che i distributori rifiutano
- Verifica ISRC e UPC/EAN (cifra di controllo), tutto sul telefono
- Web app installabile (PWA), 6 lingue, i file restano sul telefono

Live: https://streampack.pages.dev · Hosting: Cloudflare Pages (`_worker.js` gestisce `/api/cover`, binding Workers AI `AI`).
MP3 encoding: [LAME](https://lame.sourceforge.io) (LGPL).
