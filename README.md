# StreamPack

Converti audio e copertina negli standard di Spotify e dei distributori (DistroKid, RouteNote, TuneCore, CD Baby…), dal telefono.

- Audio → FLAC / MP3 320 kbps / WAV, 44,1 kHz 16-bit stereo, volume opzionale a -14 LUFS
- Copertina → 3000×3000 JPG RGB, anche generata con AI (Cloudflare Workers AI, piano gratuito)
- Web app installabile (PWA), 6 lingue, i file restano sul telefono

Live: https://streampack.pages.dev · Hosting: Cloudflare Pages (`_worker.js` gestisce `/api/cover`, binding Workers AI `AI`).
MP3 encoding: [LAME](https://lame.sourceforge.io) (LGPL).
