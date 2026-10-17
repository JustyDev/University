// Модульные тесты TransLark (backend, скомпилированный в tl-dist). Запуск: node --test
const test = require('node:test');
const assert = require('node:assert/strict');
const path = require('node:path');
const { createHmac } = require('node:crypto');
require(path.join(__dirname, '..', 'tl-dist', 'node_modules_shim.js'));
const D = (p) => require(path.join(__dirname, '..', 'tl-dist', p));

const { RoutingService } = D('modules/routing/routing.service.js');
const { LANGUAGE_CODES, isLanguage } = D('modules/languages/languages.js');
const { verifySid, ipHash } = D('modules/auth/sid.util.js');
const { BucketStore, RateLimitService } = D('modules/auth/rate-limit.service.js');
const { TransliterateService } = D('modules/transliterate/transliterate.service.js');

// --- Подсистема 2. Маршрутизация (Floyd–Warshall) ---
test('M-01 маршрут для одинаковых языков — один узел, качество 1', () => {
  const r = new RoutingService();
  assert.deepEqual(r.getRoute('ru', 'ru'), { hops: ['ru'], quality: 1 });
});
test('M-02 маршрут ru→en существует, начинается с ru и заканчивается en', () => {
  const r = new RoutingService().getRoute('ru', 'en');
  assert.ok(r); assert.equal(r.hops[0], 'ru'); assert.equal(r.hops.at(-1), 'en');
});
test('M-03 все маршруты реестра не длиннее 3 переходов, качество в (0; 1]', () => {
  const svc = new RoutingService();
  let n = 0;
  for (const s of LANGUAGE_CODES) for (const t of LANGUAGE_CODES) {
    if (s === t) continue;
    const r = svc.getRoute(s, t);
    if (!r) continue;
    n++;
    assert.ok(r.hops.length - 1 <= 3, `${s}>${t}`);
    assert.ok(r.quality > 0 && r.quality <= 1, `${s}>${t}`);
  }
  assert.ok(n > 1000, 'маршрутов меньше ожидаемого: ' + n);
});
test('M-04 слабое прямое ребро заменяется пивотом с большим сквозным качеством', () => {
  const svc = new RoutingService();
  svc.setEdges([
    { source: 'aa', target: 'cc', provider: 'weak', quality: 0.3, enabled: true },
    { source: 'aa', target: 'bb', provider: 'strong', quality: 0.9, enabled: true },
    { source: 'bb', target: 'cc', provider: 'strong', quality: 0.9, enabled: true },
  ]);
  const r = svc.getRoute('aa', 'cc');
  assert.deepEqual(r.hops, ['aa', 'bb', 'cc']);
  assert.ok(Math.abs(r.quality - 0.81) < 1e-9);
});
test('M-05 отключённое ребро не участвует в маршрутах', () => {
  const svc = new RoutingService();
  svc.setEdges([{ source: 'aa', target: 'bb', provider: 'x', quality: 0.9, enabled: false }]);
  assert.equal(svc.getRoute('aa', 'bb'), null);
});
test('M-06 реестр содержит 247 языков, проверка кода языка', () => {
  assert.equal(LANGUAGE_CODES.length, 247);
  assert.equal(isLanguage('ru'), true);
  assert.equal(isLanguage('xx'), false);
});

// --- Подсистема 6. Доступ и безопасность ---
const secret = process.env.TRANSLARK_SID_SECRET ?? 'translark-dev-secret';
const mk = (exp, iph, flag) => {
  const payload = Buffer.from([exp, 'nonce', iph, ...(flag ? [flag] : [])].join(':')).toString('base64url');
  return payload + '.' + createHmac('sha256', secret).update(payload).digest('base64url');
};
test('S-01 валидный SID принимается, привязка к IP сохраняется', () => {
  const info = verifySid(mk(Date.now() + 60_000, ipHash('10.0.0.1')));
  assert.ok(info); assert.equal(info.ipHash, ipHash('10.0.0.1')); assert.equal(info.verified, false);
});
test('S-02 SID с флагом капчи помечается как подтверждённый', () => {
  assert.equal(verifySid(mk(Date.now() + 60_000, 'h', 'c')).verified, true);
});
test('S-03 подделанная подпись отклоняется', () => {
  const t = mk(Date.now() + 60_000, 'h');
  assert.equal(verifySid(t.slice(0, -2) + (t.endsWith('AA') ? 'BB' : 'AA')), null);
});
test('S-04 просроченный SID отклоняется', () => {
  assert.equal(verifySid(mk(Date.now() - 1, 'h')), null);
});
test('S-05 строка без подписи отклоняется', () => {
  assert.equal(verifySid('garbage'), null);
});
test('S-06 токен-бакет: ёмкость 3 — четвёртый запрос отклонён, через 1 с пополнен', () => {
  const b = new BucketStore({ capacity: 3, refillPerSec: 1 });
  const t0 = 1_000_000;
  assert.deepEqual([b.take('k', t0), b.take('k', t0), b.take('k', t0), b.take('k', t0)], [true, true, true, false]);
  assert.equal(b.take('k', t0 + 1000), true);
});
test('S-07 лимитер: всплеск запросов с одного IP получает отказ rate', () => {
  const rl = new RateLimitService();
  const res = Array.from({ length: 60 }, () => rl.check('sid-1', '1.2.3.4'));
  assert.equal(res[0], 'ok');
  assert.ok(res.includes('rate') || res.includes('banned'));
});
test('S-08 лимитер: доверенный запрос не ограничивается по IP', () => {
  const rl = new RateLimitService();
  const res = Array.from({ length: 30 }, (_, i) => rl.check('sid-' + i, '5.6.7.8', true));
  assert.ok(res.every((r) => r === 'ok'));
});
test('S-09 лимитер: после серии нарушений IP блокируется (banned)', () => {
  const rl = new RateLimitService();
  let last;
  for (let i = 0; i < 200; i++) last = rl.check('sid-x', '9.9.9.9');
  assert.equal(last, 'banned');
});

// --- Подсистема 3. Обогащение: транслитерация (без обращения к LLM) ---
const tr = new TransliterateService({ chat: async () => { throw new Error('LLM не должен вызываться'); } });
test('T-01 кириллица ru транслитерируется таблицей в латиницу', async () => {
  const { text } = await tr.transliterate({ text: 'Привет, мир', lang: 'ru' });
  assert.match(text, /^[\x20-\x7EÀ-ɏ]+$/); assert.ok(text.length > 0);
});
test('T-02 китайский — пиньинь с тонами', async () => {
  const { text } = await tr.transliterate({ text: '你好', lang: 'zh' });
  assert.match(text, /n[ǐi]\s?h[ǎa]o/);
});
test('T-03 неподдерживаемый язык — пустой результат', async () => {
  assert.equal((await tr.transliterate({ text: 'Hello', lang: 'en' })).text, '');
});
test('T-04 текст длиннее 200 символов — пустой результат', async () => {
  assert.equal((await tr.transliterate({ text: 'а'.repeat(201), lang: 'ru' })).text, '');
});
test('T-05 переносы строк схлопываются в одну строку', async () => {
  const { text } = await tr.transliterate({ text: 'Привет\n\nмир', lang: 'ru' });
  assert.ok(!text.includes('\n'));
});
