# Guide per musicisti in 6 lingue (copertina e audio per Spotify, DistroKid ecc.), con lo strumento di StreamPack
# che si apre nella lingua della pagina. Uso: python3 seo/guide.py  -> scrive le cartelle e stampa gli URL.
# Fonti dei requisiti (controllate a nov 2026): support.spotify.com (cover-art-requirements, audio-file-formats,
# loudness-normalization), support.distrokid.com (formati audio), support.cdbaby.com (artwork, audio),
# support.amuse.io, support.tunecore.com. Ricontrollale se cambiano.
import html, json, os

SITO = "https://streampack.pages.dev"
ROOT = os.path.join(os.path.dirname(__file__), "..")
LINGUE = ["en", "it", "es", "de", "fr", "pt"]
SLUG = {
    "size":   {"en": "album-cover-size", "it": "it/dimensioni-copertina-album", "es": "es/tamano-portada-album", "de": "de/albumcover-groesse", "fr": "fr/taille-pochette-album", "pt": "pt/tamanho-capa-album"},
    "reject": {"en": "cover-art-rejected", "it": "it/copertina-rifiutata", "es": "es/portada-rechazada", "de": "de/cover-abgelehnt", "fr": "fr/pochette-refusee", "pt": "pt/capa-rejeitada"},
    "audio":  {"en": "audio-format-for-distrokid", "it": "it/formato-audio-distrokid", "es": "es/formato-audio-distrokid", "de": "de/audioformat-distrokid", "fr": "fr/format-audio-distrokid", "pt": "pt/formato-audio-distrokid"},
    "lufs":   {"en": "spotify-lufs", "it": "it/lufs-spotify", "es": "es/lufs-spotify", "de": "de/lufs-spotify", "fr": "fr/lufs-spotify", "pt": "pt/lufs-spotify"},
}
APRI = {"size": "go=cover", "reject": "go=cover", "audio": "to=wav", "lufs": "go=audio&lufs=1"}

# Strumenti gratuiti (pagine generate da seo/checkers.py), linkati da ogni guida: slug e nome breve per lingua
CHECK = {
 "lufs": {"en": ("lufs-checker", "LUFS checker"), "it": ("it/misura-lufs", "Misura LUFS"), "es": ("es/medidor-lufs", "Medidor de LUFS"), "de": ("de/lufs-messen", "LUFS messen"), "fr": ("fr/mesurer-lufs", "Mesurer les LUFS"), "pt": ("pt/medidor-lufs", "Medidor de LUFS")},
 "isrc": {"en": ("isrc-checker", "ISRC checker"), "it": ("it/verifica-isrc", "Verifica ISRC"), "es": ("es/verificar-isrc", "Verificar ISRC"), "de": ("de/isrc-pruefen", "ISRC prüfen"), "fr": ("fr/verifier-isrc", "Vérifier un ISRC"), "pt": ("pt/verificar-isrc", "Verificar ISRC")},
}

C = {  # testi comuni
 "en": {"free": "Free · no sign-up · no ads · files stay on your device", "other": "More guides", "conv": "All audio converters", "foot": "StreamPack is not affiliated with Spotify, Apple, DistroKid or the other services named.", "check": "Requirements change: check your distributor's help page before releasing."},
 "it": {"free": "Gratis · senza registrazione · senza pubblicità · i file restano sul tuo dispositivo", "other": "Altre guide", "conv": "Tutti i convertitori audio", "foot": "StreamPack non è affiliata a Spotify, Apple, DistroKid né agli altri servizi citati.", "check": "I requisiti possono cambiare: controlla la pagina di aiuto del tuo distributore prima di pubblicare."},
 "es": {"free": "Gratis · sin registro · sin anuncios · los archivos no salen de tu dispositivo", "other": "Más guías", "conv": "Todos los conversores de audio", "foot": "StreamPack no está afiliada a Spotify, Apple, DistroKid ni a los demás servicios citados.", "check": "Los requisitos cambian: revisa la página de ayuda de tu distribuidora antes de publicar."},
 "de": {"free": "Kostenlos · ohne Anmeldung · ohne Werbung · die Dateien bleiben auf deinem Gerät", "other": "Weitere Ratgeber", "conv": "Alle Audio-Konverter", "foot": "StreamPack ist nicht mit Spotify, Apple, DistroKid oder den anderen genannten Diensten verbunden.", "check": "Anforderungen ändern sich: Prüf vor dem Release die Hilfeseite deines Vertriebs."},
 "fr": {"free": "Gratuit · sans inscription · sans pub · vos fichiers restent sur votre appareil", "other": "Autres guides", "conv": "Tous les convertisseurs audio", "foot": "StreamPack n'est pas affiliée à Spotify, Apple, DistroKid ni aux autres services cités.", "check": "Les exigences évoluent : vérifiez la page d'aide de votre distributeur avant de publier."},
 "pt": {"free": "Grátis · sem cadastro · sem anúncios · os arquivos ficam no seu aparelho", "other": "Mais guias", "conv": "Todos os conversores de áudio", "foot": "O StreamPack não é afiliado ao Spotify, à Apple, à DistroKid nem aos outros serviços citados.", "check": "Os requisitos mudam: confira a página de ajuda da sua distribuidora antes de lançar."},
}

# Ogni guida: title, desc, h1, lead, cta, table (intestazioni, righe), blocks [(h2, [paragrafi] o ("ul", [voci]))], faq, nav (titolo breve)
G = {}

# ---------------- dimensioni copertina ----------------
G["size", "en"] = dict(nav="Album cover size",
 title="Album Cover Size for Spotify, Apple Music & DistroKid (3000×3000)",
 desc="The right album cover size is 3000×3000 px, square, RGB JPG under 10 MB: it works on Spotify, Apple Music, DistroKid, CD Baby and the rest. Resize yours free in one tap.",
 h1="Album cover size for Spotify, Apple Music and DistroKid",
 lead="Use a square 3000×3000 px image, RGB colour, JPG under 10 MB. That one file is accepted by every major platform and distributor. StreamPack crops and resizes your image to exactly that.",
 cta="Make my cover 3000×3000 →",
 table=(["Platform", "Size", "Format"], [
  ["Spotify", "square, 640–10,000 px, highest resolution available", "JPG, PNG or TIFF"],
  ["Apple Music", "at least 3000×3000 px", "JPG or PNG, RGB"],
  ["DistroKid", "square, 3000×3000 px recommended", "JPG or PNG, RGB"],
  ["CD Baby", "1400–3000 px, square", "JPG, PNG or GIF, RGB, under 25 MB"],
  ["Amazon Music, YouTube Music, TIDAL, Deezer", "they receive the cover from your distributor", "follow your distributor's spec"],
 ]),
 blocks=[
  ("Why 3000×3000 is the safe choice", ["The same cover is shown as a tiny thumbnail on a phone and full screen on a TV. A 3000×3000 file looks sharp everywhere and meets the strictest requirement (Apple Music), so you never have to export different sizes."]),
  ("Pixels matter, not DPI", ["For streaming, only the pixel size counts. A 3000×3000 image at 72 or 300 DPI is the same file for Spotify. If a distributor asks for DPI, 72–300 is fine."]),
  ("Don't send the cover through WhatsApp", ["WhatsApp, Telegram and similar apps compress and shrink images, so your 3000×3000 cover arrives smaller and blurry. Move it as a file: email, Google Drive or a USB cable."]),
 ],
 faq=[
  ("What size is Spotify cover art?", "Spotify accepts square images from 640 to 10,000 px and asks for the highest resolution available. In practice, 3000×3000 px is the standard that every distributor accepts."),
  ("My image is smaller than 3000 px. Can I use it?", "StreamPack upscales it to 3000×3000 and warns you if it may look blurry. Apple Music can reject covers that look low quality, so start from the largest image you have."),
  ("JPG or PNG?", "Both are accepted. JPG keeps the file well under 10 MB, which avoids upload errors."),
 ])
G["size", "it"] = dict(nav="Dimensioni copertina",
 title="Dimensioni copertina album per Spotify, Apple Music e DistroKid (3000×3000)",
 desc="La dimensione giusta della copertina è 3000×3000 px, quadrata, JPG RGB sotto i 10 MB: va bene per Spotify, Apple Music, DistroKid, CD Baby e gli altri. Ridimensionala gratis con un tocco.",
 h1="Dimensioni della copertina per Spotify, Apple Music e DistroKid",
 lead="Usa un'immagine quadrata da 3000×3000 px, colori RGB, JPG sotto i 10 MB. Questo file è accettato da tutte le piattaforme e i distributori principali. StreamPack ritaglia e ridimensiona la tua immagine esattamente così.",
 cta="Porta la copertina a 3000×3000 →",
 table=(["Piattaforma", "Dimensioni", "Formato"], [
  ["Spotify", "quadrata, da 640 a 10.000 px, la massima risoluzione disponibile", "JPG, PNG o TIFF"],
  ["Apple Music", "almeno 3000×3000 px", "JPG o PNG, RGB"],
  ["DistroKid", "quadrata, consigliata 3000×3000 px", "JPG o PNG, RGB"],
  ["CD Baby", "da 1400 a 3000 px, quadrata", "JPG, PNG o GIF, RGB, sotto i 25 MB"],
  ["Amazon Music, YouTube Music, TIDAL, Deezer", "ricevono la copertina dal tuo distributore", "segui le regole del distributore"],
 ]),
 blocks=[
  ("Perché 3000×3000 è la scelta sicura", ["La stessa copertina appare come miniatura sul telefono e a tutto schermo sulla TV. Un file da 3000×3000 è nitido ovunque e rispetta il requisito più severo (Apple Music), così non devi esportare misure diverse."]),
  ("Contano i pixel, non i DPI", ["Per lo streaming conta solo la dimensione in pixel. Un'immagine 3000×3000 a 72 o a 300 DPI per Spotify è lo stesso file. Se un distributore chiede i DPI, tra 72 e 300 va bene."]),
  ("Non mandare la copertina su WhatsApp", ["WhatsApp, Telegram e app simili comprimono e rimpiccioliscono le immagini: la copertina da 3000×3000 arriva più piccola e sfocata. Spostala come file: email, Google Drive o cavo USB."]),
 ],
 faq=[
  ("Che dimensioni deve avere la copertina su Spotify?", "Spotify accetta immagini quadrate da 640 a 10.000 px e chiede la massima risoluzione disponibile. In pratica 3000×3000 px è lo standard che tutti i distributori accettano."),
  ("La mia immagine è più piccola di 3000 px. Va bene?", "StreamPack la ingrandisce a 3000×3000 e ti avvisa se rischia di sembrare sfocata. Apple Music può rifiutare copertine di bassa qualità: parti dall'immagine più grande che hai."),
  ("Meglio JPG o PNG?", "Sono accettati entrambi. Il JPG tiene il file ben sotto i 10 MB ed evita errori di caricamento."),
 ])
G["size", "es"] = dict(nav="Tamaño de portada",
 title="Tamaño de portada de álbum para Spotify, Apple Music y DistroKid (3000×3000)",
 desc="El tamaño correcto de portada es 3000×3000 px, cuadrada, JPG RGB de menos de 10 MB: sirve para Spotify, Apple Music, DistroKid, CD Baby y el resto. Ajústala gratis con un toque.",
 h1="Tamaño de portada para Spotify, Apple Music y DistroKid",
 lead="Usa una imagen cuadrada de 3000×3000 px, color RGB, JPG de menos de 10 MB. Ese archivo lo aceptan todas las plataformas y distribuidoras principales. StreamPack recorta y redimensiona tu imagen exactamente así.",
 cta="Dejar mi portada en 3000×3000 →",
 table=(["Plataforma", "Tamaño", "Formato"], [
  ["Spotify", "cuadrada, de 640 a 10.000 px, la máxima resolución disponible", "JPG, PNG o TIFF"],
  ["Apple Music", "mínimo 3000×3000 px", "JPG o PNG, RGB"],
  ["DistroKid", "cuadrada, se recomienda 3000×3000 px", "JPG o PNG, RGB"],
  ["CD Baby", "de 1400 a 3000 px, cuadrada", "JPG, PNG o GIF, RGB, menos de 25 MB"],
  ["Amazon Music, YouTube Music, TIDAL, Deezer", "reciben la portada de tu distribuidora", "sigue las reglas de tu distribuidora"],
 ]),
 blocks=[
  ("Por qué 3000×3000 es la opción segura", ["La misma portada se ve como miniatura en el móvil y a pantalla completa en la tele. Un archivo de 3000×3000 se ve nítido en todas partes y cumple el requisito más exigente (Apple Music), así no tienes que exportar varios tamaños."]),
  ("Importan los píxeles, no los DPI", ["Para el streaming solo cuenta el tamaño en píxeles. Una imagen de 3000×3000 a 72 o a 300 DPI es el mismo archivo para Spotify. Si una distribuidora pide DPI, entre 72 y 300 está bien."]),
  ("No envíes la portada por WhatsApp", ["WhatsApp, Telegram y apps parecidas comprimen y reducen las imágenes: tu portada de 3000×3000 llega más pequeña y borrosa. Pásala como archivo: correo, Google Drive o cable USB."]),
 ],
 faq=[
  ("¿Qué tamaño tiene la portada en Spotify?", "Spotify acepta imágenes cuadradas de 640 a 10.000 px y pide la máxima resolución disponible. En la práctica, 3000×3000 px es el estándar que aceptan todas las distribuidoras."),
  ("Mi imagen mide menos de 3000 px. ¿Sirve?", "StreamPack la amplía a 3000×3000 y te avisa si puede verse borrosa. Apple Music puede rechazar portadas de baja calidad, así que parte de la imagen más grande que tengas."),
  ("¿JPG o PNG?", "Se aceptan los dos. El JPG deja el archivo muy por debajo de 10 MB y evita errores al subirlo."),
 ])
G["size", "de"] = dict(nav="Albumcover-Größe",
 title="Albumcover Größe für Spotify, Apple Music & DistroKid (3000×3000)",
 desc="Die richtige Cover-Größe ist 3000×3000 px, quadratisch, RGB-JPG unter 10 MB: passt für Spotify, Apple Music, DistroKid, CD Baby und alle anderen. Kostenlos mit einem Tippen anpassen.",
 h1="Albumcover-Größe für Spotify, Apple Music und DistroKid",
 lead="Nimm ein quadratisches Bild mit 3000×3000 px, RGB-Farben, JPG unter 10 MB. Diese Datei akzeptieren alle großen Plattformen und Vertriebe. StreamPack schneidet dein Bild genau so zu und skaliert es.",
 cta="Mein Cover auf 3000×3000 bringen →",
 table=(["Plattform", "Größe", "Format"], [
  ["Spotify", "quadratisch, 640–10.000 px, höchste verfügbare Auflösung", "JPG, PNG oder TIFF"],
  ["Apple Music", "mindestens 3000×3000 px", "JPG oder PNG, RGB"],
  ["DistroKid", "quadratisch, 3000×3000 px empfohlen", "JPG oder PNG, RGB"],
  ["CD Baby", "1400–3000 px, quadratisch", "JPG, PNG oder GIF, RGB, unter 25 MB"],
  ["Amazon Music, YouTube Music, TIDAL, Deezer", "bekommen das Cover von deinem Vertrieb", "Vorgaben deines Vertriebs beachten"],
 ]),
 blocks=[
  ("Warum 3000×3000 die sichere Wahl ist", ["Dasselbe Cover erscheint als kleines Vorschaubild auf dem Handy und im Vollbild auf dem Fernseher. Eine 3000×3000-Datei ist überall scharf und erfüllt die strengste Vorgabe (Apple Music) – du musst keine verschiedenen Größen exportieren."]),
  ("Es zählen Pixel, nicht DPI", ["Fürs Streaming zählt nur die Größe in Pixeln. Ein 3000×3000-Bild mit 72 oder 300 DPI ist für Spotify dieselbe Datei. Fragt ein Vertrieb nach DPI, passen 72 bis 300."]),
  ("Schick das Cover nicht über WhatsApp", ["WhatsApp, Telegram und ähnliche Apps komprimieren und verkleinern Bilder: Dein 3000×3000-Cover kommt kleiner und unscharf an. Übertrag es als Datei: per E-Mail, Google Drive oder USB-Kabel."]),
 ],
 faq=[
  ("Welche Größe hat das Spotify-Cover?", "Spotify akzeptiert quadratische Bilder von 640 bis 10.000 px und verlangt die höchste verfügbare Auflösung. In der Praxis ist 3000×3000 px der Standard, den alle Vertriebe annehmen."),
  ("Mein Bild ist kleiner als 3000 px. Geht das?", "StreamPack vergrößert es auf 3000×3000 und warnt dich, wenn es unscharf wirken kann. Apple Music kann Cover mit schlechter Qualität ablehnen, nimm also das größte Bild, das du hast."),
  ("JPG oder PNG?", "Beides wird akzeptiert. Mit JPG bleibt die Datei deutlich unter 10 MB, das vermeidet Upload-Fehler."),
 ])
G["size", "fr"] = dict(nav="Taille de pochette",
 title="Taille de pochette d'album pour Spotify, Apple Music et DistroKid (3000×3000)",
 desc="La bonne taille de pochette est 3000×3000 px, carrée, JPG RVB de moins de 10 Mo : elle convient à Spotify, Apple Music, DistroKid, CD Baby et aux autres. Redimensionnez la vôtre gratuitement en un geste.",
 h1="Taille de pochette pour Spotify, Apple Music et DistroKid",
 lead="Utilisez une image carrée de 3000×3000 px, couleurs RVB, JPG de moins de 10 Mo. Ce fichier est accepté par toutes les grandes plateformes et tous les distributeurs. StreamPack recadre et redimensionne votre image exactement ainsi.",
 cta="Passer ma pochette en 3000×3000 →",
 table=(["Plateforme", "Taille", "Format"], [
  ["Spotify", "carrée, de 640 à 10 000 px, la plus haute résolution disponible", "JPG, PNG ou TIFF"],
  ["Apple Music", "au moins 3000×3000 px", "JPG ou PNG, RVB"],
  ["DistroKid", "carrée, 3000×3000 px recommandé", "JPG ou PNG, RVB"],
  ["CD Baby", "de 1400 à 3000 px, carrée", "JPG, PNG ou GIF, RVB, moins de 25 Mo"],
  ["Amazon Music, YouTube Music, TIDAL, Deezer", "reçoivent la pochette de votre distributeur", "suivez les règles de votre distributeur"],
 ]),
 blocks=[
  ("Pourquoi 3000×3000 est le choix sûr", ["La même pochette s'affiche en vignette sur un téléphone et en plein écran sur une télé. Un fichier en 3000×3000 reste net partout et respecte l'exigence la plus stricte (Apple Music) : pas besoin d'exporter plusieurs tailles."]),
  ("Ce sont les pixels qui comptent, pas les DPI", ["Pour le streaming, seule la taille en pixels compte. Une image 3000×3000 à 72 ou à 300 DPI est le même fichier pour Spotify. Si un distributeur demande des DPI, entre 72 et 300 c'est bon."]),
  ("N'envoyez pas la pochette par WhatsApp", ["WhatsApp, Telegram et les applis similaires compressent et réduisent les images : votre pochette 3000×3000 arrive plus petite et floue. Transférez-la comme fichier : e-mail, Google Drive ou câble USB."]),
 ],
 faq=[
  ("Quelle taille pour une pochette Spotify ?", "Spotify accepte les images carrées de 640 à 10 000 px et demande la plus haute résolution disponible. En pratique, 3000×3000 px est le standard accepté par tous les distributeurs."),
  ("Mon image fait moins de 3000 px. Ça marche ?", "StreamPack l'agrandit en 3000×3000 et vous prévient si elle risque d'être floue. Apple Music peut refuser une pochette de mauvaise qualité : partez de la plus grande image que vous avez."),
  ("JPG ou PNG ?", "Les deux sont acceptés. Le JPG garde le fichier bien sous les 10 Mo, ce qui évite les erreurs d'envoi."),
 ])
G["size", "pt"] = dict(nav="Tamanho da capa",
 title="Tamanho da capa do álbum para Spotify, Apple Music e DistroKid (3000×3000)",
 desc="O tamanho certo da capa é 3000×3000 px, quadrada, JPG RGB com menos de 10 MB: serve para Spotify, Apple Music, DistroKid, CD Baby e os outros. Ajuste a sua de graça com um toque.",
 h1="Tamanho da capa para Spotify, Apple Music e DistroKid",
 lead="Use uma imagem quadrada de 3000×3000 px, cores RGB, JPG com menos de 10 MB. Esse arquivo é aceito por todas as grandes plataformas e distribuidoras. O StreamPack corta e redimensiona sua imagem exatamente assim.",
 cta="Deixar minha capa em 3000×3000 →",
 table=(["Plataforma", "Tamanho", "Formato"], [
  ["Spotify", "quadrada, de 640 a 10.000 px, a maior resolução disponível", "JPG, PNG ou TIFF"],
  ["Apple Music", "no mínimo 3000×3000 px", "JPG ou PNG, RGB"],
  ["DistroKid", "quadrada, 3000×3000 px recomendado", "JPG ou PNG, RGB"],
  ["CD Baby", "de 1400 a 3000 px, quadrada", "JPG, PNG ou GIF, RGB, menos de 25 MB"],
  ["Amazon Music, YouTube Music, TIDAL, Deezer", "recebem a capa da sua distribuidora", "siga as regras da sua distribuidora"],
 ]),
 blocks=[
  ("Por que 3000×3000 é a escolha segura", ["A mesma capa aparece como miniatura no celular e em tela cheia na TV. Um arquivo de 3000×3000 fica nítido em todo lugar e cumpre a exigência mais rígida (Apple Music), então você não precisa exportar vários tamanhos."]),
  ("O que conta são os pixels, não o DPI", ["Para streaming, só conta o tamanho em pixels. Uma imagem 3000×3000 a 72 ou a 300 DPI é o mesmo arquivo para o Spotify. Se a distribuidora pedir DPI, entre 72 e 300 está ótimo."]),
  ("Não mande a capa pelo WhatsApp", ["WhatsApp, Telegram e apps parecidos comprimem e reduzem as imagens: sua capa de 3000×3000 chega menor e borrada. Envie como arquivo: e-mail, Google Drive ou cabo USB."]),
 ],
 faq=[
  ("Qual o tamanho da capa no Spotify?", "O Spotify aceita imagens quadradas de 640 a 10.000 px e pede a maior resolução disponível. Na prática, 3000×3000 px é o padrão que todas as distribuidoras aceitam."),
  ("Minha imagem tem menos de 3000 px. Serve?", "O StreamPack amplia para 3000×3000 e avisa se ela pode ficar borrada. A Apple Music pode recusar capas de baixa qualidade, então comece pela maior imagem que você tiver."),
  ("JPG ou PNG?", "Os dois são aceitos. O JPG deixa o arquivo bem abaixo de 10 MB e evita erros no envio."),
 ])

# ---------------- copertina rifiutata ----------------
def rej(nav, title, desc, h1, lead, cta, h_check, check, h_fix, fix, faq):
    return dict(nav=nav, title=title, desc=desc, h1=h1, lead=lead, cta=cta, table=None,
                blocks=[(h_check, ("ul", check)), (h_fix, [fix])], faq=faq)
G["reject", "en"] = rej("Cover art rejected",
 "Cover Art Rejected? DistroKid & Spotify Artwork Requirements (Checklist)",
 "Why distributors reject cover art and how to fix it: size, square crop, RGB, text that doesn't match, links, logos. Checklist for DistroKid, Spotify, Apple Music, CD Baby.",
 "Cover art rejected? The checklist that gets it approved",
 "Most rejections come from a few technical problems and a few content rules. Check the list below, then fix the technical part in one tap with StreamPack.",
 "Fix my cover now →",
 "Checklist before you upload",
 ["Square (1:1) image: no rectangles, no white borders added to fake a square",
  "3000×3000 px, JPG or PNG, under 10 MB",
  "RGB colour, not CMYK (print files are often CMYK)",
  "Any text must match the release: artist name and title exactly as in your metadata",
  "No website URLs, @handles or social media logos",
  "No prices, \"new\", \"exclusive\" or store logos (Spotify, Apple, Amazon…)",
  "No images you don't have the rights to",
  "Not blurry or pixelated: don't upscale a tiny image"],
 "What StreamPack fixes for you",
 "StreamPack crops the image square, converts it to RGB, resizes it to 3000×3000 and saves a JPG under 10 MB. It also reminds you of the content rules before you upload. The design itself (text, logos, rights) is up to you.",
 [("Why was my cover art rejected by DistroKid?", "The most common reasons are a size or format problem (not square, too small, CMYK), text that doesn't match the artist name or title, and forbidden elements such as URLs, @handles or store logos."),
  ("Can I use an AI-generated cover?", "Many distributors accept original AI-generated artwork as long as you have the right to use it. Check your distributor's current rules before releasing."),
  ("How long does it take after I fix it?", "It depends on your distributor: you upload the corrected cover and the release goes back into review.")])
G["reject", "it"] = rej("Copertina rifiutata",
 "Copertina rifiutata? Requisiti copertina DistroKid e Spotify (checklist)",
 "Perché i distributori rifiutano la copertina e come sistemarla: dimensioni, formato quadrato, RGB, testi che non corrispondono, link, loghi. Checklist per DistroKid, Spotify, Apple Music, CD Baby.",
 "Copertina rifiutata? La checklist per farla approvare",
 "Quasi tutti i rifiuti nascono da pochi problemi tecnici e da poche regole sui contenuti. Controlla l'elenco qui sotto, poi sistema la parte tecnica con un tocco su StreamPack.",
 "Sistema la copertina ora →",
 "Checklist prima di caricarla",
 ["Immagine quadrata (1:1): niente rettangoli né bordi bianchi aggiunti per farla sembrare quadrata",
  "3000×3000 px, JPG o PNG, sotto i 10 MB",
  "Colori RGB, non CMYK (i file per la stampa spesso sono CMYK)",
  "Ogni testo deve corrispondere alla release: nome artista e titolo identici ai metadati",
  "Niente indirizzi web, @nomi utente o loghi dei social",
  "Niente prezzi, \"novità\", \"esclusiva\" o loghi dei negozi (Spotify, Apple, Amazon…)",
  "Niente immagini di cui non hai i diritti",
  "Non sfocata o sgranata: non ingrandire un'immagine minuscola"],
 "Cosa sistema StreamPack per te",
 "StreamPack ritaglia l'immagine quadrata, la converte in RGB, la porta a 3000×3000 e salva un JPG sotto i 10 MB. Ti ricorda anche le regole sui contenuti prima del caricamento. La grafica (testi, loghi, diritti) resta a te.",
 [("Perché DistroKid ha rifiutato la mia copertina?", "I motivi più comuni sono un problema di dimensioni o formato (non quadrata, troppo piccola, CMYK), testi che non corrispondono a nome artista o titolo ed elementi vietati come link, @nomi utente o loghi dei negozi."),
  ("Posso usare una copertina creata con l'AI?", "Molti distributori accettano copertine originali generate con l'AI, purché tu abbia il diritto di usarle. Controlla le regole attuali del tuo distributore prima di pubblicare."),
  ("Quanto ci vuole dopo averla corretta?", "Dipende dal distributore: carichi la copertina corretta e la release torna in revisione.")])
G["reject", "es"] = rej("Portada rechazada",
 "¿Portada rechazada? Requisitos de portada en DistroKid y Spotify (checklist)",
 "Por qué las distribuidoras rechazan la portada y cómo arreglarla: tamaño, formato cuadrado, RGB, textos que no coinciden, enlaces, logos. Checklist para DistroKid, Spotify, Apple Music, CD Baby.",
 "¿Portada rechazada? La checklist para que te la aprueben",
 "Casi todos los rechazos vienen de unos pocos problemas técnicos y unas pocas reglas de contenido. Revisa la lista y arregla la parte técnica con un toque en StreamPack.",
 "Arreglar mi portada ahora →",
 "Checklist antes de subirla",
 ["Imagen cuadrada (1:1): sin rectángulos ni bordes blancos añadidos para que parezca cuadrada",
  "3000×3000 px, JPG o PNG, menos de 10 MB",
  "Color RGB, no CMYK (los archivos para imprenta suelen ser CMYK)",
  "Todo texto debe coincidir con el lanzamiento: nombre artístico y título iguales a los metadatos",
  "Sin direcciones web, @usuarios ni logos de redes sociales",
  "Sin precios, \"nuevo\", \"exclusivo\" ni logos de tiendas (Spotify, Apple, Amazon…)",
  "Sin imágenes de las que no tengas los derechos",
  "Ni borrosa ni pixelada: no amplíes una imagen diminuta"],
 "Lo que StreamPack arregla por ti",
 "StreamPack recorta la imagen en cuadrado, la pasa a RGB, la deja en 3000×3000 y guarda un JPG de menos de 10 MB. También te recuerda las reglas de contenido antes de subirla. El diseño (textos, logos, derechos) depende de ti.",
 [("¿Por qué DistroKid rechazó mi portada?", "Los motivos más comunes son un problema de tamaño o formato (no cuadrada, demasiado pequeña, CMYK), textos que no coinciden con el nombre artístico o el título y elementos prohibidos como enlaces, @usuarios o logos de tiendas."),
  ("¿Puedo usar una portada hecha con IA?", "Muchas distribuidoras aceptan portadas originales generadas con IA si tienes derecho a usarlas. Revisa las reglas actuales de tu distribuidora antes de publicar."),
  ("¿Cuánto tarda después de corregirla?", "Depende de la distribuidora: subes la portada corregida y el lanzamiento vuelve a revisión.")])
G["reject", "de"] = rej("Cover abgelehnt",
 "Cover abgelehnt? Cover-Anforderungen von DistroKid & Spotify (Checkliste)",
 "Warum Vertriebe Cover ablehnen und wie du es behebst: Größe, quadratisch, RGB, Text passt nicht, Links, Logos. Checkliste für DistroKid, Spotify, Apple Music, CD Baby.",
 "Cover abgelehnt? Die Checkliste für die Freigabe",
 "Fast alle Ablehnungen haben ein paar technische Ursachen und ein paar inhaltliche Regeln. Geh die Liste durch und behebe den technischen Teil mit einem Tippen in StreamPack.",
 "Mein Cover jetzt korrigieren →",
 "Checkliste vor dem Upload",
 ["Quadratisches Bild (1:1): keine Rechtecke, keine weißen Ränder, die ein Quadrat vortäuschen",
  "3000×3000 px, JPG oder PNG, unter 10 MB",
  "RGB-Farben, kein CMYK (Druckdateien sind oft CMYK)",
  "Jeder Text muss zum Release passen: Künstlername und Titel genau wie in den Metadaten",
  "Keine Webadressen, @Namen oder Social-Media-Logos",
  "Keine Preise, „Neu“, „Exklusiv“ oder Shop-Logos (Spotify, Apple, Amazon…)",
  "Keine Bilder, an denen du keine Rechte hast",
  "Nicht unscharf oder verpixelt: kein winziges Bild hochskalieren"],
 "Was StreamPack für dich erledigt",
 "StreamPack schneidet das Bild quadratisch zu, wandelt es in RGB um, bringt es auf 3000×3000 und speichert ein JPG unter 10 MB. Vor dem Upload erinnert es dich auch an die inhaltlichen Regeln. Die Gestaltung (Text, Logos, Rechte) liegt bei dir.",
 [("Warum hat DistroKid mein Cover abgelehnt?", "Die häufigsten Gründe sind ein Größen- oder Formatproblem (nicht quadratisch, zu klein, CMYK), Text, der nicht zu Künstlername oder Titel passt, und verbotene Elemente wie Links, @Namen oder Shop-Logos."),
  ("Darf ich ein KI-generiertes Cover nutzen?", "Viele Vertriebe akzeptieren originale KI-Cover, solange du die Rechte daran hast. Prüf vor dem Release die aktuellen Regeln deines Vertriebs."),
  ("Wie lange dauert es nach der Korrektur?", "Das hängt vom Vertrieb ab: Du lädst das korrigierte Cover hoch und das Release geht wieder in die Prüfung.")])
G["reject", "fr"] = rej("Pochette refusée",
 "Pochette refusée ? Exigences de DistroKid et Spotify pour la pochette (checklist)",
 "Pourquoi les distributeurs refusent une pochette et comment la corriger : taille, format carré, RVB, texte qui ne correspond pas, liens, logos. Checklist pour DistroKid, Spotify, Apple Music, CD Baby.",
 "Pochette refusée ? La checklist pour la faire accepter",
 "Presque tous les refus viennent de quelques problèmes techniques et de quelques règles de contenu. Vérifiez la liste, puis corrigez la partie technique en un geste avec StreamPack.",
 "Corriger ma pochette →",
 "Checklist avant l'envoi",
 ["Image carrée (1:1) : pas de rectangle ni de bords blancs ajoutés pour faire carré",
  "3000×3000 px, JPG ou PNG, moins de 10 Mo",
  "Couleurs RVB, pas CMJN (les fichiers pour l'impression sont souvent en CMJN)",
  "Tout texte doit correspondre à la sortie : nom d'artiste et titre identiques aux métadonnées",
  "Pas d'adresse web, de @pseudo ni de logo de réseau social",
  "Pas de prix, de « nouveau », d'« exclusif » ni de logo de plateforme (Spotify, Apple, Amazon…)",
  "Pas d'image dont vous n'avez pas les droits",
  "Ni floue ni pixelisée : n'agrandissez pas une image minuscule"],
 "Ce que StreamPack corrige pour vous",
 "StreamPack recadre l'image en carré, la passe en RVB, la met en 3000×3000 et enregistre un JPG de moins de 10 Mo. Il vous rappelle aussi les règles de contenu avant l'envoi. Le visuel (textes, logos, droits) reste à votre charge.",
 [("Pourquoi DistroKid a refusé ma pochette ?", "Les raisons les plus fréquentes : un problème de taille ou de format (pas carrée, trop petite, CMJN), un texte qui ne correspond pas au nom d'artiste ou au titre, et des éléments interdits comme des liens, des @pseudos ou des logos de plateformes."),
  ("Puis-je utiliser une pochette créée avec l'IA ?", "Beaucoup de distributeurs acceptent les visuels originaux générés par IA si vous avez le droit de les utiliser. Vérifiez les règles actuelles de votre distributeur avant de publier."),
  ("Combien de temps après la correction ?", "Cela dépend du distributeur : vous envoyez la pochette corrigée et la sortie repart en validation.")])
G["reject", "pt"] = rej("Capa rejeitada",
 "Capa rejeitada? Requisitos de capa da DistroKid e do Spotify (checklist)",
 "Por que as distribuidoras rejeitam a capa e como corrigir: tamanho, formato quadrado, RGB, texto que não bate, links, logos. Checklist para DistroKid, Spotify, Apple Music, CD Baby.",
 "Capa rejeitada? O checklist para ser aprovada",
 "Quase todas as rejeições vêm de poucos problemas técnicos e poucas regras de conteúdo. Confira a lista e corrija a parte técnica com um toque no StreamPack.",
 "Corrigir minha capa agora →",
 "Checklist antes de enviar",
 ["Imagem quadrada (1:1): nada de retângulos nem bordas brancas para parecer quadrada",
  "3000×3000 px, JPG ou PNG, menos de 10 MB",
  "Cores RGB, não CMYK (arquivos para impressão costumam ser CMYK)",
  "Todo texto precisa bater com o lançamento: nome artístico e título iguais aos metadados",
  "Sem endereços de sites, @usuários ou logos de redes sociais",
  "Sem preços, \"novo\", \"exclusivo\" ou logos de lojas (Spotify, Apple, Amazon…)",
  "Sem imagens sobre as quais você não tem direitos",
  "Nada borrado ou pixelado: não amplie uma imagem minúscula"],
 "O que o StreamPack corrige para você",
 "O StreamPack corta a imagem em quadrado, converte para RGB, deixa em 3000×3000 e salva um JPG com menos de 10 MB. Também lembra as regras de conteúdo antes do envio. O design (textos, logos, direitos) fica com você.",
 [("Por que a DistroKid rejeitou minha capa?", "Os motivos mais comuns são problema de tamanho ou formato (não quadrada, pequena demais, CMYK), texto que não bate com o nome artístico ou o título e elementos proibidos como links, @usuários ou logos de lojas."),
  ("Posso usar uma capa feita com IA?", "Muitas distribuidoras aceitam capas originais geradas por IA, desde que você tenha o direito de usá-las. Confira as regras atuais da sua distribuidora antes de lançar."),
  ("Quanto tempo leva depois de corrigir?", "Depende da distribuidora: você envia a capa corrigida e o lançamento volta para análise.")])

# ---------------- formato audio ----------------
def aud(nav, title, desc, h1, lead, cta, hdr, rows, blocks, faq):
    return dict(nav=nav, title=title, desc=desc, h1=h1, lead=lead, cta=cta, table=(hdr, rows), blocks=blocks, faq=faq)
G["audio", "en"] = aud("Audio format for DistroKid",
 "Audio Format for DistroKid & Spotify: WAV or FLAC, 16-bit 44.1 kHz",
 "Which audio file to upload to DistroKid, CD Baby, TuneCore or Amuse for Spotify and Apple Music: stereo WAV or FLAC, 44.1 kHz. Convert MP4, M4A, OGG or 48 kHz files free.",
 "Audio format for DistroKid and Spotify",
 "The file every distributor accepts is a stereo WAV or FLAC at 44.1 kHz, 16-bit. If your track is an M4A, MP4, OGG, a phone recording or a 48 kHz file, StreamPack converts it to exactly that.",
 "Convert my track to WAV 44.1 kHz →",
 ["Distributor", "What it accepts"],
 [["DistroKid", "WAV, MP3, M4A, FLAC, AIFF or WMA; 16-bit 44.1 kHz WAV is typical; up to 1 GB"],
  ["Spotify (via your distributor)", "FLAC preferred, WAV accepted; 44.1 kHz or higher; stereo; 24-bit if that is your master"],
  ["CD Baby", "WAV or FLAC (MP3 accepted, not recommended); stereo, 44.1 kHz, 16-bit"],
  ["TuneCore", "WAV; 24-bit recommended, 16-bit 44.1 kHz accepted"],
  ["Amuse", "WAV, stereo, 44.1 kHz, 16-bit (no 24-bit)"]],
 [("When you need StreamPack and when you don't", ["If your DAW already exported a WAV or FLAC master that your distributor accepts, upload it as it is: Spotify asks for the native master and doesn't want it downsampled. StreamPack is for the other cases: the file is in a format the distributor refuses, it's 48 kHz or mono, or you're not sure. It gives you a stereo 44.1 kHz 16-bit WAV or FLAC that every distributor takes."]),
  ("File names", ["DistroKid refuses file names containing \\ / : * ? \" ' < > |. StreamPack names the files with your artist name and the title, without those characters."])],
 [("WAV or FLAC for DistroKid?", "Both are lossless, so the sound is identical. FLAC files are smaller, which helps with long tracks or albums."),
  ("Is MP3 enough?", "Some distributors accept MP3, but lossless WAV or FLAC is recommended: the platforms re-encode your file, and starting from MP3 loses more quality."),
  ("Should I upload 24-bit?", "If your master is 24-bit and your distributor accepts it, yes. Amuse only takes 16-bit; when in doubt, 16-bit 44.1 kHz is accepted everywhere.")])
G["audio", "it"] = aud("Formato audio per DistroKid",
 "Formato audio per DistroKid e Spotify: WAV o FLAC, 16 bit 44,1 kHz",
 "Che file audio caricare su DistroKid, CD Baby, TuneCore o Amuse per Spotify e Apple Music: WAV o FLAC stereo a 44,1 kHz. Converti gratis file MP4, M4A, OGG o a 48 kHz.",
 "Formato audio per DistroKid e Spotify",
 "Il file che tutti i distributori accettano è un WAV o FLAC stereo a 44,1 kHz, 16 bit. Se il tuo brano è un M4A, un MP4, un OGG, una registrazione del telefono o un file a 48 kHz, StreamPack lo converte esattamente così.",
 "Converti il brano in WAV 44,1 kHz →",
 ["Distributore", "Cosa accetta"],
 [["DistroKid", "WAV, MP3, M4A, FLAC, AIFF o WMA; tipico WAV 16 bit 44,1 kHz; fino a 1 GB"],
  ["Spotify (tramite distributore)", "preferisce FLAC, accetta WAV; 44,1 kHz o più; stereo; 24 bit se il master è a 24 bit"],
  ["CD Baby", "WAV o FLAC (MP3 accettato ma sconsigliato); stereo, 44,1 kHz, 16 bit"],
  ["TuneCore", "WAV; consigliato 24 bit, accettato 16 bit 44,1 kHz"],
  ["Amuse", "WAV, stereo, 44,1 kHz, 16 bit (niente 24 bit)"]],
 [("Quando ti serve StreamPack e quando no", ["Se la tua DAW ha già esportato un master WAV o FLAC accettato dal distributore, caricalo così com'è: Spotify chiede il master originale e non vuole che venga abbassata la qualità. StreamPack serve negli altri casi: il file è in un formato che il distributore rifiuta, è a 48 kHz o mono, oppure non sei sicuro. Ti dà un WAV o FLAC stereo a 44,1 kHz e 16 bit che tutti i distributori accettano."]),
  ("Nomi dei file", ["DistroKid rifiuta i nomi di file che contengono \\ / : * ? \" ' < > |. StreamPack nomina i file con il nome artista e il titolo, senza quei caratteri."])],
 [("WAV o FLAC per DistroKid?", "Sono entrambi senza perdita, quindi il suono è identico. I FLAC sono più leggeri: comodo per brani lunghi o album."),
  ("Basta un MP3?", "Alcuni distributori accettano l'MP3, ma è consigliato un WAV o FLAC: le piattaforme ricodificano il file e partire da un MP3 fa perdere più qualità."),
  ("Devo caricare a 24 bit?", "Se il master è a 24 bit e il distributore lo accetta, sì. Amuse prende solo 16 bit; nel dubbio, 16 bit 44,1 kHz va bene ovunque.")])
G["audio", "es"] = aud("Formato de audio para DistroKid",
 "Formato de audio para DistroKid y Spotify: WAV o FLAC, 16 bits 44,1 kHz",
 "Qué archivo de audio subir a DistroKid, CD Baby, TuneCore o Amuse para Spotify y Apple Music: WAV o FLAC estéreo a 44,1 kHz. Convierte gratis archivos MP4, M4A, OGG o de 48 kHz.",
 "Formato de audio para DistroKid y Spotify",
 "El archivo que aceptan todas las distribuidoras es un WAV o FLAC estéreo a 44,1 kHz y 16 bits. Si tu tema es un M4A, un MP4, un OGG, una grabación del móvil o un archivo a 48 kHz, StreamPack lo convierte exactamente así.",
 "Convertir mi tema a WAV 44,1 kHz →",
 ["Distribuidora", "Qué acepta"],
 [["DistroKid", "WAV, MP3, M4A, FLAC, AIFF o WMA; lo típico es WAV 16 bits 44,1 kHz; hasta 1 GB"],
  ["Spotify (a través de tu distribuidora)", "prefiere FLAC, acepta WAV; 44,1 kHz o más; estéreo; 24 bits si ese es tu máster"],
  ["CD Baby", "WAV o FLAC (MP3 aceptado pero no recomendado); estéreo, 44,1 kHz, 16 bits"],
  ["TuneCore", "WAV; recomienda 24 bits, acepta 16 bits 44,1 kHz"],
  ["Amuse", "WAV, estéreo, 44,1 kHz, 16 bits (sin 24 bits)"]],
 [("Cuándo necesitas StreamPack y cuándo no", ["Si tu DAW ya exportó un máster WAV o FLAC que tu distribuidora acepta, súbelo tal cual: Spotify pide el máster original y no quiere que se reduzca la calidad. StreamPack es para los demás casos: el archivo está en un formato que la distribuidora rechaza, está a 48 kHz o en mono, o no estás seguro. Te da un WAV o FLAC estéreo a 44,1 kHz y 16 bits que aceptan todas."]),
  ("Nombres de archivo", ["DistroKid rechaza los nombres de archivo con \\ / : * ? \" ' < > |. StreamPack nombra los archivos con tu nombre artístico y el título, sin esos caracteres."])],
 [("¿WAV o FLAC para DistroKid?", "Los dos son sin pérdida, así que suenan igual. Los FLAC pesan menos: útil para temas largos o álbumes."),
  ("¿Vale un MP3?", "Algunas distribuidoras aceptan MP3, pero se recomienda WAV o FLAC: las plataformas vuelven a codificar el archivo y partir de un MP3 pierde más calidad."),
  ("¿Subo a 24 bits?", "Si tu máster es de 24 bits y tu distribuidora lo acepta, sí. Amuse solo acepta 16 bits; ante la duda, 16 bits 44,1 kHz vale en todas.")])
G["audio", "de"] = aud("Audioformat für DistroKid",
 "Audioformat für DistroKid & Spotify: WAV oder FLAC, 16 Bit 44,1 kHz",
 "Welche Audiodatei du bei DistroKid, CD Baby, TuneCore oder Amuse für Spotify und Apple Music hochlädst: Stereo-WAV oder -FLAC mit 44,1 kHz. MP4-, M4A-, OGG- oder 48-kHz-Dateien kostenlos umwandeln.",
 "Audioformat für DistroKid und Spotify",
 "Die Datei, die jeder Vertrieb annimmt, ist ein Stereo-WAV oder -FLAC mit 44,1 kHz und 16 Bit. Ist dein Song ein M4A, MP4, OGG, eine Handyaufnahme oder eine 48-kHz-Datei, wandelt StreamPack ihn genau so um.",
 "Song in WAV 44,1 kHz umwandeln →",
 ["Vertrieb", "Was er annimmt"],
 [["DistroKid", "WAV, MP3, M4A, FLAC, AIFF oder WMA; üblich ist WAV 16 Bit 44,1 kHz; bis 1 GB"],
  ["Spotify (über deinen Vertrieb)", "bevorzugt FLAC, nimmt WAV; 44,1 kHz oder mehr; Stereo; 24 Bit, wenn das dein Master ist"],
  ["CD Baby", "WAV oder FLAC (MP3 möglich, aber nicht empfohlen); Stereo, 44,1 kHz, 16 Bit"],
  ["TuneCore", "WAV; 24 Bit empfohlen, 16 Bit 44,1 kHz akzeptiert"],
  ["Amuse", "WAV, Stereo, 44,1 kHz, 16 Bit (kein 24 Bit)"]],
 [("Wann du StreamPack brauchst – und wann nicht", ["Hat deine DAW schon einen WAV- oder FLAC-Master exportiert, den dein Vertrieb annimmt, lad ihn so hoch: Spotify will den Original-Master und keine reduzierte Qualität. StreamPack ist für die anderen Fälle: Die Datei hat ein Format, das der Vertrieb ablehnt, sie ist 48 kHz oder mono, oder du bist unsicher. Du bekommst ein Stereo-WAV oder -FLAC mit 44,1 kHz und 16 Bit, das jeder Vertrieb nimmt."]),
  ("Dateinamen", ["DistroKid lehnt Dateinamen mit \\ / : * ? \" ' < > | ab. StreamPack benennt die Dateien mit Künstlername und Titel, ohne diese Zeichen."])],
 [("WAV oder FLAC für DistroKid?", "Beide sind verlustfrei, der Klang ist identisch. FLAC-Dateien sind kleiner – praktisch bei langen Songs oder Alben."),
  ("Reicht MP3?", "Manche Vertriebe nehmen MP3, empfohlen ist aber WAV oder FLAC: Die Plattformen kodieren die Datei neu, und von MP3 aus geht mehr Qualität verloren."),
  ("Soll ich 24 Bit hochladen?", "Wenn dein Master 24 Bit hat und dein Vertrieb es annimmt, ja. Amuse nimmt nur 16 Bit; im Zweifel geht 16 Bit 44,1 kHz überall.")])
G["audio", "fr"] = aud("Format audio pour DistroKid",
 "Format audio pour DistroKid et Spotify : WAV ou FLAC, 16 bits 44,1 kHz",
 "Quel fichier audio envoyer à DistroKid, CD Baby, TuneCore ou Amuse pour Spotify et Apple Music : WAV ou FLAC stéréo en 44,1 kHz. Convertissez gratuitement vos fichiers MP4, M4A, OGG ou 48 kHz.",
 "Format audio pour DistroKid et Spotify",
 "Le fichier accepté par tous les distributeurs est un WAV ou FLAC stéréo en 44,1 kHz, 16 bits. Si votre morceau est un M4A, un MP4, un OGG, un enregistrement de téléphone ou un fichier en 48 kHz, StreamPack le convertit exactement ainsi.",
 "Convertir mon morceau en WAV 44,1 kHz →",
 ["Distributeur", "Ce qu'il accepte"],
 [["DistroKid", "WAV, MP3, M4A, FLAC, AIFF ou WMA ; le plus courant : WAV 16 bits 44,1 kHz ; jusqu'à 1 Go"],
  ["Spotify (via votre distributeur)", "FLAC de préférence, WAV accepté ; 44,1 kHz ou plus ; stéréo ; 24 bits si c'est votre master"],
  ["CD Baby", "WAV ou FLAC (MP3 accepté mais déconseillé) ; stéréo, 44,1 kHz, 16 bits"],
  ["TuneCore", "WAV ; 24 bits recommandé, 16 bits 44,1 kHz accepté"],
  ["Amuse", "WAV, stéréo, 44,1 kHz, 16 bits (pas de 24 bits)"]],
 [("Quand StreamPack vous sert, et quand non", ["Si votre STAN a déjà exporté un master WAV ou FLAC que votre distributeur accepte, envoyez-le tel quel : Spotify demande le master d'origine, sans réduction de qualité. StreamPack sert dans les autres cas : le fichier est dans un format refusé, il est en 48 kHz ou en mono, ou vous avez un doute. Vous obtenez un WAV ou FLAC stéréo en 44,1 kHz et 16 bits accepté partout."]),
  ("Noms de fichiers", ["DistroKid refuse les noms de fichiers contenant \\ / : * ? \" ' < > |. StreamPack nomme les fichiers avec votre nom d'artiste et le titre, sans ces caractères."])],
 [("WAV ou FLAC pour DistroKid ?", "Les deux sont sans perte, le son est identique. Les FLAC sont plus légers : pratique pour les morceaux longs ou les albums."),
  ("Un MP3 suffit-il ?", "Certains distributeurs acceptent le MP3, mais le WAV ou le FLAC est recommandé : les plateformes réencodent le fichier, et partir d'un MP3 fait perdre plus de qualité."),
  ("Faut-il envoyer du 24 bits ?", "Si votre master est en 24 bits et que votre distributeur l'accepte, oui. Amuse n'accepte que le 16 bits ; dans le doute, le 16 bits 44,1 kHz passe partout.")])
G["audio", "pt"] = aud("Formato de áudio para DistroKid",
 "Formato de áudio para DistroKid e Spotify: WAV ou FLAC, 16 bits 44,1 kHz",
 "Qual arquivo de áudio enviar para DistroKid, CD Baby, TuneCore ou Amuse para Spotify e Apple Music: WAV ou FLAC estéreo em 44,1 kHz. Converta grátis arquivos MP4, M4A, OGG ou de 48 kHz.",
 "Formato de áudio para DistroKid e Spotify",
 "O arquivo que todas as distribuidoras aceitam é um WAV ou FLAC estéreo em 44,1 kHz e 16 bits. Se sua música é um M4A, um MP4, um OGG, uma gravação do celular ou um arquivo em 48 kHz, o StreamPack converte exatamente assim.",
 "Converter minha música para WAV 44,1 kHz →",
 ["Distribuidora", "O que aceita"],
 [["DistroKid", "WAV, MP3, M4A, FLAC, AIFF ou WMA; o comum é WAV 16 bits 44,1 kHz; até 1 GB"],
  ["Spotify (pela sua distribuidora)", "prefere FLAC, aceita WAV; 44,1 kHz ou mais; estéreo; 24 bits se esse for seu master"],
  ["CD Baby", "WAV ou FLAC (MP3 aceito, mas não recomendado); estéreo, 44,1 kHz, 16 bits"],
  ["TuneCore", "WAV; recomenda 24 bits, aceita 16 bits 44,1 kHz"],
  ["Amuse", "WAV, estéreo, 44,1 kHz, 16 bits (sem 24 bits)"]],
 [("Quando você precisa do StreamPack e quando não", ["Se a sua DAW já exportou um master WAV ou FLAC que a distribuidora aceita, envie assim mesmo: o Spotify pede o master original, sem perda de qualidade. O StreamPack serve para os outros casos: o arquivo está num formato que a distribuidora recusa, está em 48 kHz ou mono, ou você não tem certeza. Você recebe um WAV ou FLAC estéreo em 44,1 kHz e 16 bits que todas aceitam."]),
  ("Nomes de arquivo", ["A DistroKid recusa nomes de arquivo com \\ / : * ? \" ' < > |. O StreamPack nomeia os arquivos com seu nome artístico e o título, sem esses caracteres."])],
 [("WAV ou FLAC para a DistroKid?", "Os dois são sem perdas, então o som é idêntico. O FLAC é mais leve: bom para faixas longas ou álbuns."),
  ("MP3 serve?", "Algumas distribuidoras aceitam MP3, mas o recomendado é WAV ou FLAC: as plataformas recodificam o arquivo, e partir de um MP3 perde mais qualidade."),
  ("Devo enviar em 24 bits?", "Se seu master é 24 bits e a distribuidora aceita, sim. A Amuse só aceita 16 bits; na dúvida, 16 bits 44,1 kHz serve em todas.")])

# ---------------- LUFS ----------------
def lufs(nav, title, desc, h1, lead, cta, blocks, faq):
    return dict(nav=nav, title=title, desc=desc, h1=h1, lead=lead, cta=cta, table=None, blocks=blocks, faq=faq)
G["lufs", "en"] = lufs("Spotify -14 LUFS",
 "Spotify -14 LUFS: Loudness Normalization Explained (Free Tool)",
 "Spotify plays every track at -14 LUFS: louder masters are turned down, quiet ones turned up only if they have headroom. What it means for your mix, plus a free tool to set -14 LUFS with peaks under -1 dB.",
 "Spotify -14 LUFS: what it means for your track",
 "Spotify adjusts every track to -14 LUFS during playback. It doesn't change your file: it just turns the volume down or up. StreamPack can set your track to -14 LUFS with peaks under -1 dB before you upload.",
 "Set my track to -14 LUFS →",
 [("How Spotify normalization works", ("ul", [
   "Target: -14 LUFS integrated (ITU 1770 standard), applied while the track plays",
   "Louder masters are turned down to -14 LUFS: no extra distortion, just lower volume",
   "Quieter masters are turned up only as far as their peaks allow (Spotify leaves 1 dB of headroom), so a quiet track with high peaks can stay quieter than the rest",
   "Spotify's advice: aim for -14 LUFS integrated and keep true peaks below -1 dB"])),
  ("When the -14 LUFS option helps", ["It helps with demos, live recordings and unmastered bounces that are too quiet or uneven, so they don't sound weaker than the tracks around them. If your song is already professionally mastered, keep the master as it is: the option sets the level, it isn't mastering."])],
 [("Do I have to master at -14 LUFS?", "No. Spotify will turn a louder master down anyway. Many engineers master louder on purpose; -14 LUFS is the level you'll be heard at, not a rule."),
  ("Does Spotify change my audio file?", "No. Spotify measures loudness when the track is uploaded and adjusts the volume during playback."),
  ("What do other platforms use?", "Most streaming services normalize too, at similar levels. Aiming around -14 LUFS with peaks under -1 dB works well across platforms.")])
G["lufs", "it"] = lufs("-14 LUFS su Spotify",
 "-14 LUFS su Spotify: come funziona il volume (strumento gratis)",
 "Spotify riproduce ogni brano a -14 LUFS: i master più forti vengono abbassati, quelli bassi alzati solo se hanno margine. Cosa significa per il tuo mix e uno strumento gratis per portarlo a -14 LUFS con picchi sotto -1 dB.",
 "-14 LUFS su Spotify: cosa significa per il tuo brano",
 "Spotify regola ogni brano a -14 LUFS durante l'ascolto. Non modifica il tuo file: alza o abbassa solo il volume. StreamPack può portare il brano a -14 LUFS con i picchi sotto -1 dB prima del caricamento.",
 "Porta il brano a -14 LUFS →",
 [("Come funziona la normalizzazione di Spotify", ("ul", [
   "Obiettivo: -14 LUFS integrati (standard ITU 1770), applicato mentre il brano suona",
   "I master più forti vengono abbassati a -14 LUFS: nessuna distorsione in più, solo volume più basso",
   "I master più bassi vengono alzati solo quanto lo permettono i picchi (Spotify lascia 1 dB di margine): un brano basso con picchi alti può restare più basso degli altri",
   "Il consiglio di Spotify: punta a -14 LUFS integrati e tieni i true peak sotto -1 dB"])),
  ("Quando serve l'opzione -14 LUFS", ["Serve per demo, registrazioni live e bounce non masterizzati troppo bassi o irregolari, così non suonano più deboli dei brani vicini. Se il tuo brano è già masterizzato da un professionista, lascia il master com'è: l'opzione regola il livello, non è un mastering."])],
 [("Devo masterizzare a -14 LUFS?", "No. Un master più forte Spotify lo abbassa comunque. Molti fonici masterizzano più forte di proposito: -14 LUFS è il livello a cui verrai ascoltato, non una regola."),
  ("Spotify modifica il mio file audio?", "No. Spotify misura il volume al caricamento e lo regola durante l'ascolto."),
  ("E le altre piattaforme?", "Quasi tutti i servizi di streaming normalizzano, a livelli simili. Stare intorno a -14 LUFS con i picchi sotto -1 dB funziona bene ovunque.")])
G["lufs", "es"] = lufs("-14 LUFS en Spotify",
 "-14 LUFS en Spotify: la normalización de volumen explicada (gratis)",
 "Spotify reproduce cada tema a -14 LUFS: baja los másteres más fuertes y sube los flojos solo si tienen margen. Qué significa para tu mezcla y una herramienta gratis para dejarlo a -14 LUFS con picos bajo -1 dB.",
 "-14 LUFS en Spotify: qué significa para tu tema",
 "Spotify ajusta cada tema a -14 LUFS mientras se reproduce. No cambia tu archivo: solo sube o baja el volumen. StreamPack puede dejar tu tema a -14 LUFS con picos por debajo de -1 dB antes de subirlo.",
 "Dejar mi tema a -14 LUFS →",
 [("Cómo funciona la normalización de Spotify", ("ul", [
   "Objetivo: -14 LUFS integrados (estándar ITU 1770), aplicado durante la reproducción",
   "Los másteres más fuertes bajan a -14 LUFS: sin distorsión extra, solo menos volumen",
   "Los másteres más flojos suben solo hasta donde lo permiten sus picos (Spotify deja 1 dB de margen): un tema flojo con picos altos puede sonar más bajo que el resto",
   "El consejo de Spotify: apunta a -14 LUFS integrados y mantén los true peak por debajo de -1 dB"])),
  ("Cuándo sirve la opción -14 LUFS", ["Sirve para maquetas, directos y bounces sin masterizar demasiado bajos o irregulares, para que no suenen más débiles que los temas de al lado. Si tu tema ya está masterizado por un profesional, deja el máster como está: la opción ajusta el nivel, no es un mastering."])],
 [("¿Tengo que masterizar a -14 LUFS?", "No. Spotify bajará igualmente un máster más fuerte. Muchos ingenieros masterizan más alto a propósito: -14 LUFS es el nivel al que se te escuchará, no una regla."),
  ("¿Spotify cambia mi archivo de audio?", "No. Spotify mide el volumen al subir el tema y lo ajusta durante la reproducción."),
  ("¿Y las demás plataformas?", "Casi todos los servicios de streaming normalizan, con niveles parecidos. Quedarte en torno a -14 LUFS con picos bajo -1 dB funciona bien en todas.")])
G["lufs", "de"] = lufs("-14 LUFS bei Spotify",
 "-14 LUFS bei Spotify: Lautheitsnormalisierung erklärt (kostenloses Tool)",
 "Spotify spielt jeden Song mit -14 LUFS: Lautere Master werden leiser gemacht, leise nur angehoben, wenn sie Headroom haben. Was das für deinen Mix bedeutet – plus ein kostenloses Tool für -14 LUFS mit Peaks unter -1 dB.",
 "-14 LUFS bei Spotify: Was das für deinen Song bedeutet",
 "Spotify regelt jeden Song beim Abspielen auf -14 LUFS. Deine Datei bleibt unverändert, nur die Lautstärke wird angepasst. StreamPack kann deinen Song vor dem Upload auf -14 LUFS mit Peaks unter -1 dB bringen.",
 "Song auf -14 LUFS bringen →",
 [("So funktioniert die Normalisierung bei Spotify", ("ul", [
   "Ziel: -14 LUFS integriert (Standard ITU 1770), angewendet während der Wiedergabe",
   "Lautere Master werden auf -14 LUFS abgesenkt: keine zusätzliche Verzerrung, nur leiser",
   "Leisere Master werden nur so weit angehoben, wie die Peaks es erlauben (Spotify lässt 1 dB Headroom): Ein leiser Song mit hohen Peaks kann leiser bleiben als der Rest",
   "Spotifys Tipp: Ziel -14 LUFS integriert, True Peaks unter -1 dB"])),
  ("Wann die -14-LUFS-Option hilft", ["Sie hilft bei Demos, Live-Aufnahmen und ungemasterten Bounces, die zu leise oder ungleichmäßig sind, damit sie nicht schwächer klingen als die Songs daneben. Ist dein Song schon professionell gemastert, lass den Master, wie er ist: Die Option stellt den Pegel ein, sie ist kein Mastering."])],
 [("Muss ich auf -14 LUFS mastern?", "Nein. Einen lauteren Master macht Spotify ohnehin leiser. Viele Engineers mastern bewusst lauter: -14 LUFS ist der Pegel, mit dem du gehört wirst, keine Regel."),
  ("Verändert Spotify meine Audiodatei?", "Nein. Spotify misst die Lautheit beim Upload und passt die Lautstärke bei der Wiedergabe an."),
  ("Und die anderen Plattformen?", "Fast alle Streamingdienste normalisieren, auf ähnlichem Niveau. Rund -14 LUFS mit Peaks unter -1 dB funktioniert überall gut.")])
G["lufs", "fr"] = lufs("-14 LUFS sur Spotify",
 "-14 LUFS sur Spotify : la normalisation du volume expliquée (outil gratuit)",
 "Spotify lit chaque morceau à -14 LUFS : les masters plus forts sont baissés, les plus faibles montés seulement s'ils ont de la marge. Ce que ça change pour votre mix, et un outil gratuit pour régler -14 LUFS avec des crêtes sous -1 dB.",
 "-14 LUFS sur Spotify : ce que ça change pour votre morceau",
 "Spotify règle chaque morceau à -14 LUFS pendant la lecture. Il ne modifie pas votre fichier : il monte ou baisse seulement le volume. StreamPack peut régler votre morceau à -14 LUFS avec des crêtes sous -1 dB avant l'envoi.",
 "Régler mon morceau à -14 LUFS →",
 [("Comment fonctionne la normalisation de Spotify", ("ul", [
   "Cible : -14 LUFS intégrés (norme ITU 1770), appliquée pendant la lecture",
   "Les masters plus forts sont baissés à -14 LUFS : pas de distorsion en plus, juste moins de volume",
   "Les masters plus faibles ne sont montés que dans la limite de leurs crêtes (Spotify garde 1 dB de marge) : un morceau faible avec des crêtes hautes peut rester plus bas que les autres",
   "Le conseil de Spotify : viser -14 LUFS intégrés et garder les true peaks sous -1 dB"])),
  ("Quand l'option -14 LUFS est utile", ["Elle sert pour les démos, les enregistrements live et les bounces non masterisés trop faibles ou irréguliers, pour qu'ils ne sonnent pas plus faibles que les morceaux voisins. Si votre morceau est déjà masterisé par un pro, gardez le master tel quel : l'option règle le niveau, ce n'est pas un mastering."])],
 [("Dois-je masteriser à -14 LUFS ?", "Non. Spotify baissera de toute façon un master plus fort. Beaucoup d'ingénieurs masterisent plus fort exprès : -14 LUFS est le niveau auquel vous serez écouté, pas une règle."),
  ("Spotify modifie-t-il mon fichier audio ?", "Non. Spotify mesure le volume à l'envoi et l'ajuste pendant la lecture."),
  ("Et les autres plateformes ?", "Presque tous les services de streaming normalisent, à des niveaux proches. Viser environ -14 LUFS avec des crêtes sous -1 dB fonctionne bien partout.")])
G["lufs", "pt"] = lufs("-14 LUFS no Spotify",
 "-14 LUFS no Spotify: normalização de volume explicada (ferramenta grátis)",
 "O Spotify toca cada faixa a -14 LUFS: masters mais altos são abaixados, os baixos só sobem se tiverem margem. O que isso significa para sua mixagem e uma ferramenta grátis para deixar em -14 LUFS com picos abaixo de -1 dB.",
 "-14 LUFS no Spotify: o que significa para sua música",
 "O Spotify ajusta cada faixa para -14 LUFS durante a reprodução. Ele não altera seu arquivo: só aumenta ou diminui o volume. O StreamPack pode deixar sua faixa em -14 LUFS com picos abaixo de -1 dB antes do envio.",
 "Deixar minha faixa em -14 LUFS →",
 [("Como funciona a normalização do Spotify", ("ul", [
   "Alvo: -14 LUFS integrados (padrão ITU 1770), aplicado durante a reprodução",
   "Masters mais altos são abaixados para -14 LUFS: sem distorção extra, só menos volume",
   "Masters mais baixos só sobem até onde os picos permitem (o Spotify deixa 1 dB de margem): uma faixa baixa com picos altos pode ficar mais baixa que as outras",
   "A dica do Spotify: mire em -14 LUFS integrados e mantenha os true peaks abaixo de -1 dB"])),
  ("Quando a opção -14 LUFS ajuda", ["Ajuda com demos, gravações ao vivo e bounces sem master muito baixos ou irregulares, para não soarem mais fracos que as faixas ao lado. Se sua música já foi masterizada por um profissional, mantenha o master como está: a opção ajusta o nível, não é masterização."])],
 [("Preciso masterizar em -14 LUFS?", "Não. O Spotify vai abaixar um master mais alto de qualquer jeito. Muitos engenheiros masterizam mais alto de propósito: -14 LUFS é o nível em que você será ouvido, não uma regra."),
  ("O Spotify altera meu arquivo de áudio?", "Não. O Spotify mede o volume no envio e ajusta durante a reprodução."),
  ("E as outras plataformas?", "Quase todos os serviços de streaming normalizam, em níveis parecidos. Ficar perto de -14 LUFS com picos abaixo de -1 dB funciona bem em todos.")])

e = lambda s: html.escape(s, quote=True)
url = lambda k, l: f"{SITO}/{SLUG[k][l]}/"


def pagina(k, l):
    d, c = G[k, l], C[l]
    alt = "".join(f'<link rel="alternate" hreflang="{x}" href="{url(k, x)}">' for x in LINGUE) + f'<link rel="alternate" hreflang="x-default" href="{url(k, "en")}">'
    lingue = " ".join(f'<a href="/{SLUG[k][x]}/" hreflang="{x}" lang="{x}">{x.upper()}</a>' for x in LINGUE if x != l)
    apri = f"/?lang={l}&{APRI[k]}"
    cta = f'<a class="btn" style="font-size:1.1rem;padding:16px 22px" href="{e(apri)}">{e(d["cta"])}</a><p class="msg">{e(c["free"])}</p>'
    corpo = [f"<h1>{e(d['h1'])}</h1>", f'<p class="lead">{e(d["lead"])}</p>', cta]
    if d["table"]:
        hdr, righe = d["table"]
        corpo.append("<table><thead><tr>" + "".join(f"<th>{e(h)}</th>" for h in hdr) + "</tr></thead><tbody>" +
                     "".join("<tr>" + "".join(f"<td>{'<b>'+e(v)+'</b>' if i == 0 else e(v)}</td>" for i, v in enumerate(r)) + "</tr>" for r in righe) + "</tbody></table>")
        corpo.append(f'<p class="msg">{e(c["check"])}</p>')
    for h, v in d["blocks"]:
        corpo.append(f"<h2>{e(h)}</h2>")
        if isinstance(v, tuple): corpo.append("<ul>" + "".join(f"<li>{e(x)}</li>" for x in v[1]) + "</ul>")
        else: corpo.extend(f"<p>{e(x)}</p>" for x in v)
    corpo.append("<h2>FAQ</h2>" + "".join(f"<h3>{e(q)}</h3><p>{e(a)}</p>" for q, a in d["faq"]))
    corpo.append(f'<div class="card cta"><p style="margin-top:0"><b>{e(d["h1"])}</b></p>{cta}</div>')
    altre = " · ".join([f'<a href="/{CHECK[x][l][0]}/">{e(CHECK[x][l][1])}</a>' for x in CHECK] + [f'<a href="/{SLUG[x][l]}/">{e(G[x, l]["nav"])}</a>' for x in SLUG if x != k])
    corpo.append(f"<h2>{e(c['other'])}</h2><p>{altre} · <a href=\"/convert/\">{e(c['conv'])}</a></p>")
    ld_app = {"@context": "https://schema.org", "@type": "WebApplication", "name": "StreamPack", "url": url(k, l), "inLanguage": l,
              "description": d["desc"], "applicationCategory": "MultimediaApplication", "operatingSystem": "Any (browser, Android)",
              "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}}
    ld_faq = {"@context": "https://schema.org", "@type": "FAQPage", "inLanguage": l,
              "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in d["faq"]]}
    ld = lambda o: json.dumps(o, ensure_ascii=False).replace("</", "<\\/")
    return f"""<!doctype html><html lang="{l}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(d["title"])}</title><meta name="description" content="{e(d["desc"])}"><link rel="canonical" href="{url(k, l)}">{alt}
<meta property="og:type" content="article"><meta property="og:url" content="{url(k, l)}"><meta property="og:title" content="{e(d["title"])}"><meta property="og:description" content="{e(d["desc"])}"><meta property="og:image" content="{SITO}/og-image.jpg">
<link rel="icon" href="/icon-192.png"><link rel="stylesheet" href="/video/style.css">
<script type="application/ld+json">{ld(ld_app)}</script><script type="application/ld+json">{ld(ld_faq)}</script>
<script src="/ext-links.js" defer></script></head><body><div class="w">
<nav><a href="/?lang={l}">StreamPack</a><small>{lingue}</small></nav>
{"".join(corpo)}
<footer><a href="/?lang={l}">StreamPack</a> · <a href="/privacy">Privacy</a><br>{e(c["foot"])}</footer></div></body></html>
"""


if __name__ == "__main__":
    for k in SLUG:
        for l in LINGUE:
            cart = os.path.join(ROOT, SLUG[k][l]); os.makedirs(cart, exist_ok=True)
            with open(os.path.join(cart, "index.html"), "w", encoding="utf-8") as f: f.write(pagina(k, l))
            print(url(k, l), len(G[k, l]["title"]))
