// Системные тесты «чёрного ящика» на рабочем стенде https://translark.ru. Запуск: node system.test.mjs
import { writeFileSync } from 'node:fs';
const BASE = 'https://translark.ru';
const results = [];
async function t(id, name, fn) {
  const t0 = performance.now();
  try {
    const note = await fn();
    results.push({ id, name, ok: true, ms: Math.round(performance.now() - t0), note: note ?? '' });
  } catch (e) {
    results.push({ id, name, ok: false, ms: Math.round(performance.now() - t0), note: String(e.message ?? e) });
  }
}
const assert = (c, m) => { if (!c) throw new Error(m); };
const post = (path, body, headers = {}) => fetch(BASE + path, { method: 'POST', headers: { 'content-type': 'application/json', ...headers }, body: JSON.stringify(body) });

await t('C-01', 'Доступность API: GET /api/health', async () => {
  const r = await fetch(BASE + '/api/health'); const j = await r.json();
  assert(r.status === 200 && j.status === 'ok', `статус ${r.status}`);
  return `200, status=ok`;
});
for (const [id, p] of [['C-02', '/'], ['C-03', '/about'], ['C-04', '/privacy'], ['C-05', '/phrases']]) {
  await t(id, `SSR-страница ${p} отдаётся с HTML`, async () => {
    const r = await fetch(BASE + p); const h = await r.text();
    assert(r.status === 200, `статус ${r.status}`);
    assert(/<html[^>]*lang=/.test(h), 'нет <html lang>');
    assert(h.includes('__APP_STATE__'), 'нет сериализованного состояния');
    return `200, ${Math.round(h.length / 1024)} КБ`;
  });
}
await t('C-06', 'Несуществующая страница — 404', async () => {
  const r = await fetch(BASE + '/no-such-page-' + Date.now());
  assert(r.status === 404, `статус ${r.status}`); return '404';
});
await t('C-07', 'HTTP перенаправляется на HTTPS', async () => {
  const r = await fetch('http://translark.ru/', { redirect: 'manual' });
  assert([301, 302, 307, 308].includes(r.status), `статус ${r.status}`);
  assert((r.headers.get('location') ?? '').startsWith('https://'), 'нет https в Location');
  return `${r.status} → ${r.headers.get('location')}`;
});
await t('C-08', 'Перевод без SID отклоняется (401)', async () => {
  const r = await post('/api/translate', { text: 'hello', source: 'en', target: 'ru' });
  assert(r.status === 401, `статус ${r.status}`); return '401';
});
await t('C-09', 'Перевод с поддельным SID отклоняется (401)', async () => {
  const r = await post('/api/translate', { text: 'hello', source: 'en', target: 'ru' }, { 'x-sid': 'AAAA.BBBB' });
  assert(r.status === 401, `статус ${r.status}`); return '401';
});
let sid = '';
await t('C-10', 'Выдача SID: GET /api/sid', async () => {
  const r = await fetch(BASE + '/api/sid'); const j = await r.json();
  assert(r.status === 200 && typeof j.sid === 'string' && j.sid.includes('.'), `статус ${r.status}`);
  sid = j.sid; return `200, длина токена ${j.sid.length}`;
});
await t('C-11', 'SID без капчи не пускает к моделям (403 captcha_required)', async () => {
  const r = await post('/api/translate', { text: 'hello', source: 'en', target: 'ru' }, { 'x-sid': sid });
  const j = await r.json().catch(() => ({}));
  assert(r.status === 403 && j.code === 'captcha_required', `статус ${r.status}`); return '403 captcha_required';
});
await t('C-12', 'Ограничение частоты выдачи SID (429 при всплеске)', async () => {
  const codes = [];
  for (let i = 0; i < 15; i++) codes.push((await fetch(BASE + '/api/sid')).status);
  assert(codes.includes(429), 'нет 429: ' + codes.join(','));
  return `первый 429 на запросе № ${codes.indexOf(429) + 1}`;
});
await t('C-13', 'Время ответа /api/health (20 запросов): p95 < 500 мс', async () => {
  const ms = [];
  for (let i = 0; i < 20; i++) { const a = performance.now(); await fetch(BASE + '/api/health'); ms.push(performance.now() - a); }
  ms.sort((a, b) => a - b);
  const p95 = Math.round(ms[Math.floor(ms.length * 0.95) - 1]); const med = Math.round(ms[10]);
  assert(p95 < 500, 'p95=' + p95); return `медиана ${med} мс, p95 ${p95} мс`;
});
await t('C-14', 'Время загрузки главной страницы < 2 с', async () => {
  const a = performance.now(); const r = await fetch(BASE + '/'); await r.text();
  const ms = Math.round(performance.now() - a); assert(ms < 2000, ms + ' мс'); return `${ms} мс`;
});
await t('C-15', 'robots.txt доступен', async () => {
  const r = await fetch(BASE + '/robots.txt'); assert(r.status === 200, `статус ${r.status}`); return '200';
});

const stamp = new Date().toISOString();
writeFileSync(new URL('./system-results.json', import.meta.url), JSON.stringify({ stamp, base: BASE, results }, null, 2));
for (const r of results) console.log(`${r.ok ? 'PASS' : 'FAIL'} ${r.id} ${r.name} — ${r.note} (${r.ms} мс)`);
console.log(`итого: ${results.filter((r) => r.ok).length}/${results.length} · ${stamp}`);
