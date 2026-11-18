// DistroKid adapter: maps release-package fields to the upload form.
// Fields are found by their visible label (or aria-label / placeholder / name),
// so small layout changes do not break it. Anything not found can be pointed
// out once with "Indica il campo" and is remembered per site.
// `value` reads from the package: (pkg) for release fields, (pkg, track, i) for track fields.
window.RC_ADAPTERS = window.RC_ADAPTERS || {};
window.RC_ADAPTERS.distrokid = {
  name: 'DistroKid',
  host: /(^|\.)distrokid\.com$/,
  release: [
    { key: 'artist', label: 'Artist / band name', kind: 'text', match: [/artist.*(name|band)|band name|^artist$/i], value: (p) => p.artist },
    { key: 'releaseTitle', label: 'Album title', kind: 'text', match: [/album title|release title|^title of (the )?(album|release)/i], value: (p) => p.type === 'single' ? '' : p.releaseTitle, skipIfEmpty: true },
    { key: 'releaseDate', label: 'Release date', kind: 'date', match: [/release date/i], value: (p) => p.releaseDate },
    { key: 'label', label: 'Record label', kind: 'text', match: [/record label|^label$/i], value: (p) => p.label, skipIfEmpty: true },
    { key: 'primaryGenre', label: 'Primary genre', kind: 'select', match: [/primary genre|^genre$/i], value: (p) => p.primaryGenre },
    { key: 'secondaryGenre', label: 'Secondary genre', kind: 'select', match: [/secondary genre/i], value: (p) => p.secondaryGenre },
    { key: 'language', label: 'Language', kind: 'select', match: [/language/i], value: (p) => p.language },
    { key: 'cover', label: 'Album art', kind: 'file', accept: /image/, match: [/album art|cover art|artwork/i], value: (p) => 'cover' },
  ],
  track: [
    { key: 'title', label: 'Song title', kind: 'text', match: [/song title|track.*title|^title$/i], value: (p, t) => t.title },
    { key: 'version', label: 'Version / remix', kind: 'text', match: [/version|remix/i], value: (p, t) => t.version, skipIfEmpty: true },
    { key: 'featuring', label: 'Featured artist', kind: 'text', match: [/featur/i], value: (p, t) => t.featuring, skipIfEmpty: true },
    { key: 'writerFirst', label: 'Songwriter first name', kind: 'text', match: [/(songwriter|composer).*first|first name/i], value: (p, t) => (t.songwriters[0] || {}).first },
    { key: 'writerLast', label: 'Songwriter last name', kind: 'text', match: [/(songwriter|composer).*last|last name|surname/i], value: (p, t) => (t.songwriters[0] || {}).last },
    { key: 'explicit', label: 'Explicit lyrics', kind: 'choice', match: [/explicit/i], value: (p, t) => (t.explicit ? 'yes' : 'no') },
    { key: 'instrumental', label: 'Instrumental', kind: 'choice', match: [/instrumental/i], value: (p, t) => (t.instrumental ? 'yes' : 'no') },
    { key: 'isrc', label: 'ISRC', kind: 'text', match: [/isrc/i], value: (p, t) => t.isrc, skipIfEmpty: true },
    { key: 'previewStart', label: 'Preview start (TikTok)', kind: 'text', match: [/preview|clip start|tiktok/i], value: (p, t) => t.previewStart, skipIfEmpty: true },
    { key: 'audio', label: 'Audio file', kind: 'file', accept: /audio|\.wav|\.flac|\.mp3/, match: [/audio|song file|upload.*(track|song)/i], value: (p, t, i) => 'audio:' + i },
  ],
};
