# StreamPack – kit per community (Reddit, Product Hunt, AlternativeTo, video brevi)

Regola d'oro: niente pubblicità. Si aiuta qualcuno che ha un problema reale e si linka la guida giusta,
dicendo sempre che il tool l'hai fatto tu. Su Reddit vale la regola 9:1: su 10 interventi, al massimo 1 con un tuo link.
Un account nuovissimo che posta subito link viene preso per spam: prima qualche giorno di commenti utili senza link.

Link da usare (si aprono nella lingua giusta e portano dritti allo strumento):
- Dimensioni copertina: https://streampack.pages.dev/album-cover-size/
- Copertina rifiutata: https://streampack.pages.dev/cover-art-rejected/
- Formato audio DistroKid: https://streampack.pages.dev/audio-format-for-distrokid/
- -14 LUFS Spotify: https://streampack.pages.dev/spotify-lufs/
- App: https://streampack.pages.dev

Il Play Store è ancora in test chiuso: per ora si linka sempre la web app.

---

## 1. Dove postare e con quali regole

| Dove | Cosa si può fare |
|---|---|
| r/WeAreTheMusicMakers | Autopromozione solo nel **Weekly Promotion Thread** (fissato ogni settimana). Nel **Weekly Gear Thread** la gente chiede quali strumenti usare: lì si risponde. |
| r/aiMusic, r/AI_Music | Tool solo nel megathread di autopromozione o con ok dei moderatori. Pubblico perfetto: chi fa musica con Suno/Udio e poi la distribuisce. |
| r/SideProject | Post "ho costruito questo" ammessi: è il posto per il post di lancio. |
| r/musicmarketing, r/independentmusic | Leggere le regole del giorno: si risponde alle domande su distribuzione, copertine, rifiuti. |
| Product Hunt | Un lancio (una volta sola), meglio di martedì–giovedì. |
| AlternativeTo | Scheda gratuita come alternativa a CloudConvert e Online Audio Converter. |
| Gruppi Facebook di musicisti | Solo dove l'autopromozione è ammessa, postando come pagina StreamPack. |

---

## 2. Risposte pronte (Reddit, forum, gruppi) – inglese

Da adattare alla domanda. Mai copiate uguali in più posti.

**"DistroKid rejected my cover art"**
> The usual culprits: not perfectly square, smaller than 3000×3000, CMYK instead of RGB, or content issues: text that doesn't match your artist name/title exactly, URLs or @handles, store logos, or "new/exclusive" badges. Also don't send the file through WhatsApp/Telegram, they shrink it.
> I put the full checklist here: https://streampack.pages.dev/cover-art-rejected/ (disclosure: I built the free tool on that page, it crops/converts the image to a 3000×3000 RGB JPG on your device, no upload).

**"What size should my cover art be?"**
> 3000×3000 px, square, RGB, JPG under 10 MB works everywhere. Spotify itself accepts 640–10,000 px, but Apple Music wants at least 3000×3000, so that's the safe size. DPI doesn't matter for streaming, only pixels.
> Table by platform: https://streampack.pages.dev/album-cover-size/ (I made the free resizer there, disclosure).

**"What audio format should I upload to DistroKid?"**
> If your DAW already gives you a WAV or FLAC master, upload that as it is (Spotify actually prefers the native master, 24-bit is fine). DistroKid takes WAV, MP3, M4A, FLAC, AIFF or WMA, and 16-bit 44.1 kHz WAV is the typical spec. If your file is an M4A/MP4/OGG, a phone recording or 48 kHz and you just want something every distributor accepts, convert it to stereo 44.1 kHz WAV or FLAC.
> Comparison of distributors: https://streampack.pages.dev/audio-format-for-distrokid/ (disclosure: I built the converter there, free, no upload).

**"Should I master to -14 LUFS for Spotify?"**
> You don't have to. Spotify normalizes at playback to -14 LUFS: louder masters get turned down, quieter ones only get turned up as far as their peaks allow, and your file isn't changed. Spotify's own advice is around -14 LUFS integrated with true peaks under -1 dB, mostly to avoid extra distortion in the lossy versions.
> Short explainer: https://streampack.pages.dev/spotify-lufs/ (I made the tool there, disclosure).

---

## 3. Weekly Promotion Thread (r/WeAreTheMusicMakers) – commento

> I made a free web app for the boring part of releasing: getting your files past distributor checks.
> • Any audio (M4A, MP4, OGG, phone recordings, 48 kHz…) → stereo 44.1 kHz WAV, FLAC or MP3 320 that every distributor accepts. Optional -14 LUFS level for unmastered demos.
> • Any image → 3000×3000 RGB JPG under 10 MB, cropped square.
> No sign-up, no ads, files are processed on your device and never uploaded. Works on phone and computer: https://streampack.pages.dev
> Tell me what's missing, I'm actively improving it.

---

## 4. Post di lancio – r/SideProject

**Titolo:** I built a free app that gets a song and its cover art ready for Spotify/DistroKid in one tap

> As an indie musician I kept losing time on the same things before every release: exporting the right audio format, resizing the cover to 3000×3000, converting CMYK artwork, wondering about -14 LUFS. Online converters work, but you have to set everything by hand and they're full of ads.
>
> So I made StreamPack: drop audio or an image and you get files that every distributor accepts (stereo 44.1 kHz WAV/FLAC/MP3 320, 3000×3000 RGB JPG under 10 MB). Everything runs on your device, nothing is uploaded, no sign-up, no ads. It's in 6 languages and there are short guides on cover sizes, rejected artwork, audio formats and loudness.
>
> https://streampack.pages.dev
>
> I'd love feedback from people who release music: what else slows you down before a release?

---

## 5. Product Hunt

- **Nome:** StreamPack
- **Tagline (max 60):** Audio & cover art ready for Spotify and DistroKid, free
- **Descrizione (max 260):** Drop a track or an image and get files every distributor accepts: stereo 44.1 kHz WAV, FLAC or MP3 320 and 3000×3000 RGB cover art, with optional -14 LUFS. Runs on your device, nothing is uploaded. No sign-up, no ads, 6 languages.
- **Primo commento del maker:**
> Hi Product Hunt! I'm a musician and I built StreamPack because every release meant the same file fixes: wrong audio format, cover too small or CMYK, loudness doubts. StreamPack does them in one tap, on your phone or computer, and the files never leave your device. It's free and has no ads. I'd really like to hear what you'd add.
- **Topic:** Music, Productivity, Design Tools
- **Immagini:** store/en-1.png … en-4.png (già pronte)

---

## 6. AlternativeTo

- **Alternativa a:** CloudConvert, Online Audio Converter, Canva (ridimensionamento copertine)
- **Descrizione:** Free audio and cover art converter made for musicians. Converts any audio to stereo 44.1 kHz WAV, FLAC or MP3 320 accepted by DistroKid, TuneCore, CD Baby and Spotify, with optional -14 LUFS, and turns any image into 3000×3000 RGB cover art under 10 MB. Processing happens on your device; no sign-up, no ads.
- **Tag:** audio-converter, music-distribution, cover-art, flac, wav

---

## 7. Video brevi (Shorts, TikTok, Reels) – 15-20 secondi, registrazione dello schermo

1. **"DistroKid ha rifiutato la copertina?"** → scegli immagine → spunte 3000×3000 ✓ RGB ✓ sotto 10 MB ✓ → "Gratis, senza registrazione: streampack.pages.dev"
2. **"Il tuo brano è un M4A del telefono?"** → scegli file → WAV 44,1 kHz pronto → stesso finale
3. **"-14 LUFS: devi davvero masterizzare così?"** → 3 frasi dalla guida → tool con l'opzione attiva

Testo a schermo in inglese, voce o sottotitoli anche in italiano per i gruppi italiani.

---

## 8. Gruppi Facebook italiani – post breve

> Per chi pubblica su Spotify con DistroKid, RouteNote o simili: ho fatto un'app gratuita che prepara i file in un tocco. Audio in WAV/FLAC/MP3 320 a 44,1 kHz accettato da tutti i distributori (anche da M4A del telefono o file a 48 kHz) e copertina 3000×3000 RGB sotto i 10 MB. Niente registrazione, niente pubblicità, i file non vengono caricati da nessuna parte. https://streampack.pages.dev/it/dimensioni-copertina-album/
