// StreamPack server: serves the app and generates AI covers with Cloudflare Workers AI.
// Costs: runs only on the Workers FREE plan (10,000 neurons/day). When the daily
// allowance is used up, Cloudflare returns an error and nothing is billed.
const PER_IP_PER_DAY = 4;

const json = (obj, status = 200) =>
  new Response(JSON.stringify(obj), { status, headers: { 'content-type': 'application/json', 'cache-control': 'no-store' } });

async function countToday(request) {
  // Soft per-visitor limit using the edge cache (no database needed)
  const ip = request.headers.get('cf-connecting-ip') || 'x';
  const day = new Date().toISOString().slice(0, 10);
  const key = new Request(`https://limit.streampack/${day}/${encodeURIComponent(ip)}`);
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

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === '/api/cover' && request.method === 'POST') return cover(request, env);
    return env.ASSETS.fetch(request);
  },
};
