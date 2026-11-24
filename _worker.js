// StreamPack server: serves the app and generates AI covers with Cloudflare Workers AI.
// Costs: runs only on the Workers FREE plan (10,000 neurons/day). When the daily
// allowance is used up, Cloudflare returns an error and nothing is billed.
const PER_IP_PER_DAY = 4;

const json = (obj, status = 200) =>
  new Response(JSON.stringify(obj), { status, headers: { 'content-type': 'application/json', 'cache-control': 'no-store' } });

async function countToday(request, bucket = 'cover') {
  // Soft per-visitor limit using the edge cache (no database needed)
  const ip = request.headers.get('cf-connecting-ip') || 'x';
  const day = new Date().toISOString().slice(0, 10);
  const key = new Request(`https://limit.streampack/${bucket}/${day}/${encodeURIComponent(ip)}`);
  const cache = caches.default;
  const hit = await cache.match(key);
  const n = hit ? parseInt(await hit.text(), 10) || 0 : 0;
  return {
    n,
    async bump() {
      await cache.put(key, new Response(String(n + 1), { headers: { 'cache-control': 'max-age=90000' } }));
    },
  };
}

async function toEnglish(env, text) {
  try {
    const r = await env.AI.run('@cf/meta/llama-3.2-3b-instruct', {
      messages: [
        { role: 'system', content: 'Translate the user text to English for an image generator. Reply with the translation only, no quotes, no comments.' },
        { role: 'user', content: text },
      ],
      max_tokens: 120,
    });
    const out = (r && r.response || '').trim();
    return out || text;
  } catch (e) {
    return text;
  }
}

async function cover(request, env) {
  if (!env.AI) return json({ error: 'unavailable' }, 503);
  let body;
  try { body = await request.json(); } catch (e) { return json({ error: 'bad_request' }, 400); }
  const idea = String(body.prompt || '').trim().slice(0, 400);
  if (idea.length < 3) return json({ error: 'empty' }, 400);

  const limit = await countToday(request);
  if (limit.n >= PER_IP_PER_DAY) return json({ error: 'limit', left: 0 }, 429);

  const en = await toEnglish(env, idea);
  const prompt = `${en}. Square album cover artwork, professional, striking composition, high detail. No text, no letters, no words, no logos, no watermark.`;
  try {
    const r = await env.AI.run('@cf/black-forest-labs/flux-1-schnell', { prompt, steps: 6 });
    if (!r || !r.image) return json({ error: 'failed' }, 502);
    await limit.bump();
    return json({ image: r.image, left: PER_IP_PER_DAY - limit.n - 1 });
  } catch (e) {
    // Most likely the free daily allowance is used up
    return json({ error: 'busy' }, 503);
  }
}

const SCRIPT_PER_IP_PER_DAY = 10;
const TEXT_MODELS = [
  '@cf/meta/llama-3.3-70b-instruct-fp8-fast',
  '@cf/meta/llama-4-scout-17b-16e-instruct',
  '@cf/mistralai/mistral-small-3.1-24b-instruct',
  '@cf/google/gemma-3-12b-it',
  '@cf/meta/llama-3.2-3b-instruct',
];
async function chat(env, messages, max_tokens) {
  let last;
  for (const m of TEXT_MODELS) {
    try {
      const r = await env.AI.run(m, { messages, max_tokens });
      const out = (r && (r.response || (r.choices && r.choices[0] && r.choices[0].message && r.choices[0].message.content)) || '').toString().trim();
      if (out) return out;
    } catch (e) { last = e; }
  }
  throw last || new Error('no output');
}
const TOOLS = {
  shorts: (i) => [`You write scripts for YouTube Shorts, TikTok and Reels. Output in ${i.lang}. Format exactly:
HOOK (0-2s): one spoken line
SCRIPT: numbered lines to be spoken, each with [visual] in brackets
ON-SCREEN TEXT: 3-5 short overlays
CTA: one line
Length: about ${i.seconds} seconds of speech. No preamble.`, `Topic: ${i.topic}\nAudience: ${i.audience || 'general'}\nTone: ${i.tone || 'energetic'}`],
  hooks: (i) => [`You are a viral short-form video strategist. Output in ${i.lang}. Write 10 different opening hooks (max 12 words each) for a video, numbered, each labeled with its technique in parentheses (curiosity gap, bold claim, question, pattern interrupt, story, number, warning...). No preamble.`, `Video topic: ${i.topic}\nAudience: ${i.audience || 'general'}\nTone: ${i.tone || 'any'}`],
  ideas: (i) => [`You are a YouTube strategist for faceless channels. Output in ${i.lang}. Give 10 video ideas for the niche, numbered. For each: a clickable title (max 60 chars), a one-line angle, and the format (Short or long). No preamble.`, `Niche: ${i.topic}\nAudience: ${i.audience || 'general'}\nTone: ${i.tone || 'any'}`],
  titles: (i) => [`You are a YouTube SEO and packaging expert. Output in ${i.lang}. Write 10 different titles for one YouTube video, numbered "1." to "10.", one title per line. Rules: each title under 70 characters; put the main keyword near the start when one is given; be specific and honest (no clickbait the video cannot deliver); vary the angle across curiosity, number/list, how-to, result/transformation, mistake/warning, comparison, question. After each title add the angle in square brackets, e.g. [how-to]. No emojis unless the tone asks for them, no hashtags, no preamble, no notes.`, `Video topic: ${i.topic}\nMain keyword: ${i.audience || 'none'}\nTone: ${i.tone || 'clear and clickable'}`],
  descriptions: (i) => [`You are a YouTube SEO copywriter. Output in ${i.lang}. Write ONE ready-to-paste YouTube video description. Structure:
1) First 2 lines (max 150 characters total): what the viewer gets, with the main keyword in the first sentence when one is given. These lines show in search, so make them count.
2) A blank line, then 2 short paragraphs (60-120 words total) explaining what the video covers, using the keyword and 1-2 natural related phrases once each. No keyword stuffing.
3) A blank line, then "In this video:" followed by 3-5 bullet points starting with "- ".
4) A blank line, then one call to action line (subscribe or comment question).
5) A blank line, then exactly 3 relevant hashtags on one line.
Be specific and honest; do not invent facts, prices, links, timestamps, names or statistics that were not given. Write [LINK] where a link would go. No preamble, no notes, no markdown headings or bold.`, `Video topic: ${i.topic}\nMain keyword: ${i.audience || 'none'}\nTone: ${i.tone || 'friendly and clear'}`],
  prompts: (i) => [`You write prompts for AI video models (Sora, Veo, Kling, Runway). Output in English. Write 5 alternative prompts for the scene, numbered. Each prompt: subject and action, setting, camera movement, lens/shot type, lighting, mood, style, duration hint. 40-70 words each. No preamble.`, `Scene idea: ${i.topic}\nStyle: ${i.tone || 'cinematic'}\nAspect: ${i.audience || '9:16 vertical'}`],
};
async function tool(request, env) {
  if (!env.AI) return json({ error: 'unavailable' }, 503);
  let b;
  try { b = await request.json(); } catch (e) { return json({ error: 'bad_request' }, 400); }
  const make = TOOLS[b.tool];
  const clip = (v, n) => String(v || '').trim().slice(0, n);
  const i = { topic: clip(b.topic, 300), audience: clip(b.audience, 80), tone: clip(b.tone, 60),
    seconds: [15, 30, 45, 60].includes(+b.seconds) ? +b.seconds : 30, lang: clip(b.lang, 30) || 'English' };
  if (!make || i.topic.length < 3) return json({ error: 'empty' }, 400);
  const limit = await countToday(request, 'tool');
  if (limit.n >= 15) return json({ error: 'limit', left: 0 }, 429);
  const [sys, user] = make(i);
  try {
    const out = await chat(env, [{ role: 'system', content: sys }, { role: 'user', content: user }], 900);
    await limit.bump();
    return json({ text: out, left: 15 - limit.n - 1 });
  } catch (e) {
    return json({ error: 'busy' }, 503);
  }
}
async function script(request, env) {
  if (!env.AI) return json({ error: 'unavailable' }, 503);
  let b;
  try { b = await request.json(); } catch (e) { return json({ error: 'bad_request' }, 400); }
  const clip = (v, n) => String(v || '').trim().slice(0, n);
  const title = clip(b.title, 80), genre = clip(b.genre, 40), mood = clip(b.mood, 80), about = clip(b.about, 300);
  const platform = ['tiktok', 'reels', 'shorts', 'youtube'].includes(b.platform) ? b.platform : 'reels';
  const lang = b.lang === 'it' ? 'Italian' : 'English';
  if (!title) return json({ error: 'empty' }, 400);
  const limit = await countToday(request, 'script');
  if (limit.n >= SCRIPT_PER_IP_PER_DAY) return json({ error: 'limit', left: 0 }, 429);
  const len = platform === 'youtube' ? '45-60 seconds' : '15-30 seconds';
  const sys = `You are a music marketing video director. Write a promo video script for an independent artist's song, in ${lang}. Format exactly:
HOOK (first 2 seconds): one line of on-screen text
SCENES: 4 to 6 numbered scenes, each with: visual description, on-screen text (max 8 words), seconds
CAPTION: a social caption with 3-5 hashtags
CALL TO ACTION: one line
Keep it ${len} total, vertical 9:16 unless YouTube. No preamble, no comments.`;
  const user = `Song title: ${title}\nGenre: ${genre || 'n/a'}\nMood: ${mood || 'n/a'}\nWhat the song is about: ${about || 'n/a'}\nPlatform: ${platform}`;
  try {
    const out = await chat(env, [{ role: 'system', content: sys }, { role: 'user', content: user }], 700);
    if (!out) return json({ error: 'failed' }, 502);
    await limit.bump();
    return json({ script: out, left: SCRIPT_PER_IP_PER_DAY - limit.n - 1 });
  } catch (e) {
    return json({ error: 'busy' }, 503);
  }
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname.startsWith('/google13bcbada3e5e0f65')) return new Response('google-site-verification: google13bcbada3e5e0f65.html', { headers: { 'content-type': 'text/html; charset=utf-8' } });
    if (url.pathname === '/api/cover' && request.method === 'POST') return cover(request, env);
    if (url.pathname === '/api/script' && request.method === 'POST') return script(request, env);
    if (url.pathname === '/api/tool' && request.method === 'POST') return tool(request, env);
    return env.ASSETS.fetch(request);
  },
};
