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
    const r = await env.AI.run('@cf/meta/llama-3.1-8b-instruct', {
      messages: [{ role: 'system', content: sys }, { role: 'user', content: user }],
      max_tokens: 700,
    });
    const out = (r && r.response || '').trim();
    if (!out) return json({ error: 'failed' }, 502);
    await limit.bump();
    return json({ script: out, left: SCRIPT_PER_IP_PER_DAY - limit.n - 1 });
  } catch (e) {
    return json({ error: 'busy', detail: String(e && e.message || e).slice(0, 200) }, 503);
  }
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === '/api/cover' && request.method === 'POST') return cover(request, env);
    if (url.pathname === '/api/script' && request.method === 'POST') return script(request, env);
    return env.ASSETS.fetch(request);
  },
};
