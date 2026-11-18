// Fields in the same order as each distributor's upload form.
// The panel only copies to the clipboard: it never touches the distributor's page,
// so it stays within their terms (no scripts, no overlays on their site).
// value(p) for release fields, value(p, t) for per-track fields.
const yesNo = (b, it) => (b ? (it ? 'Sì' : 'Yes') : 'No');
const writers = (t) => t.songwriters.map((w) => `${w.first} ${w.last}`.trim()).filter(Boolean).join(', ');
const cline = (p) => (p.copyrightYear && p.copyrightOwner ? `${p.copyrightYear} ${p.copyrightOwner}` : '');

window.DISTRIBUTORS = {
  distrokid: {
    name: 'DistroKid', url: 'https://distrokid.com/new/',
    release: [
      ['artist', 'Artist / band name', (p) => p.artist],
      ['releaseTitle', 'Album title', (p) => (p.type === 'single' ? '' : p.releaseTitle)],
      ['releaseDate', 'Release date', (p) => p.releaseDate],
      ['label', 'Record label', (p) => p.label],
      ['primaryGenre', 'Primary genre', (p) => p.primaryGenre],
      ['secondaryGenre', 'Secondary genre', (p) => p.secondaryGenre],
      ['language', 'Language', (p) => p.language],
      ['cover', 'Album art', () => '', 'file'],
    ],
    track: [
      ['title', 'Song title', (p, t) => t.title],
      ['version', 'Version / remix', (p, t) => t.version],
      ['featuring', 'Featured artist', (p, t) => t.featuring],
      ['writers', 'Songwriter real name', (p, t) => writers(t)],
      ['explicit', 'Explicit lyrics', (p, t, it) => yesNo(t.explicit, it), 'choice'],
      ['instrumental', 'Instrumental', (p, t, it) => yesNo(t.instrumental, it), 'choice'],
      ['isrc', 'ISRC', (p, t) => t.isrc],
      ['previewStart', 'TikTok preview start', (p, t) => t.previewStart],
      ['audio', 'Audio file', () => '', 'file'],
    ],
  },
  routenote: {
    name: 'RouteNote', url: 'https://routenote.com/',
    release: [
      ['releaseTitle', 'Release title', (p) => p.releaseTitle || (p.tracks[0] || {}).title],
      ['artist', 'Primary artist', (p) => p.artist],
      ['type', 'Release type', (p) => ({ single: 'Single', ep: 'EP', album: 'Album' }[p.type])],
      ['primaryGenre', 'Primary genre', (p) => p.primaryGenre],
      ['secondaryGenre', 'Secondary genre', (p) => p.secondaryGenre],
      ['language', 'Language', (p) => p.language],
      ['label', 'Label', (p) => p.label || p.artist],
      ['cline', '© / ℗ line', cline],
      ['releaseDate', 'Release date', (p) => p.releaseDate],
      ['cover', 'Artwork', () => '', 'file'],
    ],
    track: [
      ['title', 'Track title', (p, t) => t.title],
      ['version', 'Version', (p, t) => t.version],
      ['featuring', 'Featured artist', (p, t) => t.featuring],
      ['writers', 'Composer', (p, t) => writers(t)],
      ['producers', 'Producer', (p, t) => t.producers],
      ['explicit', 'Explicit', (p, t, it) => yesNo(t.explicit, it), 'choice'],
      ['isrc', 'ISRC', (p, t) => t.isrc],
      ['lyrics', 'Lyrics', (p, t) => t.lyrics],
      ['audio', 'Audio file', () => '', 'file'],
    ],
  },
  tunecore: {
    name: 'TuneCore', url: 'https://www.tunecore.com/',
    release: [
      ['releaseTitle', 'Release title', (p) => p.releaseTitle || (p.tracks[0] || {}).title],
      ['artist', 'Main artist', (p) => p.artist],
      ['primaryGenre', 'Primary genre', (p) => p.primaryGenre],
      ['secondaryGenre', 'Secondary genre', (p) => p.secondaryGenre],
      ['language', 'Language', (p) => p.language],
      ['releaseDate', 'Release date', (p) => p.releaseDate],
      ['label', 'Label', (p) => p.label],
      ['cline', 'Copyright', cline],
      ['cover', 'Artwork', () => '', 'file'],
    ],
    track: [
      ['title', 'Song title', (p, t) => t.title],
      ['featuring', 'Featured artist', (p, t) => t.featuring],
      ['writers', 'Songwriter', (p, t) => writers(t)],
      ['explicit', 'Explicit', (p, t, it) => yesNo(t.explicit, it), 'choice'],
      ['isrc', 'ISRC', (p, t) => t.isrc],
      ['audio', 'Audio file', () => '', 'file'],
    ],
  },
  cdbaby: {
    name: 'CD Baby', url: 'https://cdbaby.com/',
    release: [
      ['artist', 'Artist name', (p) => p.artist],
      ['releaseTitle', 'Album / single title', (p) => p.releaseTitle || (p.tracks[0] || {}).title],
      ['releaseDate', 'Release date', (p) => p.releaseDate],
      ['primaryGenre', 'Primary genre', (p) => p.primaryGenre],
      ['secondaryGenre', 'Secondary genre', (p) => p.secondaryGenre],
      ['language', 'Language', (p) => p.language],
      ['label', 'Record label', (p) => p.label],
      ['cline', 'Copyright', cline],
      ['cover', 'Album artwork', () => '', 'file'],
    ],
    track: [
      ['title', 'Track title', (p, t) => t.title],
      ['featuring', 'Featured artist', (p, t) => t.featuring],
      ['writers', 'Songwriters', (p, t) => writers(t)],
      ['producers', 'Producer', (p, t) => t.producers],
      ['explicit', 'Explicit', (p, t, it) => yesNo(t.explicit, it), 'choice'],
      ['lyrics', 'Lyrics', (p, t) => t.lyrics],
      ['audio', 'Audio file', () => '', 'file'],
    ],
  },
};
