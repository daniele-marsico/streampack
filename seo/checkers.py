# Pagine con strumento gratuito dentro (6 lingue): "LUFS checker" e "ISRC / UPC checker".
# Parole chiave (Ubersuggest, nov 2026, globale): "isrc checker" ~4.400/mese, "lufs checker" ~1.300/mese,
# "audio file checker" solo ~50. La misura gira nel browser con /check.js + /checkers.js: niente upload.
# Livelli delle piattaforme: Spotify -14 LUFS è pubblicato da Spotify; gli altri sono i valori misurati più spesso.
# Uso: python3 seo/checkers.py  -> scrive le cartelle e stampa gli URL.
import json, os
from guide import SITO, LINGUE, C, CHECK, SLUG, G, e, ROOT

CSS = """<style>
.drop{position:relative;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;min-height:140px;border-radius:18px;text-align:center;padding:18px;cursor:pointer;
 background:linear-gradient(var(--surface),var(--surface)) padding-box,var(--grad) border-box;border:2px dashed transparent;margin:18px 0 0}
.drop b{font-size:1.25rem}.drop small{color:var(--muted)}.drop input{position:absolute;inset:0;opacity:0;cursor:pointer;width:100%;height:100%}
.big{font-size:3rem;font-weight:800;line-height:1.1;margin:10px 0 6px;font-variant-numeric:tabular-nums}.big small{font-size:1.1rem;color:var(--muted);font-weight:600}
.kv th{width:42%}.kv td{font-variant-numeric:tabular-nums}
.issues{list-style:none;padding:0;margin:14px 0 0;display:grid;gap:6px;justify-items:stretch;text-align:left}.issues li{padding:8px 12px;border-radius:10px;font-size:.93rem;text-align:left}
.res td:nth-child(2){white-space:nowrap}
.issues .w,.warn{color:#FBBF24}.issues .w{background:rgba(251,191,36,.12)}.issues .ok,.ok{color:#4ADE80}.issues .ok{background:rgba(74,222,128,.10)}
.codein{font-family:ui-monospace,Menlo,monospace;letter-spacing:.04em;text-transform:uppercase}
.res h3{margin-top:1.4em}
</style>"""

P = {}
# ================= LUFS checker =================
P["lufs", "en"] = dict(
 title="LUFS Checker – Free Online Loudness & True Peak Meter (No Upload)",
 desc="Check your track's integrated LUFS, true peak and loudness range in seconds, and see what Spotify, Apple Music, YouTube and the others will do to it. Free and private: the file never leaves your device.",
 h1="LUFS checker: how loud is your track?",
 lead="Drop your master to measure integrated loudness (LUFS), true peak (dBTP) and loudness range (LU), to the ITU-R BS.1770 standard. You also see how much each streaming platform will turn it down, and the problems that get releases rejected: clipping, long silences, compressed source files.",
 cta="Fix it in StreamPack: -14 LUFS, true peak -1 dB →",
 blocks=[("What the numbers mean", ("ul", [
   "Integrated LUFS: the average loudness of the whole track, the number platforms use to set the volume",
   "True peak (dBTP): the highest level once the waveform is rebuilt between samples. Above -1 dBTP, the MP3 and AAC versions can distort",
   "Loudness range (LU): how much the level moves between quiet and loud parts. Low values mean a heavily compressed track"])),
  ("Louder isn't better on streaming", ["Spotify, YouTube and the other platforms turn loud masters down to their level. A track at -8 LUFS plays about 6 dB quieter on Spotify and keeps the squashed sound of the limiter. Aim near -14 LUFS with true peaks at -1 dBTP or lower, unless you master loud on purpose."]),
  ("Your file stays on your device", ["The measurement runs in your browser: nothing is uploaded and you don't need an account. WAV, FLAC, AIFF, MP3, M4A and OGG files work."])],
 faq=[("How many LUFS should my song be for Spotify?", "Spotify plays music at -14 LUFS. A louder master is turned down; a quieter one is turned up only as far as its peaks allow. -14 LUFS with true peak at -1 dBTP is a safe target."),
  ("Is this LUFS meter accurate?", "It uses the ITU-R BS.1770 K-weighting and gating for integrated loudness, EBU Tech 3342 for loudness range and 4× oversampling for true peak. Results match professional meters within a few tenths of a dB."),
  ("Why is true peak higher than the sample peak?", "Between two samples the rebuilt waveform can go higher than either of them. Those inter-sample peaks come out when the file is turned into MP3 or AAC, which is why platforms ask for -1 dBTP."),
  ("Can I fix the loudness here?", "Yes: open StreamPack, turn on Spotify-ready loudness and the track is set to -14 LUFS with true peak at -1 dBTP, then saved as WAV, FLAC or MP3 ready for your distributor.")],
 ui=dict(pick="Choose a track", pickSub="WAV, FLAC, AIFF, MP3, M4A… measured on your device, nothing is uploaded", measuring="Measuring…", err="This file can't be opened in this browser",
  TP="True peak", LRA="Loudness range", file="File", dur="Duration", stereo="stereo", plat="What each platform does", cols=["Platform", "Level", "Your track"],
  down="turned down {d} dB", below="{d} dB below its level", same="about the same level",
  note="Spotify publishes its -14 LUFS level; the other values are the ones most often measured and can change.",
  tpw="True peak above -1 dBTP: the MP3/AAC version can distort", tpok="True peak at or below -1 dBTP",
  clip="Clipping in {n} places: fix it in the mix", lead="{s} s of silence at the start", tail="{s} s of silence at the end", silent="The file is silent",
  lossy="{k} is compressed: if you have the WAV or FLAC master, use that", mis="Named .{e} but it's really {k}", mono="Mono file: many distributors want stereo", dc="DC offset in the file"))
P["lufs", "it"] = dict(
 title="Misura LUFS online gratis – loudness e true peak del brano (senza upload)",
 desc="Misura in pochi secondi LUFS integrati, true peak e loudness range del tuo brano e scopri cosa faranno Spotify, Apple Music, YouTube e gli altri. Gratis e privato: il file non lascia il tuo dispositivo.",
 h1="Misura i LUFS: quanto è forte il tuo brano?",
 lead="Carica il master per misurare loudness integrata (LUFS), true peak (dBTP) e loudness range (LU) secondo lo standard ITU-R BS.1770. Vedi anche di quanto lo abbasserà ogni piattaforma e i problemi che fanno rifiutare le release: clipping, silenzi lunghi, file compressi.",
 cta="Sistemalo in StreamPack: -14 LUFS, true peak -1 dB →",
 blocks=[("Cosa significano i numeri", ("ul", [
   "LUFS integrati: il volume medio di tutto il brano, il numero che le piattaforme usano per regolare il volume",
   "True peak (dBTP): il livello più alto dell'onda ricostruita tra un campione e l'altro. Sopra -1 dBTP le versioni MP3 e AAC possono distorcere",
   "Loudness range (LU): quanto cambia il livello tra parti piano e parti forti. Valori bassi indicano un brano molto compresso"])),
  ("Sullo streaming più forte non vuol dire meglio", ["Spotify, YouTube e le altre piattaforme abbassano i master troppo forti fino al loro livello. Un brano a -8 LUFS su Spotify suona circa 6 dB più basso e si tiene il suono schiacciato del limiter. Punta a circa -14 LUFS con true peak a -1 dBTP o meno, a meno che tu non voglia un master forte per scelta."]),
  ("Il file resta sul tuo dispositivo", ["La misura avviene nel browser: niente upload e niente account. Funziona con WAV, FLAC, AIFF, MP3, M4A e OGG."])],
 faq=[("Quanti LUFS deve avere un brano per Spotify?", "Spotify riproduce la musica a -14 LUFS. Un master più forte viene abbassato; uno più basso viene alzato solo finché i picchi lo permettono. -14 LUFS con true peak a -1 dBTP è un obiettivo sicuro."),
  ("Questa misura è precisa?", "Usa la pesatura K e il gating ITU-R BS.1770 per la loudness integrata, EBU Tech 3342 per il loudness range e il sovracampionamento 4× per il true peak. I risultati coincidono con i misuratori professionali entro pochi decimi di dB."),
  ("Perché il true peak è più alto del picco dei campioni?", "Tra due campioni l'onda ricostruita può salire più in alto di entrambi. Questi picchi tra i campioni emergono quando il file diventa MP3 o AAC: per questo le piattaforme chiedono -1 dBTP."),
  ("Posso correggere il volume qui?", "Sì: apri StreamPack, attiva il volume per Spotify e il brano viene portato a -14 LUFS con true peak a -1 dBTP, poi salvato in WAV, FLAC o MP3 pronto per il distributore.")],
 ui=dict(pick="Scegli il brano", pickSub="WAV, FLAC, AIFF, MP3, M4A… misurato sul tuo dispositivo, niente upload", measuring="Misuro…", err="Questo file non si apre in questo browser",
  TP="True peak", LRA="Loudness range", file="File", dur="Durata", stereo="stereo", plat="Cosa fa ogni piattaforma", cols=["Piattaforma", "Livello", "Il tuo brano"],
  down="abbassato di {d} dB", below="{d} dB sotto il suo livello", same="circa allo stesso livello",
  note="Il livello di -14 LUFS è pubblicato da Spotify; gli altri sono i valori misurati più spesso e possono cambiare.",
  tpw="True peak sopra -1 dBTP: la versione MP3/AAC può distorcere", tpok="True peak a -1 dBTP o meno",
  clip="Clipping in {n} punti: va sistemato nel mix", lead="{s} s di silenzio all'inizio", tail="{s} s di silenzio alla fine", silent="Il file è silenzioso",
  lossy="{k} è compresso: se hai il master WAV o FLAC, usa quello", mis="Si chiama .{e} ma in realtà è {k}", mono="File mono: molti distributori vogliono lo stereo", dc="DC offset nel file"))
P["lufs", "es"] = dict(
 title="Medidor de LUFS online gratis – loudness y true peak (sin subir archivos)",
 desc="Mide en segundos los LUFS integrados, el true peak y el rango de loudness de tu canción y descubre qué harán Spotify, Apple Music, YouTube y las demás. Gratis y privado: el archivo no sale de tu dispositivo.",
 h1="Medidor de LUFS: ¿qué tan fuerte suena tu canción?",
 lead="Sube tu máster para medir la sonoridad integrada (LUFS), el true peak (dBTP) y el rango de loudness (LU) según el estándar ITU-R BS.1770. También ves cuánto lo bajará cada plataforma y los problemas que hacen rechazar un lanzamiento: clipping, silencios largos, archivos comprimidos.",
 cta="Arréglalo en StreamPack: -14 LUFS, true peak -1 dB →",
 blocks=[("Qué significan los números", ("ul", [
   "LUFS integrados: la sonoridad media de toda la canción, el número que usan las plataformas para ajustar el volumen",
   "True peak (dBTP): el nivel más alto de la onda reconstruida entre muestras. Por encima de -1 dBTP, las versiones MP3 y AAC pueden distorsionar",
   "Rango de loudness (LU): cuánto cambia el nivel entre partes suaves y fuertes. Valores bajos indican una canción muy comprimida"])),
  ("En streaming, más fuerte no es mejor", ["Spotify, YouTube y las demás plataformas bajan los másteres demasiado fuertes hasta su nivel. Una canción a -8 LUFS suena unos 6 dB más baja en Spotify y conserva el sonido aplastado del limitador. Apunta a unos -14 LUFS con true peak de -1 dBTP o menos, salvo que quieras un máster fuerte a propósito."]),
  ("Tu archivo no sale de tu dispositivo", ["La medición se hace en el navegador: no se sube nada y no necesitas cuenta. Funciona con WAV, FLAC, AIFF, MP3, M4A y OGG."])],
 faq=[("¿Cuántos LUFS debe tener una canción para Spotify?", "Spotify reproduce la música a -14 LUFS. Un máster más fuerte se baja; uno más suave se sube solo hasta donde lo permiten sus picos. -14 LUFS con true peak de -1 dBTP es un objetivo seguro."),
  ("¿Es precisa esta medición?", "Usa la ponderación K y el gating de ITU-R BS.1770 para la sonoridad integrada, EBU Tech 3342 para el rango de loudness y sobremuestreo 4× para el true peak. Los resultados coinciden con los medidores profesionales en pocas décimas de dB."),
  ("¿Por qué el true peak es más alto que el pico de las muestras?", "Entre dos muestras la onda reconstruida puede subir más que ambas. Esos picos entre muestras aparecen al pasar el archivo a MP3 o AAC: por eso las plataformas piden -1 dBTP."),
  ("¿Puedo corregir el volumen aquí?", "Sí: abre StreamPack, activa el volumen para Spotify y la canción queda a -14 LUFS con true peak de -1 dBTP, guardada en WAV, FLAC o MP3 lista para tu distribuidora.")],
 ui=dict(pick="Elige la canción", pickSub="WAV, FLAC, AIFF, MP3, M4A… se mide en tu dispositivo, no se sube nada", measuring="Midiendo…", err="Este archivo no se abre en este navegador",
  TP="True peak", LRA="Rango de loudness", file="Archivo", dur="Duración", stereo="estéreo", plat="Qué hace cada plataforma", cols=["Plataforma", "Nivel", "Tu canción"],
  down="se baja {d} dB", below="{d} dB por debajo de su nivel", same="más o menos al mismo nivel",
  note="Spotify publica su nivel de -14 LUFS; los demás son los valores medidos con más frecuencia y pueden cambiar.",
  tpw="True peak por encima de -1 dBTP: la versión MP3/AAC puede distorsionar", tpok="True peak en -1 dBTP o menos",
  clip="Clipping en {n} puntos: arréglalo en la mezcla", lead="{s} s de silencio al inicio", tail="{s} s de silencio al final", silent="El archivo está en silencio",
  lossy="{k} está comprimido: si tienes el máster WAV o FLAC, usa ese", mis="Se llama .{e} pero en realidad es {k}", mono="Archivo mono: muchas distribuidoras piden estéreo", dc="DC offset en el archivo"))
P["lufs", "de"] = dict(
 title="LUFS messen online, kostenlos – Lautheit & True Peak (ohne Upload)",
 desc="Miss in Sekunden integrierte LUFS, True Peak und Loudness Range deines Songs und sieh, was Spotify, Apple Music, YouTube und die anderen damit machen. Kostenlos und privat: Die Datei bleibt auf deinem Gerät.",
 h1="LUFS messen: Wie laut ist dein Song?",
 lead="Lade deinen Master, um integrierte Lautheit (LUFS), True Peak (dBTP) und Loudness Range (LU) nach ITU-R BS.1770 zu messen. Du siehst auch, wie stark jede Plattform ihn leiser macht, und die Probleme, an denen Releases scheitern: Clipping, lange Stille, komprimierte Quelldateien.",
 cta="In StreamPack korrigieren: -14 LUFS, True Peak -1 dB →",
 blocks=[("Was die Zahlen bedeuten", ("ul", [
   "Integrierte LUFS: die durchschnittliche Lautheit des ganzen Songs, nach der die Plattformen die Lautstärke einstellen",
   "True Peak (dBTP): der höchste Pegel der zwischen den Samples rekonstruierten Wellenform. Über -1 dBTP können MP3- und AAC-Versionen verzerren",
   "Loudness Range (LU): wie stark sich der Pegel zwischen leisen und lauten Teilen ändert. Niedrige Werte bedeuten einen stark komprimierten Song"])),
  ("Beim Streaming ist lauter nicht besser", ["Spotify, YouTube und die anderen Plattformen drehen zu laute Master auf ihren Pegel herunter. Ein Song mit -8 LUFS läuft auf Spotify etwa 6 dB leiser und behält den gequetschten Klang des Limiters. Ziel sind etwa -14 LUFS mit True Peak bei -1 dBTP oder darunter, außer du willst bewusst einen lauten Master."]),
  ("Deine Datei bleibt auf deinem Gerät", ["Die Messung läuft im Browser: Nichts wird hochgeladen, du brauchst kein Konto. WAV, FLAC, AIFF, MP3, M4A und OGG funktionieren."])],
 faq=[("Wie viele LUFS sollte ein Song für Spotify haben?", "Spotify spielt Musik mit -14 LUFS ab. Ein lauterer Master wird leiser gemacht, ein leiserer nur so weit angehoben, wie seine Spitzen es erlauben. -14 LUFS mit True Peak bei -1 dBTP ist ein sicheres Ziel."),
  ("Ist diese Messung genau?", "Sie nutzt K-Gewichtung und Gating nach ITU-R BS.1770 für die integrierte Lautheit, EBU Tech 3342 für die Loudness Range und 4-faches Oversampling für den True Peak. Die Werte stimmen bis auf wenige Zehntel dB mit professionellen Messgeräten überein."),
  ("Warum ist der True Peak höher als der Sample-Peak?", "Zwischen zwei Samples kann die rekonstruierte Wellenform höher steigen als beide. Diese Inter-Sample-Peaks tauchen auf, wenn die Datei zu MP3 oder AAC wird: Deshalb verlangen die Plattformen -1 dBTP."),
  ("Kann ich die Lautheit hier korrigieren?", "Ja: Öffne StreamPack, schalte die Spotify-Lautstärke ein, und der Song wird auf -14 LUFS mit True Peak bei -1 dBTP gebracht und als WAV, FLAC oder MP3 für deinen Vertrieb gespeichert.")],
 ui=dict(pick="Song wählen", pickSub="WAV, FLAC, AIFF, MP3, M4A… wird auf deinem Gerät gemessen, nichts wird hochgeladen", measuring="Wird gemessen…", err="Diese Datei lässt sich in diesem Browser nicht öffnen",
  TP="True Peak", LRA="Loudness Range", file="Datei", dur="Dauer", stereo="Stereo", plat="Was jede Plattform macht", cols=["Plattform", "Pegel", "Dein Song"],
  down="{d} dB leiser", below="{d} dB unter ihrem Pegel", same="etwa gleicher Pegel",
  note="Spotify veröffentlicht seinen Pegel von -14 LUFS; die anderen Werte sind die am häufigsten gemessenen und können sich ändern.",
  tpw="True Peak über -1 dBTP: Die MP3/AAC-Version kann verzerren", tpok="True Peak bei -1 dBTP oder darunter",
  clip="Clipping an {n} Stellen: im Mix beheben", lead="{s} s Stille am Anfang", tail="{s} s Stille am Ende", silent="Die Datei ist stumm",
  lossy="{k} ist komprimiert: Wenn du den WAV- oder FLAC-Master hast, nimm den", mis="Heißt .{e}, ist aber eigentlich {k}", mono="Mono-Datei: Viele Vertriebe wollen Stereo", dc="DC-Offset in der Datei"))
P["lufs", "fr"] = dict(
 title="Mesurer les LUFS en ligne, gratuit – loudness et true peak (sans envoi)",
 desc="Mesure en quelques secondes les LUFS intégrés, le true peak et la plage de loudness de ton morceau, et vois ce que Spotify, Apple Music, YouTube et les autres vont en faire. Gratuit et privé : le fichier ne quitte pas ton appareil.",
 h1="Mesurer les LUFS : ton morceau est-il trop fort ?",
 lead="Dépose ton master pour mesurer la loudness intégrée (LUFS), le true peak (dBTP) et la plage de loudness (LU) selon la norme ITU-R BS.1770. Tu vois aussi de combien chaque plateforme va le baisser, et les problèmes qui font refuser une sortie : clipping, longs silences, fichiers compressés.",
 cta="Corrige-le dans StreamPack : -14 LUFS, true peak -1 dB →",
 blocks=[("Ce que veulent dire les chiffres", ("ul", [
   "LUFS intégrés : la loudness moyenne de tout le morceau, le chiffre que les plateformes utilisent pour régler le volume",
   "True peak (dBTP) : le niveau le plus haut de l'onde reconstruite entre les échantillons. Au-dessus de -1 dBTP, les versions MP3 et AAC peuvent saturer",
   "Plage de loudness (LU) : à quel point le niveau varie entre les passages doux et forts. Une valeur basse indique un morceau très compressé"])),
  ("En streaming, plus fort n'est pas mieux", ["Spotify, YouTube et les autres plateformes baissent les masters trop forts jusqu'à leur niveau. Un morceau à -8 LUFS joue environ 6 dB plus bas sur Spotify et garde le son écrasé du limiteur. Vise environ -14 LUFS avec un true peak à -1 dBTP ou moins, sauf si tu veux un master fort exprès."]),
  ("Ton fichier reste sur ton appareil", ["La mesure se fait dans le navigateur : rien n'est envoyé, aucun compte n'est nécessaire. WAV, FLAC, AIFF, MP3, M4A et OGG fonctionnent."])],
 faq=[("Combien de LUFS pour un morceau sur Spotify ?", "Spotify joue la musique à -14 LUFS. Un master plus fort est baissé ; un master plus doux n'est monté que dans la limite de ses crêtes. -14 LUFS avec un true peak à -1 dBTP est un objectif sûr."),
  ("Cette mesure est-elle précise ?", "Elle utilise la pondération K et le gating de l'ITU-R BS.1770 pour la loudness intégrée, l'EBU Tech 3342 pour la plage de loudness et un suréchantillonnage 4× pour le true peak. Les résultats correspondent aux mesureurs professionnels à quelques dixièmes de dB près."),
  ("Pourquoi le true peak est-il plus haut que la crête des échantillons ?", "Entre deux échantillons, l'onde reconstruite peut monter plus haut que les deux. Ces crêtes inter-échantillons apparaissent quand le fichier devient MP3 ou AAC : c'est pour ça que les plateformes demandent -1 dBTP."),
  ("Puis-je corriger le volume ici ?", "Oui : ouvre StreamPack, active le volume pour Spotify et le morceau est mis à -14 LUFS avec un true peak à -1 dBTP, puis enregistré en WAV, FLAC ou MP3 prêt pour ton distributeur.")],
 ui=dict(pick="Choisir le morceau", pickSub="WAV, FLAC, AIFF, MP3, M4A… mesuré sur ton appareil, rien n'est envoyé", measuring="Mesure en cours…", err="Ce fichier ne s'ouvre pas dans ce navigateur",
  TP="True peak", LRA="Plage de loudness", file="Fichier", dur="Durée", stereo="stéréo", plat="Ce que fait chaque plateforme", cols=["Plateforme", "Niveau", "Ton morceau"],
  down="baissé de {d} dB", below="{d} dB sous son niveau", same="à peu près au même niveau",
  note="Spotify publie son niveau de -14 LUFS ; les autres valeurs sont celles mesurées le plus souvent et peuvent changer.",
  tpw="True peak au-dessus de -1 dBTP : la version MP3/AAC peut saturer", tpok="True peak à -1 dBTP ou moins",
  clip="Clipping à {n} endroits : à corriger au mix", lead="{s} s de silence au début", tail="{s} s de silence à la fin", silent="Le fichier est silencieux",
  lossy="{k} est compressé : si tu as le master WAV ou FLAC, utilise-le", mis="Nommé .{e} mais c'est en fait du {k}", mono="Fichier mono : beaucoup de distributeurs veulent du stéréo", dc="DC offset dans le fichier"))
P["lufs", "pt"] = dict(
 title="Medidor de LUFS online grátis – loudness e true peak da sua faixa (sem upload)",
 desc="Meça em segundos os LUFS integrados, o true peak e a faixa de loudness da sua música e veja o que Spotify, Apple Music, YouTube e as outras vão fazer com ela. Grátis e privado: o arquivo não sai do seu aparelho.",
 h1="Medidor de LUFS: qual o volume da sua faixa?",
 lead="Envie seu master para medir a loudness integrada (LUFS), o true peak (dBTP) e a faixa de loudness (LU) pelo padrão ITU-R BS.1770. Você também vê quanto cada plataforma vai abaixar e os problemas que fazem um lançamento ser recusado: clipping, silêncios longos, arquivos comprimidos.",
 cta="Corrija no StreamPack: -14 LUFS, true peak -1 dB →",
 blocks=[("O que os números significam", ("ul", [
   "LUFS integrados: a loudness média da faixa inteira, o número que as plataformas usam para ajustar o volume",
   "True peak (dBTP): o nível mais alto da onda reconstruída entre as amostras. Acima de -1 dBTP, as versões MP3 e AAC podem distorcer",
   "Faixa de loudness (LU): quanto o nível muda entre partes suaves e fortes. Valores baixos indicam uma faixa muito comprimida"])),
  ("No streaming, mais alto não é melhor", ["Spotify, YouTube e as outras plataformas abaixam masters altos demais até o nível delas. Uma faixa a -8 LUFS toca cerca de 6 dB mais baixa no Spotify e mantém o som esmagado do limitador. Mire em cerca de -14 LUFS com true peak de -1 dBTP ou menos, a não ser que queira um master alto de propósito."]),
  ("Seu arquivo fica no seu aparelho", ["A medição acontece no navegador: nada é enviado e não precisa de conta. Funciona com WAV, FLAC, AIFF, MP3, M4A e OGG."])],
 faq=[("Quantos LUFS uma música deve ter para o Spotify?", "O Spotify toca música a -14 LUFS. Um master mais alto é abaixado; um mais baixo só é aumentado até onde os picos permitem. -14 LUFS com true peak de -1 dBTP é um alvo seguro."),
  ("Essa medição é precisa?", "Ela usa a ponderação K e o gating do ITU-R BS.1770 para a loudness integrada, o EBU Tech 3342 para a faixa de loudness e sobreamostragem 4× para o true peak. Os resultados batem com medidores profissionais em poucos décimos de dB."),
  ("Por que o true peak é maior que o pico das amostras?", "Entre duas amostras a onda reconstruída pode subir mais que as duas. Esses picos entre amostras aparecem quando o arquivo vira MP3 ou AAC: por isso as plataformas pedem -1 dBTP."),
  ("Posso corrigir o volume aqui?", "Sim: abra o StreamPack, ative o volume para Spotify e a faixa fica em -14 LUFS com true peak de -1 dBTP, salva em WAV, FLAC ou MP3 pronta para a sua distribuidora.")],
 ui=dict(pick="Escolher a faixa", pickSub="WAV, FLAC, AIFF, MP3, M4A… medido no seu aparelho, nada é enviado", measuring="Medindo…", err="Este arquivo não abre neste navegador",
  TP="True peak", LRA="Faixa de loudness", file="Arquivo", dur="Duração", stereo="estéreo", plat="O que cada plataforma faz", cols=["Plataforma", "Nível", "Sua faixa"],
  down="abaixada {d} dB", below="{d} dB abaixo do nível dela", same="mais ou menos no mesmo nível",
  note="O Spotify publica seu nível de -14 LUFS; os outros são os valores medidos com mais frequência e podem mudar.",
  tpw="True peak acima de -1 dBTP: a versão MP3/AAC pode distorcer", tpok="True peak em -1 dBTP ou menos",
  clip="Clipping em {n} pontos: corrija na mixagem", lead="{s} s de silêncio no início", tail="{s} s de silêncio no final", silent="O arquivo está em silêncio",
  lossy="{k} é comprimido: se você tem o master WAV ou FLAC, use esse", mis="Chama-se .{e} mas na verdade é {k}", mono="Arquivo mono: muitas distribuidoras pedem estéreo", dc="DC offset no arquivo"))

# ================= ISRC / UPC checker =================
P["isrc", "en"] = dict(
 title="ISRC Checker & UPC/EAN Barcode Validator – Free, Instant",
 desc="Check that an ISRC or a UPC/EAN barcode is valid before you release: format, country, year and check digit, plus links to find the recording on Spotify and MusicBrainz. Free, no sign-up.",
 h1="ISRC checker and UPC/EAN validator",
 lead="Paste a code to see if it's valid and what it contains. An ISRC identifies one recording; a UPC or EAN identifies the whole release. A typo in either can block a release or send royalties to the wrong place.",
 cta="Get your audio and cover ready in StreamPack →",
 blocks=[("How an ISRC is built", ("ul", [
   "2 letters: country of the registrant (US, GB, IT…)", "3 characters: registrant code, given to the label or distributor",
   "2 digits: the year the code was assigned (not the release year)", "5 digits: the number of the recording",
   "12 characters in total; hyphens are only for reading, e.g. US-S1Z-25-00001"])),
  ("Where to get your codes", ["Most distributors (DistroKid, RouteNote, TuneCore, CD Baby, Amuse…) assign ISRCs and the UPC for free when you upload. If a recording is already out, reuse its ISRC: the same recording keeps the same code on every release."]),
  ("ISRC or UPC?", ["One recording = one ISRC, wherever it appears. One release = one UPC or EAN. A 5-track EP has one UPC and five ISRCs."])],
 faq=[("How do I check if an ISRC is valid?", "Paste it above: the checker verifies the length, the country letters, the registrant code, the year and the number. ISRCs have no check digit, so a valid format doesn't prove the code was registered: use the Spotify or MusicBrainz link to find the recording."),
  ("How do I check a UPC or EAN barcode?", "Paste the 12 (UPC) or 13 (EAN) digits. The last one is a check digit: if there's a typo, the checker tells you which digit it should be."),
  ("Can I reuse an ISRC for a remix or a new version?", "No. A remix, a remaster, a live version or a radio edit is a different recording and needs its own ISRC. The same recording released as a single and later on an album keeps its ISRC."),
  ("Is anything sent to a server?", "No. The check runs in your browser. The search links open Spotify or MusicBrainz only if you tap them.")],
 ui=dict(isrcL="ISRC", upcL="UPC / EAN barcode", isrcOk="Valid ISRC", isrcLen="An ISRC has 12 characters: country (2 letters), registrant (3), year (2), number (5)", isrcFmt="Invalid format. Example: US-S1Z-25-00001",
  upcOk="Valid {t} barcode", upcLen="Must be 12 digits (UPC) or 13 (EAN)", upcFmt="Digits only", upcChk="Wrong check digit: the last one should be {d}. Copy it again from your distributor.",
  country="Country", reg="Registrant", year="Year assigned", num="Recording number", find="Find the recording:", findRel="Find the release:", us="United States", intl="International (IFPI)", ctryWarn="Country code not recognised: check it with your distributor"))
P["isrc", "it"] = dict(
 title="Verifica ISRC e codice UPC/EAN – controllo gratis e immediato",
 desc="Controlla che un ISRC o un codice a barre UPC/EAN sia valido prima di pubblicare: formato, paese, anno e cifra di controllo, più i link per trovare la registrazione su Spotify e MusicBrainz. Gratis, senza registrazione.",
 h1="Verifica ISRC e codice UPC/EAN",
 lead="Incolla un codice per sapere se è valido e cosa contiene. L'ISRC identifica una registrazione; l'UPC o l'EAN identifica tutta la release. Un errore di battitura può bloccare l'uscita o mandare le royalty nel posto sbagliato.",
 cta="Prepara audio e copertina con StreamPack →",
 blocks=[("Com'è fatto un ISRC", ("ul", [
   "2 lettere: il paese di chi registra (IT, US, GB…)", "3 caratteri: il codice del registrante, assegnato all'etichetta o al distributore",
   "2 cifre: l'anno in cui è stato assegnato il codice (non l'anno di uscita)", "5 cifre: il numero della registrazione",
   "12 caratteri in tutto; i trattini servono solo a leggerlo, es. IT-A1B-25-00001"])),
  ("Dove prendere i codici", ["Quasi tutti i distributori (DistroKid, RouteNote, TuneCore, CD Baby, Amuse…) assegnano gratis ISRC e UPC quando carichi. Se una registrazione è già uscita, riusa il suo ISRC: la stessa registrazione mantiene lo stesso codice in ogni release."]),
  ("ISRC o UPC?", ["Una registrazione = un ISRC, ovunque compaia. Una release = un UPC o EAN. Un EP da 5 brani ha un UPC e cinque ISRC."])],
 faq=[("Come verifico se un ISRC è valido?", "Incollalo qui sopra: lo strumento controlla lunghezza, lettere del paese, codice registrante, anno e numero. L'ISRC non ha una cifra di controllo, quindi un formato valido non prova che il codice sia registrato: usa il link a Spotify o MusicBrainz per trovare la registrazione."),
  ("Come controllo un codice a barre UPC o EAN?", "Incolla le 12 (UPC) o 13 (EAN) cifre. L'ultima è una cifra di controllo: se c'è un errore di battitura, lo strumento ti dice quale dovrebbe essere."),
  ("Posso riusare un ISRC per un remix o una nuova versione?", "No. Remix, remaster, versione live o radio edit sono registrazioni diverse e vogliono un ISRC nuovo. La stessa registrazione uscita come singolo e poi nell'album mantiene il suo ISRC."),
  ("Viene inviato qualcosa a un server?", "No. Il controllo avviene nel browser. I link di ricerca aprono Spotify o MusicBrainz solo se li tocchi.")],
 ui=dict(isrcL="ISRC", upcL="Codice a barre UPC / EAN", isrcOk="ISRC valido", isrcLen="L'ISRC ha 12 caratteri: paese (2 lettere), codice registrante (3), anno (2), numero (5)", isrcFmt="Formato non valido. Esempio: IT-A1B-25-00001",
  upcOk="Codice {t} valido", upcLen="Servono 12 cifre (UPC) o 13 (EAN)", upcFmt="Solo cifre", upcChk="Cifra di controllo sbagliata: l'ultima dovrebbe essere {d}. Ricopialo dal distributore.",
  country="Paese", reg="Registrante", year="Anno del codice", num="Numero registrazione", find="Trova la registrazione:", findRel="Trova la release:", us="Stati Uniti", intl="Internazionale (IFPI)", ctryWarn="Codice paese non riconosciuto: verificalo con il distributore"))
P["isrc", "es"] = dict(
 title="Verificar ISRC y código UPC/EAN – comprobación gratis e inmediata",
 desc="Comprueba que un ISRC o un código de barras UPC/EAN es válido antes de publicar: formato, país, año y dígito de control, con enlaces para encontrar la grabación en Spotify y MusicBrainz. Gratis, sin registro.",
 h1="Verificar ISRC y código UPC/EAN",
 lead="Pega un código para saber si es válido y qué contiene. El ISRC identifica una grabación; el UPC o el EAN identifica todo el lanzamiento. Una errata puede bloquear el lanzamiento o mandar las regalías al sitio equivocado.",
 cta="Prepara audio y portada con StreamPack →",
 blocks=[("Cómo es un ISRC", ("ul", [
   "2 letras: el país de quien registra (ES, US, MX…)", "3 caracteres: el código del registrante, asignado al sello o a la distribuidora",
   "2 dígitos: el año en que se asignó el código (no el año de lanzamiento)", "5 dígitos: el número de la grabación",
   "12 caracteres en total; los guiones solo sirven para leerlo, p. ej. ES-A1B-25-00001"])),
  ("Dónde conseguir los códigos", ["Casi todas las distribuidoras (DistroKid, RouteNote, TuneCore, CD Baby, Amuse…) asignan gratis ISRC y UPC al subir la música. Si una grabación ya salió, reutiliza su ISRC: la misma grabación mantiene el mismo código en cada lanzamiento."]),
  ("¿ISRC o UPC?", ["Una grabación = un ISRC, aparezca donde aparezca. Un lanzamiento = un UPC o EAN. Un EP de 5 canciones tiene un UPC y cinco ISRC."])],
 faq=[("¿Cómo compruebo si un ISRC es válido?", "Pégalo arriba: la herramienta revisa la longitud, las letras del país, el código del registrante, el año y el número. El ISRC no tiene dígito de control, así que un formato válido no prueba que esté registrado: usa el enlace a Spotify o MusicBrainz para encontrar la grabación."),
  ("¿Cómo compruebo un código de barras UPC o EAN?", "Pega los 12 (UPC) o 13 (EAN) dígitos. El último es un dígito de control: si hay una errata, la herramienta te dice cuál debería ser."),
  ("¿Puedo reutilizar un ISRC para un remix o una nueva versión?", "No. Un remix, una remasterización, una versión en directo o un radio edit son grabaciones distintas y necesitan su propio ISRC. La misma grabación publicada como single y luego en el álbum conserva su ISRC."),
  ("¿Se envía algo a un servidor?", "No. La comprobación se hace en tu navegador. Los enlaces de búsqueda abren Spotify o MusicBrainz solo si los tocas.")],
 ui=dict(isrcL="ISRC", upcL="Código de barras UPC / EAN", isrcOk="ISRC válido", isrcLen="Un ISRC tiene 12 caracteres: país (2 letras), registrante (3), año (2), número (5)", isrcFmt="Formato no válido. Ejemplo: ES-A1B-25-00001",
  upcOk="Código {t} válido", upcLen="Debe tener 12 dígitos (UPC) o 13 (EAN)", upcFmt="Solo dígitos", upcChk="Dígito de control incorrecto: el último debería ser {d}. Cópialo de nuevo de tu distribuidora.",
  country="País", reg="Registrante", year="Año del código", num="Número de grabación", find="Encuentra la grabación:", findRel="Encuentra el lanzamiento:", us="Estados Unidos", intl="Internacional (IFPI)", ctryWarn="Código de país no reconocido: compruébalo con tu distribuidora"))
P["isrc", "de"] = dict(
 title="ISRC prüfen & UPC/EAN-Barcode validieren – kostenlos und sofort",
 desc="Prüf vor dem Release, ob ein ISRC oder ein UPC/EAN-Barcode gültig ist: Format, Land, Jahr und Prüfziffer, plus Links, um die Aufnahme auf Spotify und MusicBrainz zu finden. Kostenlos, ohne Anmeldung.",
 h1="ISRC prüfen und UPC/EAN validieren",
 lead="Füge einen Code ein und sieh, ob er gültig ist und was er enthält. Der ISRC kennzeichnet eine Aufnahme, der UPC oder EAN das ganze Release. Ein Tippfehler kann ein Release blockieren oder Tantiemen an die falsche Stelle schicken.",
 cta="Audio und Cover in StreamPack vorbereiten →",
 blocks=[("So ist ein ISRC aufgebaut", ("ul", [
   "2 Buchstaben: Land des Registranten (DE, AT, US…)", "3 Zeichen: Registrant-Code, vergeben an Label oder Vertrieb",
   "2 Ziffern: das Jahr, in dem der Code vergeben wurde (nicht das Release-Jahr)", "5 Ziffern: die Nummer der Aufnahme",
   "Insgesamt 12 Zeichen; Bindestriche dienen nur der Lesbarkeit, z. B. DE-A1B-25-00001"])),
  ("Woher du die Codes bekommst", ["Fast alle Vertriebe (DistroKid, RouteNote, TuneCore, CD Baby, Amuse…) vergeben ISRC und UPC beim Upload kostenlos. Ist eine Aufnahme schon erschienen, nutz ihren ISRC weiter: Dieselbe Aufnahme behält auf jedem Release denselben Code."]),
  ("ISRC oder UPC?", ["Eine Aufnahme = ein ISRC, egal wo sie erscheint. Ein Release = ein UPC oder EAN. Eine EP mit 5 Songs hat einen UPC und fünf ISRCs."])],
 faq=[("Wie prüfe ich, ob ein ISRC gültig ist?", "Füg ihn oben ein: Das Tool prüft Länge, Länderbuchstaben, Registrant-Code, Jahr und Nummer. ISRCs haben keine Prüfziffer, ein gültiges Format beweist also nicht, dass der Code registriert ist: Nutz den Link zu Spotify oder MusicBrainz, um die Aufnahme zu finden."),
  ("Wie prüfe ich einen UPC- oder EAN-Barcode?", "Füg die 12 (UPC) oder 13 (EAN) Ziffern ein. Die letzte ist eine Prüfziffer: Bei einem Tippfehler sagt dir das Tool, welche Ziffer es sein müsste."),
  ("Darf ich einen ISRC für einen Remix oder eine neue Version wiederverwenden?", "Nein. Remix, Remaster, Live-Version oder Radio Edit sind andere Aufnahmen und brauchen einen eigenen ISRC. Dieselbe Aufnahme als Single und später auf dem Album behält ihren ISRC."),
  ("Wird etwas an einen Server geschickt?", "Nein. Die Prüfung läuft im Browser. Die Suchlinks öffnen Spotify oder MusicBrainz nur, wenn du sie antippst.")],
 ui=dict(isrcL="ISRC", upcL="UPC / EAN-Barcode", isrcOk="Gültiger ISRC", isrcLen="Ein ISRC hat 12 Zeichen: Land (2 Buchstaben), Registrant (3), Jahr (2), Nummer (5)", isrcFmt="Ungültiges Format. Beispiel: DE-A1B-25-00001",
  upcOk="Gültiger {t}-Code", upcLen="Es braucht 12 Ziffern (UPC) oder 13 (EAN)", upcFmt="Nur Ziffern", upcChk="Falsche Prüfziffer: Die letzte sollte {d} sein. Kopiere den Code erneut vom Vertrieb.",
  country="Land", reg="Registrant", year="Vergabejahr", num="Aufnahme-Nummer", find="Aufnahme finden:", findRel="Release finden:", us="Vereinigte Staaten", intl="International (IFPI)", ctryWarn="Ländercode nicht erkannt: Prüf ihn mit deinem Vertrieb"))
P["isrc", "fr"] = dict(
 title="Vérifier un ISRC et un code UPC/EAN – contrôle gratuit et immédiat",
 desc="Vérifie qu'un ISRC ou un code-barres UPC/EAN est valide avant de publier : format, pays, année et chiffre de contrôle, avec des liens pour retrouver l'enregistrement sur Spotify et MusicBrainz. Gratuit, sans inscription.",
 h1="Vérifier un ISRC et un code UPC/EAN",
 lead="Colle un code pour savoir s'il est valide et ce qu'il contient. L'ISRC identifie un enregistrement ; l'UPC ou l'EAN identifie toute la sortie. Une faute de frappe peut bloquer une sortie ou envoyer les droits au mauvais endroit.",
 cta="Prépare l'audio et la pochette avec StreamPack →",
 blocks=[("Comment est fait un ISRC", ("ul", [
   "2 lettres : le pays du déclarant (FR, BE, CA…)", "3 caractères : le code du déclarant, attribué au label ou au distributeur",
   "2 chiffres : l'année d'attribution du code (pas l'année de sortie)", "5 chiffres : le numéro de l'enregistrement",
   "12 caractères au total ; les tirets servent seulement à la lecture, ex. FR-A1B-25-00001"])),
  ("Où obtenir tes codes", ["Presque tous les distributeurs (DistroKid, RouteNote, TuneCore, CD Baby, Amuse…) attribuent gratuitement les ISRC et l'UPC à l'envoi. Si un enregistrement est déjà sorti, réutilise son ISRC : le même enregistrement garde le même code sur chaque sortie."]),
  ("ISRC ou UPC ?", ["Un enregistrement = un ISRC, où qu'il apparaisse. Une sortie = un UPC ou EAN. Un EP de 5 titres a un UPC et cinq ISRC."])],
 faq=[("Comment vérifier si un ISRC est valide ?", "Colle-le ci-dessus : l'outil contrôle la longueur, les lettres du pays, le code du déclarant, l'année et le numéro. Un ISRC n'a pas de chiffre de contrôle, un format valide ne prouve donc pas que le code est enregistré : utilise le lien Spotify ou MusicBrainz pour retrouver l'enregistrement."),
  ("Comment vérifier un code-barres UPC ou EAN ?", "Colle les 12 (UPC) ou 13 (EAN) chiffres. Le dernier est un chiffre de contrôle : en cas de faute de frappe, l'outil t'indique lequel il devrait être."),
  ("Puis-je réutiliser un ISRC pour un remix ou une nouvelle version ?", "Non. Un remix, un remaster, une version live ou un radio edit est un autre enregistrement et demande son propre ISRC. Le même enregistrement sorti en single puis sur l'album garde son ISRC."),
  ("Quelque chose est-il envoyé à un serveur ?", "Non. Le contrôle se fait dans ton navigateur. Les liens de recherche n'ouvrent Spotify ou MusicBrainz que si tu les touches.")],
 ui=dict(isrcL="ISRC", upcL="Code-barres UPC / EAN", isrcOk="ISRC valide", isrcLen="Un ISRC a 12 caractères : pays (2 lettres), déclarant (3), année (2), numéro (5)", isrcFmt="Format non valide. Exemple : FR-A1B-25-00001",
  upcOk="Code {t} valide", upcLen="Il faut 12 chiffres (UPC) ou 13 (EAN)", upcFmt="Chiffres uniquement", upcChk="Chiffre de contrôle erroné : le dernier devrait être {d}. Recopie-le depuis ton distributeur.",
  country="Pays", reg="Déclarant", year="Année du code", num="Numéro d'enregistrement", find="Retrouver l'enregistrement :", findRel="Retrouver la sortie :", us="États-Unis", intl="International (IFPI)", ctryWarn="Code pays non reconnu : vérifie-le avec ton distributeur"))
P["isrc", "pt"] = dict(
 title="Verificar ISRC e código UPC/EAN – checagem grátis e imediata",
 desc="Confira se um ISRC ou um código de barras UPC/EAN é válido antes de lançar: formato, país, ano e dígito verificador, com links para achar a gravação no Spotify e no MusicBrainz. Grátis, sem cadastro.",
 h1="Verificar ISRC e código UPC/EAN",
 lead="Cole um código para saber se é válido e o que ele contém. O ISRC identifica uma gravação; o UPC ou EAN identifica o lançamento inteiro. Um erro de digitação pode travar o lançamento ou mandar os royalties para o lugar errado.",
 cta="Prepare áudio e capa no StreamPack →",
 blocks=[("Como é um ISRC", ("ul", [
   "2 letras: o país de quem registra (BR, PT, US…)", "3 caracteres: o código do registrante, dado à gravadora ou distribuidora",
   "2 dígitos: o ano em que o código foi atribuído (não o ano de lançamento)", "5 dígitos: o número da gravação",
   "12 caracteres no total; os hífens servem só para leitura, ex. BR-A1B-25-00001"])),
  ("Onde conseguir os códigos", ["Quase todas as distribuidoras (DistroKid, RouteNote, TuneCore, CD Baby, Amuse…) atribuem ISRC e UPC de graça no envio. Se a gravação já saiu, reutilize o ISRC dela: a mesma gravação mantém o mesmo código em todo lançamento."]),
  ("ISRC ou UPC?", ["Uma gravação = um ISRC, onde quer que apareça. Um lançamento = um UPC ou EAN. Um EP de 5 faixas tem um UPC e cinco ISRCs."])],
 faq=[("Como verifico se um ISRC é válido?", "Cole acima: a ferramenta confere o tamanho, as letras do país, o código do registrante, o ano e o número. O ISRC não tem dígito verificador, então um formato válido não prova que o código foi registrado: use o link do Spotify ou do MusicBrainz para achar a gravação."),
  ("Como confiro um código de barras UPC ou EAN?", "Cole os 12 (UPC) ou 13 (EAN) dígitos. O último é o dígito verificador: se houver erro de digitação, a ferramenta diz qual deveria ser."),
  ("Posso reutilizar um ISRC num remix ou numa nova versão?", "Não. Remix, remaster, versão ao vivo ou radio edit são gravações diferentes e precisam de ISRC próprio. A mesma gravação lançada como single e depois no álbum mantém o ISRC."),
  ("Algo é enviado para um servidor?", "Não. A checagem acontece no seu navegador. Os links de busca só abrem o Spotify ou o MusicBrainz se você tocar neles.")],
 ui=dict(isrcL="ISRC", upcL="Código de barras UPC / EAN", isrcOk="ISRC válido", isrcLen="Um ISRC tem 12 caracteres: país (2 letras), registrante (3), ano (2), número (5)", isrcFmt="Formato inválido. Exemplo: BR-A1B-25-00001",
  upcOk="Código {t} válido", upcLen="Precisa ter 12 dígitos (UPC) ou 13 (EAN)", upcFmt="Só dígitos", upcChk="Dígito verificador errado: o último deveria ser {d}. Copie de novo da distribuidora.",
  country="País", reg="Registrante", year="Ano do código", num="Número da gravação", find="Encontre a gravação:", findRel="Encontre o lançamento:", us="Estados Unidos", intl="Internacional (IFPI)", ctryWarn="Código de país não reconhecido: confira com a sua distribuidora"))

APRI = {"lufs": "go=audio&lufs=1", "isrc": "go=audio"}
url = lambda k, l: f"{SITO}/{CHECK[k][l][0]}/"


def tool(k, l, d):
    u = d["ui"]
    if k == "lufs":
        return (f'<label class="drop"><b>{e(u["pick"])}</b><small>{e(u["pickSub"])}</small>'
                f'<input id="f" type="file" accept="audio/*,video/mp4,.wav,.flac,.aif,.aiff,.mp3,.m4a,.aac,.ogg,.opus"></label><div id="res"></div>')
    ph_i = {"en": "US-S1Z-25-00001", "it": "IT-A1B-25-00001", "es": "ES-A1B-25-00001", "de": "DE-A1B-25-00001", "fr": "FR-A1B-25-00001", "pt": "BR-A1B-25-00001"}[l]
    return (f'<div class="card"><label for="isrc">{e(u["isrcL"])}</label><input id="isrc" class="codein" autocomplete="off" autocapitalize="characters" spellcheck="false" maxlength="24" placeholder="{ph_i}"><div id="res-isrc"></div>'
            f'<label for="upc" style="margin-top:16px">{e(u["upcL"])}</label><input id="upc" class="codein" inputmode="numeric" autocomplete="off" maxlength="20" placeholder="196871234567"><div id="res-upc"></div></div>')


def pagina(k, l):
    d, c = P[k, l], C[l]
    alt = "".join(f'<link rel="alternate" hreflang="{x}" href="{url(k, x)}">' for x in LINGUE) + f'<link rel="alternate" hreflang="x-default" href="{url(k, "en")}">'
    lingue = " ".join(f'<a href="/{CHECK[k][x][0]}/" hreflang="{x}" lang="{x}">{x.upper()}</a>' for x in LINGUE if x != l)
    apri = f"/?lang={l}&{APRI[k]}"
    ui = dict(d["ui"], fixUrl=apri, fix=d["cta"])
    corpo = [f"<h1>{e(d['h1'])}</h1>", f'<p class="lead">{e(d["lead"])}</p>', tool(k, l, d), f'<p class="msg">{e(c["free"])}</p>']
    for h, v in d["blocks"]:
        corpo.append(f"<h2>{e(h)}</h2>")
        if isinstance(v, tuple): corpo.append("<ul>" + "".join(f"<li>{e(x)}</li>" for x in v[1]) + "</ul>")
        else: corpo.extend(f"<p>{e(x)}</p>" for x in v)
    corpo.append("<h2>FAQ</h2>" + "".join(f"<h3>{e(q)}</h3><p>{e(a)}</p>" for q, a in d["faq"]))
    corpo.append(f'<div class="card cta"><p style="margin-top:0"><b>StreamPack</b> · {e(c["free"])}</p><a class="btn" href="{e(apri)}">{e(d["cta"])}</a></div>')
    altre = " · ".join([f'<a href="/{CHECK[x][l][0]}/">{e(CHECK[x][l][1])}</a>' for x in CHECK if x != k] + [f'<a href="/{SLUG[x][l]}/">{e(G[x, l]["nav"])}</a>' for x in SLUG])
    corpo.append(f"<h2>{e(c['other'])}</h2><p>{altre} · <a href=\"/convert/\">{e(c['conv'])}</a></p>")
    ld_app = {"@context": "https://schema.org", "@type": "WebApplication", "name": CHECK[k][l][1] + " – StreamPack", "url": url(k, l), "inLanguage": l,
              "description": d["desc"], "applicationCategory": "MultimediaApplication", "operatingSystem": "Any (browser, Android)", "browserRequirements": "Requires JavaScript",
              "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}}
    ld_faq = {"@context": "https://schema.org", "@type": "FAQPage", "inLanguage": l,
              "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in d["faq"]]}
    js = lambda o: json.dumps(o, ensure_ascii=False).replace("</", "<\\/")
    return f"""<!doctype html><html lang="{l}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(d["title"])}</title><meta name="description" content="{e(d["desc"])}"><link rel="canonical" href="{url(k, l)}">{alt}
<meta property="og:type" content="website"><meta property="og:url" content="{url(k, l)}"><meta property="og:title" content="{e(d["title"])}"><meta property="og:description" content="{e(d["desc"])}"><meta property="og:image" content="{SITO}/og-image.jpg">
<meta name="theme-color" content="#0B0A12"><link rel="icon" href="/icon-192.png"><link rel="stylesheet" href="/video/style.css">{CSS}
<script type="application/ld+json">{js(ld_app)}</script><script type="application/ld+json">{js(ld_faq)}</script>
<script src="/ext-links.js" defer></script></head><body><div class="w">
<nav><a href="/?lang={l}">StreamPack</a><small>{lingue}</small></nav>
{"".join(corpo)}
<footer><a href="/?lang={l}">StreamPack</a> · <a href="/privacy">Privacy</a><br>{e(c["foot"])}</footer></div>
<script type="application/json" id="ui">{js(ui)}</script><script src="/check.js"></script><script src="/checkers.js"></script></body></html>
"""


if __name__ == "__main__":
    for k in CHECK:
        for l in LINGUE:
            cart = os.path.join(ROOT, CHECK[k][l][0]); os.makedirs(cart, exist_ok=True)
            with open(os.path.join(cart, "index.html"), "w", encoding="utf-8") as f: f.write(pagina(k, l))
            print(url(k, l), len(P[k, l]["title"]), len(P[k, l]["desc"]))
