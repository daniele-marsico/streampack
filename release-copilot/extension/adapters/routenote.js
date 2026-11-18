// RouteNote adapter: same idea as DistroKid, different labels.
window.RC_ADAPTERS = window.RC_ADAPTERS || {};
window.RC_ADAPTERS.routenote = {
  name: 'RouteNote',
  host: /(^|\.)routenote\.com$/,
  release: [
    { key: 'releaseTitle', label: 'Release title', kind: 'text', match: [/release title|album title|^title$/i], value: (p) => p.releaseTitle || (p.tracks[0] || {}).title },
    { key: 'artist', label: 'Primary artist', kind: 'text', match: [/primary artist|artist name|^artist$/i], value: (p) => p.artist },
    { key: 'releaseType', label: 'Release type', kind: 'select', match: [/release type|format|^type$/i], value: (p) => ({ single: 'Single', ep: 'EP', album: 'Album' }[p.type]) },
    { key: 'releaseDate', label: 'Release date', kind: 'date', match: [/release date|sales start/i], value: (p) => p.releaseDate },
    { key: 'label', label: 'Label', kind: 'text', match: [/label/i], value: (p) => p.label, skipIfEmpty: true },
    { key: 'primaryGenre', label: 'Primary genre', kind: 'select', match: [/primary genre|^genre$/i], value: (p) => p.primaryGenre },
    { key: 'secondaryGenre', label: 'Secondary genre', kind: 'select', match: [/secondary genre|sub.?genre/i], value: (p) => p.secondaryGenre },
    { key: 'language', label: 'Language', kind: 'select', match: [/(metadata|title|lyrics)? ?language/i], value: (p) => p.language },
    { key: 'cLine', label: '© line', kind: 'text', match: [/copyright|c line|℗|©/i], value: (p) => p.copyrightYear && p.copyrightOwner ? `${p.copyrightYear} ${p.copyrightOwner}` : '' , skipIfEmpty: true },
    { key: 'upc', label: 'UPC', kind: 'text', match: [/upc|barcode|ean/i], value: (p) => p.upc, skipIfEmpty: true },
    { key: 'cover', label: 'Artwork', kind: 'file', accept: /image/, match: [/artwork|cover/i], value: () => 'cover' },
  ],
  track: [
    { key: 'title', label: 'Track title', kind: 'text', match: [/track title|song title|^title$/i], value: (p, t) => t.title },
    { key: 'version', label: 'Version', kind: 'text', match: [/version|mix/i], value: (p, t) => t.version, skipIfEmpty: true },
    { key: 'featuring', label: 'Featured artist', kind: 'text', match: [/featur/i], value: (p, t) => t.featuring, skipIfEmpty: true },
    { key: 'composer', label: 'Composer / songwriter', kind: 'text', match: [/composer|songwriter|writer/i], value: (p, t) => t.songwriters.map((w) => `${w.first} ${w.last}`.trim()).filter(Boolean).join(', ') },
    { key: 'producer', label: 'Producer', kind: 'text', match: [/producer/i], value: (p, t) => t.producers, skipIfEmpty: true },
    { key: 'explicit', label: 'Explicit', kind: 'choice', match: [/explicit|parental/i], value: (p, t) => (t.explicit ? 'yes' : 'no') },
    { key: 'isrc', label: 'ISRC', kind: 'text', match: [/isrc/i], value: (p, t) => t.isrc, skipIfEmpty: true },
    { key: 'lyrics', label: 'Lyrics', kind: 'text', match: [/lyrics/i], value: (p, t) => t.lyrics, skipIfEmpty: true },
    { key: 'audio', label: 'Audio file', kind: 'file', accept: /audio|\.wav|\.flac/, match: [/audio|upload.*track|track file/i], value: (p, t, i) => 'audio:' + i },
  ],
};
